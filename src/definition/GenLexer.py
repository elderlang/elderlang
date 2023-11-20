import eons
import logging
import re
from .Blocks import *
from .Summary import summary

class GenLexer(eons.Functor):

	def	__init__(this, name = "SlyPy Parser Generator"):
		super().__init__(name)

		this.optionalKWArgs['outFileName'] = "lexer.py"
	
	def Function(this):
		this.blocks = []
		this.syntax = eons.util.DotDict()
		this.syntax.abstract = []
		this.syntax.strict = []
		this.catchAllBlock = None

		for name in summary.blocks:
			toAppend = eons.SelfRegistering(name)
			this.blocks.append(toAppend)
			if (isinstance(toAppend, CatchAllBlock)):
				this.catchAllBlock = toAppend
		
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
			block.WarmUp(executor = this.executor, precursor = this)
			
			tokenSources = {'openings': 'open', 'closings': 'close'}

			if (isinstance(block, OpenEndedBlock)):
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
					if (block.excludeFromCatchAll):
						this.tokens.excludeFromCatchAll.append(blockName)

		blockRepresentations = [block.representation for block in this.blocks]

		for syntax in this.syntax.strict:
			syntax.WarmUp(executor = this.executor, precursor = this)
			possibleToken = syntax.match
			for representation in blockRepresentations:
				possibleToken = possibleToken.replace(representation, '')
			for builtin in summary.builtins:
				possibleToken = possibleToken.replace(builtin, '')
			possibleToken = fr"({possibleToken})"
			if (
				len(possibleToken) > 2
				and possibleToken not in this.tokens.syntactic.values()
			):
				this.tokens.syntactic[syntax.name.upper()] = possibleToken
				if (syntax.excludeFromCatchAll):
					this.tokens.excludeFromCatchAll.append(syntax.name.upper())
			else:
				logging.info(f"Syntax {syntax.name} has no matchable tokens.")

		this.tokens.all = this.tokens.open
		this.tokens.all.update(this.tokens.close)
		this.tokens.all.update(this.tokens.syntactic)

		this.tokens.all[summary.catchAllBlock.upper()] = fr"[{''.join(this.catchAllBlock.specialStarts)}]?(?:(?!{'|'.join([v[1:-1] for k, v in this.tokens.all.items() if len(v) > 2 and not k in this.tokens.excludeFromCatchAll])}).)+"

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