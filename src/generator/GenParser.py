import eons
import logging
import re
import copy
from .Blocks import *
from .Syntax import *
from .Expressions import *
from .Summary import summary

class GenParser(eons.Functor):

	def	__init__(this, name = "Sly Parser Generator"):
		super().__init__(name)

		this.requiredKWArgs.append('gen_lexer')

		this.optionalKWArgs['outFileName'] = "parser.py"

		this.optionalKWArgs['debug'] = False
		this.optionalKWArgs['custom_precedence'] = True

	def Function(this):
		this.grammar = {}
		this.precedence = eons.util.DotDict()
		this.precedence.token = eons.util.DotDict()
		this.precedence.token.block = []
		this.precedence.token.syntax = []
		this.precedence.rule = []
		this.precedence.prioritized = []
		this.precedence.deprioritized = []
		this.precedence.unparsedBlock = []
		this.possibleNestings = []

		this.tokens = list(this.gen_lexer.tokens.use.keys())

		this.parsableBlocks = [block for block in this.gen_lexer.blocks 
			if not block in this.gen_lexer.expressions 
			and not block in this.gen_lexer.expressionSets
			and not isinstance(block, CatchAllBlock)
		]

		# NOTE: Block precedence < Exact Syntax precedence, so Block processing occurs first (buried deeper in the stack = lower precedence). 

		this.PopulateBlockSyntaxGrammar()
		this.PopulateBlockGrammar()
		this.PopulateExactSyntaxGrammar()
		this.PopulateExpressionGrammar()
		this.PopulatePrecedence()

		# Build Grammar
		logging.debug(f"Grammar: {this.grammar.items}")
		logging.debug(f"Writing to {this.outFileName}")

		this.outFile = open(this.outFileName, 'w')
		
		localImports = [
			"lex",
			"yacc",
			"ast",
		]
		for imp in localImports:
			this.outFile.write(f"from .{imp} import *\n")
		
		globalImports = [
			"eons",
			"elderlangdefinitions"
		]
		for imp in globalImports:
			this.outFile.write(f"import {imp}\n")

		# Has to be declared outside of f-string to use backslashes.
		precedenceJoiner = ",\n\t\t"
		# precedenceString = f"('right', 'EXCLUDED'){precedenceJoiner}"
		precedenceString = "\t\t"
		if (len(this.precedence.deprioritized)):
			precedenceString += precedenceJoiner.join([f"('right', '{dep.upper()}')" for dep in this.precedence.deprioritized])
			precedenceString += precedenceJoiner
		if (len(this.precedence.token.block)):
			precedenceString += precedenceJoiner.join(this.precedence.token.block)
			precedenceString += precedenceJoiner
		if (len(this.precedence.token.syntax)):
			precedenceString += precedenceJoiner.join(this.precedence.token.syntax)
			precedenceString += precedenceJoiner
		if (len(this.precedence.unparsedBlock)):
			precedenceString += precedenceJoiner.join(this.precedence.unparsedBlock)
			precedenceString += precedenceJoiner
		if (len(this.precedence.rule)):	
			precedenceString += precedenceJoiner.join(this.precedence.rule)
			precedenceString += precedenceJoiner
		if (len(this.gen_lexer.tokens.syntactic.keys())):
			precedenceString += f"('right', {', '.join([t for t in this.gen_lexer.tokens.syntactic.keys() if t != 'EOL'])})"
			precedenceString += precedenceJoiner
		precedenceString += f"('right', {summary.catchAllBlock.upper()})"
		precedenceString += precedenceJoiner
		builtins = [builtin.upper() for builtin in summary.builtins]
		if (len(builtins)):
			precedenceString += f"('right', {', '.join(builtins)})"
			precedenceString += precedenceJoiner
		if (len(this.precedence.prioritized)):
			precedenceString += precedenceJoiner.join([f"('right', '{pri.upper()}')" for pri in this.precedence.prioritized])
		
		this.outFile.write(f"""\
class ElderParser(Parser):
	tokens = {{ {', '.join([t for t in this.tokens])} }}
	start = '{summary.startingBlock.lower()}'
""")

		if (this.custom_precedence):
			this.outFile.write(f"""
	precedence = (
{precedenceString}
	)
""")
		if (this.debug):
			this.outFile.write("\n\tdebugfile = 'parsetab.out'\n")

