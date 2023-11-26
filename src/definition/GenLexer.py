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
		this.syntax.abstract = []
		this.syntax.strict = []
		this.defaultBlocks = []
		this.defaultBlockSets = []
		this.catchAllBlock = None

		for name in summary.blocks:
			toAppend = eons.SelfRegistering(name)
			this.blocks.append(toAppend)
			if (isinstance(toAppend, CatchAllBlock)):
				this.catchAllBlock = toAppend
			elif (isinstance(toAppend, DefaultBlock)):
				this.defaultBlocks.append(toAppend)
			elif (isinstance(toAppend, DefaultBlockSet)):
				this.defaultBlockSets.append(toAppend)
		
		for name in summary.syntax.abstract:
			this.syntax.abstract.append(eons.SelfRegistering(name))
		
		for name in summary.syntax.strict:
			this.syntax.strict.append(eons.SelfRegistering(name))

		this.tokens = eons.util.DotDict()
		this.tokens.open = {}
		this.tokens.close = {}
		this.tokens.syntactic = {}
		this.tokens.excludeFromCatchAll = []

		for block in this.blocks:
			block.WarmUp(executor = this.executor, precursor = None)
			
			tokenSources = {'openings': 'open', 'closings': 'close'}

			if (isinstance(block, DefaultBlock)):
				continue
			elif (isinstance(block, OpenEndedBlock)):
				del tokenSources['closings']
			elif (isinstance(block, CatchAllBlock)):
				continue

			for source, name in tokenSources.items():
				matches = eval(f"block.{source}")
				for emptyMatch in [r'^', r'$']:
					try:
						matches.remove(emptyMatch)
					except:
						pass
				if (len(matches)):
					blockName =f"{name}_{block.name}".upper()
					this.tokens[name][blockName] = fr"({'|'.join(matches)})"
					if ("all.catch.block" in block.exclusions):
						this.tokens.excludeFromCatchAll.append(blockName)
		
		# NOTE: "Openings" function as "closings" for the DefaultBlock only.
		# For example, start(expression); open(next_expression) // ; closes the first, even though it opens the second.
		this.defaultBlock = eons.SelfRegistering(summary.defaultBlock)
		this.defaultBlock.WarmUp(executor = this.executor, precursor = None)
		this.tokens['close'][f"CLOSE_{this.defaultBlock.name.upper()}"] = fr"({'|'.join(this.defaultBlock.openings)})"

		for syntax in this.syntax.abstract:
			syntax.WarmUp(executor = this.executor, precursor = None)
			# Nothing to do yet, but everything needs to be warm before we pass *this off to the Parser.

		for syntax in this.syntax.strict:
			syntax.WarmUp(executor = this.executor, precursor = None)
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

		this.tokens.all = {
			# Builtins
			'SPACE': r' +',
		}
		this.tokens.all.update(this.tokens.open)
		this.tokens.all.update(this.tokens.close)
		this.tokens.all.update(this.tokens.syntactic)

		this.tokens.all[summary.catchAllBlock.upper()] = fr"[{''.join(this.catchAllBlock.specialStarts)}]?(?:(?!{'|'.join([v[1:-1] for k, v in this.tokens.all.items() if len(v) > 2 and not k in this.tokens.excludeFromCatchAll])})\S)+"

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
	tokens = {{ {', '.join([t for t in this.tokens.all.keys()])} }}

	ignore = '\\t+'

	def error(self, t):
		print("Illegal character '%s'" % t.value[0])
		self.index += 1
""")
	
		for token,regex in this.tokens.all.items():
			this.outFile.write(f"\t{token} = r'{regex}'\n")

		this.outFile.close()

		logging.debug(f"Done writing to {this.outFileName}")