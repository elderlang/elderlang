import eons
import logging
import re
from .Blocks import *
from .Expressions import *
from .Summary import summary

class GenLexer(eons.Functor):

	def	__init__(this, name = "Sly Lexer Generator"):
		super().__init__(name)

		this.optionalKWArgs['outFileName'] = "lexer.py"

	def GetBlock(this, name):
		for block in this.blocks:
			if (block.name == name):
				return block
		return None
	
	def SubstituteRepresentations(this, 
		string,
		substitution = "",
		separateTokensWith = " ",
		quoteContents = False,
		replaceContentsWith = None
	):
		if (quoteContents or replaceContentsWith is not None):
			contents = string
			for block in this.blocks:
				contents = contents.replace(block.representation, '')
				if (separateTokensWith is not None):
					string = string.replace(block.representation, f"{separateTokensWith}{block.representation}{separateTokensWith}")
			for builtin in summary.builtins:
				contents = contents.replace(builtin, '')
				if (separateTokensWith is not None):
					string = string.replace(builtin, f"{separateTokensWith}{builtin}{separateTokensWith}")
			
			if (len(contents)):
				if (replaceContentsWith is not None):
					string = string.replace(contents, replaceContentsWith)
				else:
					for char in contents:
						string = string.replace(char, f' "{char}" ')

		for block in this.blocks:
			sub = substitution.replace("Block", block.name)
			sub = substitution.replace("BLOCK", block.name.upper())
			sub = substitution.replace("block", block.name.lower())
			string = string.replace(block.representation, sub)
		
		while ('  ' in string):
			string = string.replace('  ', ' ')
		
		return string.strip()
	
	def Function(this):
		this.blocks = []
		this.syntax = eons.util.DotDict()
		this.syntax.block = []
		this.syntax.exact = []
		this.expressions = []
		this.expressionSets = []
		this.catchAllBlock = None

		for name in summary.blocks:
			toAppend = eons.SelfRegistering(name)
			this.blocks.append(toAppend)
			if (isinstance(toAppend, CatchAllBlock)):
				this.catchAllBlock = toAppend
			elif (isinstance(toAppend, Expression)):
				this.expressions.append(toAppend)
			elif (isinstance(toAppend, ExpressionSet)):
				this.expressionSets.append(toAppend)
		
		for name in summary.syntax.block:
			this.syntax.block.append(eons.SelfRegistering(name))
		
		for name in summary.syntax.exact:
			this.syntax.exact.append(eons.SelfRegistering(name))

		this.tokens = eons.util.DotDict()
		this.tokens.unparsed = {}
		this.tokens.open = {}
		this.tokens.close = {}
		this.tokens.syntactic = {}
		this.tokens.ignore = {}
		this.tokens.excludeFromCatchAll = []
		this.tokens.partial = []

		for block in this.blocks:
			block.WarmUp(executor = this.executor, precursor = None)

			if ('lexer' in block.exclusions):
				continue
			
			tokenSources = {'openings': 'open', 'closings': 'close'}

			if (isinstance(block, Expression)):
				continue
			elif (isinstance(block, OpenEndedBlock) or isinstance(block, SymmetricBlock)):
				del tokenSources['closings']
			elif (isinstance(block, CatchAllBlock)):
				continue

			if (block.content is None):
				regex = None

				closings = block.closings
				if (isinstance(block, OpenEndedBlock)):
					regex = fr"({'|'.join(block.openings)})(?:(?!:\n).)+"
				elif (isinstance(block, SymmetricBlock)):
					closings = block.openings
				
				if (regex is None):
					regex = fr"({'|'.join(block.openings)}).*?({'|'.join(closings)})"
				
				if ('tokens' in block.exclusions):
					this.tokens.ignore[block.name] = regex
				else:
					this.tokens.unparsed[block.name.upper()] = regex
				
				if (not "all.catch.block" in block.exclusions):
					this.tokens.partial = this.tokens.partial + block.openings + block.closings
				continue

			for source, name in tokenSources.items():
				matches = eval(f"block.{source}")
				if (len(matches)):
					blockName =f"{name}_{block.name}".upper()
					this.tokens.partial += matches
					this.tokens[name][blockName] = fr"\s*({'|'.join(matches)})\s*"
					if ("all.catch.block" in block.exclusions):
						this.tokens.excludeFromCatchAll.append(blockName)
		
		# NOTE: "Openings" function as "closings" for the Expression only.
		# For example, start(expression); open(next_expression) // ; closes the first, even though it opens the second.
		this.expression = eons.SelfRegistering(summary.expression)
		this.expression.WarmUp(executor = this.executor, precursor = None)
		this.tokens.partial += this.expression.openings
		this.tokens['close'][f"CLOSE_{this.expression.name.upper()}"] = fr"({'|'.join(this.expression.openings)})"

		for syntax in this.syntax.block:
			syntax.WarmUp(executor = this.executor, precursor = None)
			# Nothing to do yet, but everything needs to be warm before we pass *this off to the Parser.

		for syntax in this.syntax.exact:
			syntax.WarmUp(executor = this.executor, precursor = None)
			if ('lexer' in syntax.exclusions):
				continue
			possibleToken = syntax.match
			possibleToken = this.SubstituteRepresentations(possibleToken, "")
			for builtin in summary.builtins:
				possibleToken = possibleToken.replace(builtin, '')
			possibleToken = fr"({possibleToken})"
			if (
				len(possibleToken) > 2
				and possibleToken not in this.tokens.syntactic.values()
			):
				this.tokens.syntactic[syntax.name.upper()] = possibleToken
				if ("all.catch.block" in syntax.exclusions):
					this.tokens.excludeFromCatchAll.append(syntax.name.upper())
			else:
				logging.info(f"Syntax {syntax.name} has no matchable tokens.")

		this.tokens.all = {}
		this.tokens.all.update(this.tokens.open)
		this.tokens.all.update(this.tokens.close)
		this.tokens.all.update(this.tokens.syntactic)

		this.tokens.all[summary.catchAllBlock.upper()] = fr"[{''.join(this.catchAllBlock.specialStarts)}]?(?:(?!{'|'.join(t for t in this.tokens.partial)})\S)+"

		this.tokens.use = this.tokens.unparsed
		this.tokens.use.update(this.tokens.all)

		logging.debug(f"Tokens: {this.tokens.all}")

		logging.debug(f"Writing to {this.outFileName}")

		imports = [
			"lex",
			"yacc",
			"ast",
		]

		this.outFile = open(this.outFileName, 'w')
		for imp in imports:
			this.outFile.write(f"from .{imp} import *\n")
		this.outFile.write(f"""\
class ElderLexer(Lexer):
	def error(self, t):
		print("Illegal character '%s'" % t.value[0])
		self.index += 1

	def t_NUMBER(t):
		r'\d+'
		t.value = int(t.value)
		return t

	tokens = {{ {', '.join(summary.builtins)}, {', '.join([t for t in this.tokens.use.keys()])} }}

	ignore = ' \\t'
""")
		for token,regex in this.tokens.ignore.items():
			this.outFile.write(f"\n\tignore_{token.lower()} = r'{regex}'")

		this.outFile.write("\n\n")

		for token,regex in this.tokens.use.items():
			this.outFile.write(f"\t{token} = r'{regex}'\n")

		for block in this.blocks:
			if ('lexer' in block.exclusions
				or isinstance(block, Expression)
				or isinstance(block, ExpressionSet)
				or isinstance(block, OpenEndedBlock) 
				or isinstance(block, SymmetricBlock)
				or isinstance(block, CatchAllBlock)
				or block.content is None
			):
				continue
			this.outFile.write(f"\n\tCLOSE_{block.name.upper()}[''] = ['CLOSE_EXPRESSION', 'CLOSE_{block.name.upper()}']")

		this.outFile.write("\n\n")

		this.outFile.close()

		logging.debug(f"Done writing to {this.outFileName}")