# Replaced by parser.executor = this in ELDERLANG
# 		this.outFile.write(f"""
# 	def __init__(this):
# 		this.executor = eons.Executor(name="Parser")
# 		this.executor.parser = this
# 		this.executor.lexer = ElderLexer()
# 		this.executor.sanitize = Sanitize()
# 		this.executor()
# """)
		this.grammarQueue = {i:r for i,r in this.grammar.items() if hasattr(i, "before") and i.before}
		this.grammar = {i:r for i,r in this.grammar.items() if i not in this.grammarQueue.keys()}
		for implementation, rules in this.grammar.items():
			this.WriteGrammar(implementation, rules)

		this.outFile.write(f"""
	@_('{summary.catchAllBlock.upper()} %prec {summary.catchAllBlock.upper()}')
	def {summary.catchAllBlock.lower()}(this, p):
		ret = this.executor.Execute("{summary.catchAllBlock}", p=p).returned
		logging.debug(f"{summary.catchAllBlock} produced {{ret}}")
		return ret
	
	@_(
		'NUMBER %prec NUMBER',
		'NUMBER EXPLICITACCESS NUMBER %prec NUMBER',
		'number EXPLICITACCESS NUMBER %prec NUMBER',
	)
	def number(this, p):
		isFloat = False
		try:
			if (p[1] == '.'):
				isFloat = True
		except:
			pass
		if (isFloat):
			return float(f"{{p[0]}}.{{p[2]}}")
		return int(p[0])
""")

		this.outFile.close()

		logging.debug(f"Done writing to {this.outFileName}")


	def PopulatePrecedence(this):
		logging.debug(f"Populating Precedence")

		# CLOSE_EXPRESSION should be the lowest priority possible, since it directly translates EOLs.
		this.precedence.rule.append(f"('right', 'CLOSE_{summary.expression.upper()}')")

		for block in summary.blocks:
			if (block == summary.catchAllBlock):
				continue
			
			blockObject = this.gen_lexer.GetBlock(block)
			if (blockObject is None):
				continue
			if ('parser' in blockObject.exclusions):
				continue
			if ('prioritize' in blockObject.overrides):
				this.precedence.prioritized.append(block)
				continue
			if ('deprioritize' in blockObject.overrides):
				this.precedence.deprioritized.append(block)
				continue
			if (blockObject.content is None): # NOTE: This must come BEFORE the exclusions check (we'll use it later).
				this.precedence.unparsedBlock.append(f"('right', '{block.upper()}')")
				continue
			this.precedence.rule.append(f"('right', '{block.upper()}')")

		for syntax in summary.syntax.block:
			this.precedence.rule.append(f"('right', '{syntax.upper()}')")


	# Recursive to implement the "before" keyword.
	def WriteGrammar(this, implementation, rules):
		implName = ""
		if (isinstance(implementation, str)):
			implName = implementation
		else:
			implName = implementation.name
		logging.debug(f"Writing grammar for {implName}")

		for queuedImplementation, queuedRules in list(this.grammarQueue.items()):
			if (implName == queuedImplementation.before):
				this.WriteGrammar(queuedImplementation, queuedRules)
				del this.grammarQueue[queuedImplementation]
		
		if (this.custom_precedence):
			precedence = f" %prec {implName.upper()}"
			# if ('precedence' in implementation.exclusions):
			# 	precedence = " %prec EXCLUDED"
			# if (isinstance(implementation, ExactSyntax)):
			# 	precedence = " %prec EXACT_SYNTAX"
		else:
			precedence = ""
		
		this.outFile.write(f"\n\t@_(")
		for rule in rules:
			if (rule in ['NULL', 'PASSTHROUGH']):
				continue
			if (rule.startswith('PRECEDENCE')):
				precedence = f" %prec {rule.split(' ')[1].upper()}"
				continue
			this.outFile.write(f"\n\t\t'{rule}{precedence}',")

		this.outFile.write(f"\n\t)")
		this.outFile.write(f"""
	def {implName.lower()}(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {{pstr}}...")
""")
		if ('NULL' in rules):
			this.outFile.write("\t\tret = ''")
		elif ('PASSTHROUGH' in rules):
			this.outFile.write("\t\tret = p[0]")
		else:
			this.outFile.write(f'\t\tret = this.executor.Execute("{implName}", p=p).returned')
		
		this.outFile.write(f"""
		logging.info(f"...{implName} produced {{ret}}")
		return ret
""")

	
	def PopulateBlockSyntaxGrammar(this):
		logging.debug(f"Populating Block Syntax Grammar")

		for syntax in this.gen_lexer.syntax.block:
			if ("parser" in syntax.exclusions):
				continue

			standardMatch = ' '.join([block.lower() for block in syntax.blocks]) + ' '
			matches = [standardMatch]

			# Determine which other syntax we can use to build this one.
			predecessor = None
			for otherSyntax in this.gen_lexer.syntax.block:
				if (otherSyntax == syntax):
					continue
				if (predecessor is not None and len(otherSyntax.blocks) < len(predecessor.blocks)):
					continue
				if (syntax.blocks[:len(otherSyntax.blocks)] == otherSyntax.blocks):
					predecessor = otherSyntax

			predecessorMatch = None
			if (predecessor is not None):
				remainingBlocks = syntax.blocks[len(predecessor.blocks):]
				predecessorMatch = predecessor.name.lower() + ' ' + ' '.join([block.lower() for block in remainingBlocks]) + ' '
				matches.append(predecessorMatch)

			for match in [standardMatch, predecessorMatch]:
				if (match is None):
					continue
				matches.append(match)
				# for i in range(len(syntax.blocks)):
				# 	matches.append(match.replace(' ', ' EOL ', i))
				# 	i += 1
				# for i in range(len(syntax.blocks)):
				# 	matches.append(match[::-1].replace(' ', ' LOE ', i)[::-1])
				# 	i += 1

			this.grammar[syntax] = list(set(matches))


	def PopulateBlockGrammar(this):
		logging.debug(f"Populating Block Grammar")

		blockPrecedenceOpen = []
		blockPrecedenceClose = []
		for block in this.parsableBlocks:
			if ("parser" in block.exclusions):
				try:
					this.tokens.remove(block.name.upper())
				except:
					pass
				continue

			# MetaBlocks should also not have a content, so we need to check for the MetaBlock type before block.content is None.
			if (isinstance(block, MetaBlock)):
				this.grammar[block] = [b.lower() for b in block.compose]
				continue
				# disregard EOL for now.

			if (block.content is None):
				this.grammar[block] = [
					f"{block.name.upper()}",
				]
				continue
			
			openName = f"OPEN_{block.name.upper()}"
			closeName = f"CLOSE_{block.name.upper()}"

			if (isinstance(block, Expression)):
				closeName = f"CLOSE_{summary.expression.upper()}"

			elif (isinstance(block, OpenEndedBlock)):
				this.grammar[block] = [
					f"{openName.lower()} {block.content.lower()}",
					f"{openName.lower()} {block.content.lower()} close_{summary.expression.lower()}",
					f"{openName.lower()} {block.content.lower()} {openName.lower()}",
					f"{openName.lower()} {openName.lower()}",
					f"{openName.lower()}",
					f"{block.name.lower()} {openName.lower()}",

					# TODO: why doesn't upper (i.e. token) -> lower (i.e. rule) work? Can be tested with Kind.
					f"{openName.upper()} {block.content.lower()}",
					f"{openName.upper()} {block.content.lower()} close_{summary.expression.lower()}",
					f"{openName.upper()} {block.content.lower()} {openName.upper()}",
					f"{openName.upper()} {openName.upper()}",
				]

				for closing in block.closings:
					this.grammar[block].append(f"{openName} {block.content.lower()} {closing.lower()}")

				# Not necessary, now that we inject CLOSE_EXPRESSION tokens before other CLOSings.
				# if (block.content.endswith('Set')):
				# 	this.grammar[block] += [
				# 		rule.replace('set', '') for rule in this.grammar[block]
				# 	]

			elif (isinstance(block, SymmetricBlock)):
				continue

				# At the moment, all symmetric blocks are lexed as whole tokens (e.g. ".*?")

				# this.grammar[block] = [
				# 	f"{openName.lower()} {block.content.lower()} {openName.lower()}",
				# 	f"{openName.lower()} {openName.lower()}",
				# ]
			
			else:
				this.grammar[block] = [
					f"{openName.lower()} {block.content.lower()} {closeName.lower()}",
					f"{openName.lower()} {closeName.lower()}",
				]
				if (block.content.endswith('Set')):
					this.grammar[block].append(f"{openName.lower()} {block.content[:-3].lower()} {closeName.lower()}")

			for name, key in {'openName': 'open', 'closeName': 'close'}.items():
				actualName = eval(name)
				if (actualName.upper() in this.gen_lexer.tokens[key].keys()):
					exec(f"blockPrecedence{key.title()}.append({name}.upper())")
					this.grammar[actualName] = [
						'NULL',
						f"{actualName.upper()}",
					]

		if (len(blockPrecedenceOpen) and len(blockPrecedenceClose)):
			this.precedence.token.block.append(f"('right', {', '.join(blockPrecedenceOpen)}, {', '.join(blockPrecedenceClose)})")


	# These will not have tokens associated with them and thus no precedence.
	def PopulateExpressionGrammar(this):
		logging.debug(f"Populating Expression Grammar")

		for block in this.gen_lexer.expressionSets:
			if ("parser" in block.exclusions):
				continue

			adhere = this.gen_lexer.GetBlock(block.content)
			if (adhere is None):
				logging.error(f"Block {block.content} does not exist.")
				continue

			this.grammar[block] = [
				f"complete{adhere.name.lower()}",
				f"{block.name.lower()} complete{adhere.name.lower()}",
			]

		firstExpression = True
		for block in this.gen_lexer.expressions:
			if ("parser" in block.exclusions):
				continue

			this.grammar[block] = []
			for nest in block.nest:
				nestToken = nest.lower()
				this.grammar[block] += [
					f"{nestToken}",
				]

			this.grammar[f"complete{block.name.lower()}"] = [
				'PASSTHROUGH',
				f"PRECEDENCE {block.name.upper()}",
				f"{block.name.lower()} close_{summary.expression.lower()}",
			]

			if (firstExpression):
				this.grammar[f"complete{block.name.lower()}"].append(f"close_{summary.expression.lower()}")
				firstExpression = False

			for closing in block.closings:
				this.grammar[f"complete{block.name.lower()}"].append(f"{block.name.lower()} {closing.lower()}")


		this.grammar[f"close_{summary.expression.lower()}"] = [
			"NULL",
			f"EOL",
			f"CLOSE_{summary.expression.upper()}",
			f"close_{summary.expression.lower()} CLOSE_{summary.expression.upper()}",
			f"close_{summary.expression.lower()} EOL",
		]


	def PopulateExactSyntaxGrammar(this):
		logging.debug(f"Populating Exact Syntax Grammar")

		tokens = []
		for syntax in this.gen_lexer.syntax.exact:
			if ("parser" in syntax.exclusions):
				continue

			precedenceName = f"{syntax.name.upper()}_SYNTAX"

			if ('prioritize' in syntax.overrides):
				this.precedence.prioritized.append(precedenceName)
			elif ('deprioritize' in syntax.overrides):
				this.precedence.deprioritized.append(precedenceName)
			else:
				tokens.append(precedenceName)

			match = [
				f"PRECEDENCE {precedenceName}",
			]
			if (isinstance(syntax, FlexibleTokenSyntax)):
				for m in syntax.match:
					if (isinstance(m, dict)):
						if (len(m.keys()) == 2):
							for first in m['first']:
								for second in m['second']:
									match.append(f"{first} {second}")
						elif (len(m.keys()) == 3):
							for first in m['first']:
								for second in m['second']:
									for third in m['third']:
										match.append(f"{first} {second} {third}")
						else:
							logging.error(f"Unsupported match format: {m}")
					else:
						match.append(m)

			else:
				match.extend([this.gen_lexer.SubstituteRepresentations(
					syntax.match,
					" block ",
					quoteContents = False,
					replaceContentsWith = f" {syntax.name.upper()} "
				)])
			this.grammar[syntax] = match
			
			if (syntax.recurseOn is not None and len(syntax.recurseOn)):
				for i in range(len(match)):
					recursiveMatch = match[i]
					if (syntax.readDirection == ">"):
						recursiveMatch = re.sub(rf"\b{syntax.recurseOn}\b", syntax.name.lower(), recursiveMatch, 1)
					elif (syntax.readDirection == "<"):
						recursiveMatch = re.sub(rf"\b{syntax.recurseOn[::-1]}\b", syntax.name.lower()[::-1], recursiveMatch[::-1], 1)[::-1]

					if (recursiveMatch != match[i]):
						this.grammar[syntax].append(recursiveMatch)

		tokensByAscendingPriorityOrder = copy.copy(tokens)
		tokensByAscendingPriorityOrder.reverse()
		for tok in tokensByAscendingPriorityOrder:
			this.precedence.token.syntax.append(f"('right', '{tok}')")