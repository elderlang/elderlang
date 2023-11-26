import eons
import logging
from .Blocks import *
from .Summary import summary

class GenParser(eons.Functor):

	def	__init__(this, name = "Sly Parser Generator"):
		super().__init__(name)

		this.requiredKWArgs.append('gen_lexer')

		this.optionalKWArgs['outFileName'] = "parser.py"

	def Function(this):
		this.grammar = {}
		this.precedence = []
		this.possibleNestings = []

		this.parsableBlocks = [block for block in this.gen_lexer.blocks if not block in this.gen_lexer.defaultBlocks and not block in this.gen_lexer.defaultBlockSets and not isinstance(block, CatchAllBlock)]

		# NOTE: Block precedence < Strict Syntax precedence, so Block processing occurs first (buried deeper in the stack = lower precedence). 

		# Default Blocks
		# These will not have tokens associated with them and thus no precedence.
		for block in this.gen_lexer.defaultBlockSets:
			if ("parser" in block.exclusions):
				continue

			adhere = this.gen_lexer.GetBlock(block.content)
			if (adhere is None):
				logging.error(f"Block {block.content} does not exist.")
				continue
			for nest in adhere.nest:
				nestToken = nest.lower()
				if (nest == summary.catchAllBlock):
					nestToken = nest.upper()
				this.grammar[f"{block.name.lower()} {nestToken}"] = block
				this.grammar[f"{nestToken}"] = adhere
			this.grammar[adhere.name.lower()] = block

		# All Other Blocks
		blockPrecedenceOpen = []
		blockPrecedenceClose = []
		for block in this.parsableBlocks:
			if ("parser" in block.exclusions):
				continue
			
			openName = f"OPEN_{block.name.upper()}"
			closeName = f"CLOSE_{block.name.upper()}"

			if (isinstance(block, DefaultBlock)):
				closeName = f"CLOSE_{summary.defaultBlock.upper()}"
				this.grammar[f"{block.content.lower()} EOL"] = block
				this.grammar[f"{block.content.lower()} {closeName}"] = block
				for closing in block.closings:
					this.grammar[f"{block.content.lower()} OPEN_{closing.upper()}"] = block
			elif (isinstance(block, OpenEndedBlock)):
				this.grammar[f"{openName} {block.content.lower()} EOL"] = block
				this.grammar[f"{openName} {block.content.lower()} {openName}"] = block
				for closing in block.closings:
					this.grammar[f"{openName} {block.content.lower()} OPEN_{closing.upper()}"] = block
			else:
				this.grammar[f"{openName} {block.content.lower()} {closeName}"] = block

			if (openName in this.gen_lexer.tokens.open.keys()):
				blockPrecedenceOpen.append(openName)
			if (closeName in this.gen_lexer.tokens.close.keys()):
				blockPrecedenceClose.append(closeName)
		this.precedence.append(f"('left', {', '.join(blockPrecedenceOpen)}, {', '.join(blockPrecedenceClose)})")
		
		
		# Abstract Syntax
		# Abstract Syntaxes will not have tokens associated with them and thus no precedence.
		for syntax in this.gen_lexer.syntax.abstract:
			if ("parser" in syntax.exclusions):
				continue

			match = ' '.join([block.lower() for block in syntax.blocks]).replace(summary.catchAllBlock.lower(), summary.catchAllBlock.upper())
			this.grammar[match] = syntax

		# Strict Syntax
		for syntax in this.gen_lexer.syntax.strict:
			if ("parser" in syntax.exclusions):
				continue

			match = this.gen_lexer.SubstituteRepresentations(syntax.match, " block ", True).replace(summary.catchAllBlock.lower(), summary.catchAllBlock.upper())
			this.grammar[match] = syntax
			
			if (len(syntax.recurseOn)):
				recursiveMatch = match
				if (syntax.readDirection == ">"):
					recursiveMatch = recursiveMatch.replace(syntax.recurseOn, syntax.name.lower(), 1)
				elif (syntax.readDirection == "<"):
					recursiveMatch = recursiveMatch[::-1].replace(syntax.recurseOn[::-1], syntax.name.lower()[::-1], 1)[::-1]
				this.grammar[recursiveMatch] = syntax
		this.precedence.append(f"('left', {', '.join([syntax.name.upper() for syntax in this.gen_lexer.syntax.strict if not 'parser' in syntax.exclusions and syntax.name.upper() in this.gen_lexer.tokens.syntactic.keys()])})")

		# Builtins
		this.precedence.append(f"('left', {', '.join([builtin.upper() for builtin in summary.builtins])})")

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
		precedenceString = ',\n\t\t'.join(this.precedence)
		
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
	
		for rule,implementation in this.grammar.items():
			this.outFile.write(f"""
	@_('{rule}')
	def {implementation.name.lower()}(this, p):
		return this.executor.Execute("{implementation.name}", p=p).returned
""")

		this.outFile.close()

		logging.debug(f"Done writing to {this.outFileName}")
