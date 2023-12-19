import eons
import logging
from .Blocks import *
from .Syntax import *
from .Expressions import *
from .Summary import summary

class GenParser(eons.Functor):

	def	__init__(this, name = "Sly Parser Generator"):
		super().__init__(name)

		this.requiredKWArgs.append('gen_lexer')

		this.optionalKWArgs['outFileName'] = "parser.py"

		this.optionalKWArgs['debug'] = True
		this.optionalKWArgs['custom_precedence'] = True

	def Function(this):
		this.grammar = {}
		this.precedence = eons.util.DotDict()
		this.precedence.token = []
		this.precedence.rule = []
		this.precedence.unparsedBlock = []
		this.possibleNestings = []

		this.tokens = list(this.gen_lexer.tokens.all.keys())

		this.parsableBlocks = [block for block in this.gen_lexer.blocks 
			if not block in this.gen_lexer.expressions 
			and not block in this.gen_lexer.expressionSets
			and not isinstance(block, CatchAllBlock)
		]

		# NOTE: Block precedence < Exact Syntax precedence, so Block processing occurs first (buried deeper in the stack = lower precedence). 

		this.PopulateBlockSyntaxGrammar()
		this.PopulateBlockGrammar()
		this.PopulateExpressionGrammar()
		this.PopulateExactSyntaxGrammar()
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
		precedenceString = precedenceJoiner[2:]
		precedenceString += precedenceJoiner.join(this.precedence.rule)
		precedenceString += precedenceJoiner
		precedenceString += precedenceJoiner.join(this.precedence.token)
		precedenceString += precedenceJoiner
		precedenceString += precedenceJoiner.join(this.precedence.unparsedBlock)
		
		this.outFile.write(f"""\
class ElderParser(Parser):
	tokens = {{ {', '.join(summary.builtins)}, {', '.join([t for t in this.tokens])} }}
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

		this.outFile.write(f"""
	def __init__(this):
		this.executor = eons.Executor(name="Parser")
		this.executor.parser = this
		this.executor.lexer = ElderLexer()
		this.executor()
""")
		this.grammarQueue = {i:r for i,r in this.grammar.items() if hasattr(i, "before") and i.before}
		this.grammar = {i:r for i,r in this.grammar.items() if i not in this.grammarQueue.keys()}
		for implementation, rules in this.grammar.items():
			this.WriteGrammar(implementation, rules)

		this.outFile.write(f"""
	@_('{summary.catchAllBlock.upper()}')
	def {summary.catchAllBlock.lower()}(this, p):
		ret = this.executor.Execute("{summary.catchAllBlock}", p=p).returned
		logging.info(f"{summary.catchAllBlock} produced {{ret}}")
		return ret
	
	@_('NUMBER')
	def number(this, p):
		return p[0]
""")

		this.outFile.close()

		logging.debug(f"Done writing to {this.outFileName}")


	def PopulatePrecedence(this):
		logging.debug(f"Populating Precedence")

		builtins = [builtin.upper() for builtin in summary.builtins]
		if (len(builtins)):
			this.precedence.token.append(f"('left', {', '.join(builtins)})")

		for syntax in summary.syntax.block:
			this.precedence.rule.append(f"('left', '{syntax.upper()}')")

		for block in summary.blocks:
			if (block == summary.catchAllBlock):
				continue
			blockObject = this.gen_lexer.GetBlock(block)
			if (blockObject is None):
				continue
			if ('parser' in blockObject.exclusions):
				continue
			if (blockObject.content is None): # NOTE: This must come BEFORE the exclusions check (we'll use it later).
				this.precedence.unparsedBlock.append(f"('left', '{block.upper()}')")
				continue
			if ("parser" in blockObject.exclusions):
				continue
			this.precedence.rule.append(f"('left', '{block.upper()}')")
		

		# Exact Syntax always has precedence over Block Syntax.
		this.precedence.rule.append(f"('left', 'EXACT_SYNTAX')")

	# Recursive to implement the "before" keyword.
	def WriteGrammar(this, implementation, rules):
		logging.debug(f"Writing grammar for {implementation.name}")

		for queuedImplementation, queuedRules in list(this.grammarQueue.items()):
			if (implementation.name == queuedImplementation.before):
				this.WriteGrammar(queuedImplementation, queuedRules)
				del this.grammarQueue[queuedImplementation]
		
		if (this.custom_precedence):
			precedence = f" %prec {implementation.name.upper()}"
			# if ('precedence' in implementation.exclusions):
			# 	precedence = " %prec EXCLUDED"
			if (isinstance(implementation, ExactSyntax)):
				precedence = " %prec EXACT_SYNTAX"
		else:
			precedence = ""
		
		this.outFile.write(f"\n\t@_(")
		for rule in rules:
			this.outFile.write(f"\n\t\t'{rule}{precedence}',")
			# this.outFile.write(f"\n\t\t'{rule}',") # precedence is currently per grammar order
		this.outFile.write(f"\n\t)")
		this.outFile.write(f"""
	def {implementation.name.lower()}(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.critical(f"Given {{pstr}}...")
		ret = this.executor.Execute("{implementation.name}", p=p).returned
		logging.critical(f"...{implementation.name} produced {{ret}}")
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
				for i in range(len(syntax.blocks)):
					matches.append(match.replace(' ', ' EOL ', i))
					i += 1
				for i in range(len(syntax.blocks)):
					matches.append(match[::-1].replace(' ', ' LOE ', i)[::-1])
					i += 1
			
			this.grammar[syntax] = list(set(matches))


	def PopulateBlockGrammar(this):
		logging.debug(f"Populating Block Grammar")

		blockPrecedenceOpen = []
		blockPrecedenceClose = []
		for block in this.parsableBlocks:
			if ("parser" in block.exclusions):
				this.tokens.remove(block.name.upper())
				continue

			# MetaBlocks should also not have a content, so we need to check for the MetaBlock type before block.content is None.
			if (isinstance(block, MetaBlock)):
				this.grammar[block] = [b.lower() for b in block.compose]
				continue
				# disregard EOL for now.

			if (block.content is None):
				this.grammar[block] = [
					f"{block.name.upper()}",
					f"{block.name.upper()} EOL"
				]
				continue
			
			openName = f"OPEN_{block.name.upper()}"
			closeName = f"CLOSE_{block.name.upper()}"

			if (isinstance(block, Expression)):
				closeName = f"CLOSE_{summary.expression.upper()}"

			elif (isinstance(block, OpenEndedBlock)):
				this.grammar[block] = [
					# f"{openName} {block.content.lower()} EOL", # Things like LimitedExpressionSet incorporate EOL, so using it here causes reduce/reduce conflicts.
					f"{openName} {block.content.lower()}",
					f"{openName} {block.content.lower()} {openName}",
					f"{openName} {block.content.lower()} {openName} EOL",
				]
				
				for closing in block.closings:
					this.grammar[block].append(f"{openName} {block.content.lower()} {closing.lower()}")
			
			elif (isinstance(block, SymmetricBlock)):
				this.grammar[block] = [
					f"{openName} {block.content.lower()} {openName}",
					f"{openName} EOL {block.content.lower()} EOL {openName}",
					f"{openName} EOL {block.content.lower()} {openName}",
					f"{openName} {block.content.lower()} EOL {openName}",
					f"{openName} {block.content.lower()} {openName} EOL",
					f"{openName} EOL {block.content.lower()} EOL {openName} EOL",
					f"{openName} EOL {block.content.lower()} {openName} EOL",
					f"{openName} {block.content.lower()} EOL {openName} EOL",
					f"{openName} {openName}",
					f"{openName} {openName} EOL",
					f"{openName} EOL {openName}",
					f"{openName} EOL {openName} EOL",
				]
			
			else:
				this.grammar[block] = [
					f"{openName} {block.content.lower()} {closeName}",
					f"{openName} EOL {block.content.lower()} EOL {closeName}",
					f"{openName} {block.content.lower()} EOL {closeName}",
					f"{openName} EOL {block.content.lower()} {closeName}",
					f"{openName} {block.content.lower()} {closeName} EOL",
					f"{openName} EOL {block.content.lower()} EOL {closeName} EOL",
					f"{openName} {block.content.lower()} EOL {closeName} EOL",
					f"{openName} EOL {block.content.lower()} {closeName} EOL",
					f"{openName} {closeName}",
					f"{openName} EOL {closeName}",
					f"{openName} {closeName} EOL",
					f"{openName} EOL {closeName} EOL",
				]

			if (openName in this.gen_lexer.tokens.open.keys()):
				blockPrecedenceOpen.append(openName)
			if (closeName in this.gen_lexer.tokens.close.keys()):
				blockPrecedenceClose.append(closeName)
		if (len(blockPrecedenceOpen) and len(blockPrecedenceClose)):
			this.precedence.token.append(f"('left', {', '.join(blockPrecedenceOpen)}, {', '.join(blockPrecedenceClose)})")


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
				f"{adhere.name.lower()}",
				f"{adhere.name.lower()} EOL",
				f"{block.name.lower()} EOL",
				f"{block.name.lower()} {adhere.name.lower()}",
				f"{block.name.lower()} {adhere.name.lower()} EOL",
				# f"{block.name.lower()} {block.name.lower()}",
			]

		for block in this.gen_lexer.expressions:
			if ("parser" in block.exclusions):
				continue

			this.grammar[block] = []
			for nest in block.nest:
				nestToken = nest.lower()
				this.grammar[block] += [
					f"{nestToken}",
					f"{nestToken} CLOSE_{summary.expression.upper()}",
				]
				for closing in block.closings:
					this.grammar[block].append(f"{nestToken} {closing.lower()}")


	def PopulateExactSyntaxGrammar(this):
		logging.debug(f"Populating Exact Syntax Grammar")

		tokens = []
		for syntax in this.gen_lexer.syntax.exact:
			if ("parser" in syntax.exclusions):
				continue

			match = []
			if (isinstance(syntax, FlexibleTokenSyntax)):
				match = syntax.match
			
			else:
				match = [this.gen_lexer.SubstituteRepresentations(
					syntax.match,
					" block ",
					quoteContents = False,
					replaceContentsWith = f" {syntax.name.upper()} "
				)]
			this.grammar[syntax] = match
			
			if (len(syntax.recurseOn)):
				for i in range(len(match)):
					recursiveMatch = match[i]
					if (syntax.readDirection == ">"):
						recursiveMatch = recursiveMatch.replace(syntax.recurseOn, syntax.name.lower(), 1)
					elif (syntax.readDirection == "<"):
						recursiveMatch = recursiveMatch[::-1].replace(syntax.recurseOn[::-1], syntax.name.lower()[::-1], 1)[::-1]
					this.grammar[syntax].append(recursiveMatch)
		
		tokens += [syntax.name.upper() for syntax in this.gen_lexer.syntax.exact
			if not 'parser' in syntax.exclusions 
			and syntax.name.upper() in this.gen_lexer.tokens.syntactic.keys()
		]
		tokens.append(summary.catchAllBlock.upper())
		this.precedence.token.append(f"('left', {', '.join(tokens)})")