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

	def Function(this):
		this.grammar = {}
		this.precedence = eons.util.DotDict()
		this.precedence.token = []
		this.precedence.rule = []
		this.possibleNestings = []

		this.parsableBlocks = [block for block in this.gen_lexer.blocks if not block in this.gen_lexer.defaultBlocks and not block in this.gen_lexer.defaultBlockSets and not isinstance(block, CatchAllBlock)]

		# NOTE: Block precedence < Strict Syntax precedence, so Block processing occurs first (buried deeper in the stack = lower precedence). 

		this.PopulateAbstractSyntaxGrammar()
		this.PopulateBlockGrammar()
		this.PopulateDefaultGrammar()
		this.PopulateStrictSyntaxGrammar()

		# Builtins
		this.precedence.token.append(f"('left', {', '.join([builtin.upper() for builtin in summary.builtins])})")

		# Rule Precedence
		for block in summary.blocks:
			this.precedence.rule.append(f"('right', '{block.upper()}')")

		for syntax in summary.syntax.abstract:
			this.precedence.rule.append(f"('right', '{syntax.upper()}')")

		# Strict Syntax always has the highest precedence.
		this.precedence.rule.append(f"('right', 'STRICT_SYNTAX')")

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
		# precedenceString = ',\n\t\t'.join(this.precedence.token)
		# precedenceString += ',\n\t\t'
		# precedenceString += ',\n\t\t'.join(this.precedence.rule)

		# FIXME: DELETEME
		precedenceString = ',\n\t\t'.join(this.precedence.rule)
		
		this.outFile.write(f"""\
class ElderParser(Parser):
	tokens = ElderLexer.tokens
	start = '{summary.startingBlock.lower()}'
	precedence = (
		{precedenceString}
	)

	def __init__(this):
		this.executor = eons.Executor(name="Parser")
		this.executor()
""")

		for implementation, rules in this.grammar.items():
			precedence = f" %prec {implementation.name.upper()}"
			if (isinstance(implementation, StrictSyntax)):
				precedence = " %prec STRICT_SYNTAX"
			this.outFile.write(f"\n\t@_(")
			for rule in rules:
				this.outFile.write(f"\n\t\t'{rule}{precedence}',")
			this.outFile.write(f"\n\t)")
			this.outFile.write(f"""
	def {implementation.name.lower()}(this, p):
		return this.executor.Execute("{implementation.name}", p=p).returned
""")
	
		if (this.debug):
			this.outFile.write("\n\tdebugfile = 'parsetab.out'\n")

		this.outFile.close()

		logging.debug(f"Done writing to {this.outFileName}")

	
	
	def PopulateAbstractSyntaxGrammar(this):
		for syntax in this.gen_lexer.syntax.abstract:
			if ("parser" in syntax.exclusions):
				continue

			match = ' '.join([block.lower() for block in syntax.blocks]).replace(summary.catchAllBlock.lower(), summary.catchAllBlock.upper())
			this.grammar[syntax] = [match]


	def PopulateBlockGrammar(this):
		blockPrecedenceOpen = []
		blockPrecedenceClose = []
		for block in this.parsableBlocks:
			if ("parser" in block.exclusions):
				continue
			
			openName = f"OPEN_{block.name.upper()}"
			closeName = f"CLOSE_{block.name.upper()}"

			if (isinstance(block, DefaultBlock)):
				closeName = f"CLOSE_{summary.defaultBlock.upper()}"
			elif (isinstance(block, OpenEndedBlock)):
				this.grammar[block] = [
					f"{openName} {block.content.lower()} EOL",
					f"{openName} {block.content.lower()} {openName}",
				]
				
				for closing in block.closings:
					this.grammar[block].append(f"{openName} {block.content.lower()} OPEN_{closing.upper()}")
			else:
				this.grammar[block].append(f"{openName} {block.content.lower()} {closeName}")

			if (openName in this.gen_lexer.tokens.open.keys()):
				blockPrecedenceOpen.append(openName)
			if (closeName in this.gen_lexer.tokens.close.keys()):
				blockPrecedenceClose.append(closeName)
		this.precedence.token.append(f"('left', {', '.join(blockPrecedenceOpen)}, {', '.join(blockPrecedenceClose)})")


	# These will not have tokens associated with them and thus no precedence.
	def PopulateDefaultGrammar(this):
		for block in this.gen_lexer.defaultBlockSets:
			if ("parser" in block.exclusions):
				continue

			adhere = this.gen_lexer.GetBlock(block.content)
			if (adhere is None):
				logging.error(f"Block {block.content} does not exist.")
				continue
			
			this.grammar[block] = [
				f"{adhere.name.lower()}",
				f"{block.name.lower()} {adhere.name.lower()}",
				f"{block.name.lower()} {block.name.lower()}",
			]

		for block in this.gen_lexer.defaultBlocks:
			if ("parser" in block.exclusions):
				continue

			for nest in block.nest:
				nestToken = nest.lower()
				if (nest == summary.catchAllBlock):
					nestToken = nest.upper()
				this.grammar[block] = [
					f"{nestToken}",
					f"{nestToken} EOL",
					f"{nestToken} CLOSE_{summary.defaultBlock.upper()}"
				]
				for closing in block.closings:
					this.grammar[block].append(f"{nestToken} {closing.lower()}")


	def PopulateStrictSyntaxGrammar(this):
		for syntax in this.gen_lexer.syntax.strict:
			if ("parser" in syntax.exclusions):
				continue
			
			match = syntax.match
			if (not syntax.literalMatch):
				match = this.gen_lexer.SubstituteRepresentations(
					syntax.match,
					" block ",
					quoteContents = False,
					replaceContentsWith = f" {syntax.name.upper()} "
				).replace(
					summary.catchAllBlock.lower(),
					summary.catchAllBlock.upper()
				)
			this.grammar[syntax] = [match]
			
			if (len(syntax.recurseOn)):
				recursiveMatch = match
				if (syntax.readDirection == ">"):
					recursiveMatch = recursiveMatch.replace(syntax.recurseOn, syntax.name.lower(), 1)
				elif (syntax.readDirection == "<"):
					recursiveMatch = recursiveMatch[::-1].replace(syntax.recurseOn[::-1], syntax.name.lower()[::-1], 1)[::-1]
				this.grammar[syntax].append(recursiveMatch)
		this.precedence.token.append(f"('left', {', '.join([syntax.name.upper() for syntax in this.gen_lexer.syntax.strict if not 'parser' in syntax.exclusions and syntax.name.upper() in this.gen_lexer.tokens.syntactic.keys()])})")