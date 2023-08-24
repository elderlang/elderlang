import eons
import logging
import inspect
from .Blocks import *
from .Summary import summary

class GenLexer(eons.Functor):

	def	__init__(this, name = "SlyPy Parser Generator"):
		super().__init__(name)

		this.optionalKWArgs['outFileName'] = "lexer.py"
	
	def Function(this):
		this.blocks = []
		this.structure = eons.util.DotDict()
		this.structure.abstract = []
		this.structure.strict = []

		for name in summary.blocks:
			this.blocks.append(eons.SelfRegistering(name))
		
		for name in summary.structure.abstract:
			this.structure.abstract.append(eons.SelfRegistering(name))
		
		for name in summary.structure.strict:
			this.structure.strict.append(eons.SelfRegistering(name))

		this.tokens = eons.util.DotDict()
		this.tokens.open = {}
		this.tokens.close = {}
		this.tokens.structural = {}

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
					this.tokens[name][f"{name}_{block.name}".upper()] = fr"({'|'.join(matches)})"

		blockRepresentations = [block.representation for block in this.blocks]

		for structure in this.structure.strict:
			structure.WarmUp(executor = this.executor, precursor = this)
			possibleToken = structure.match
			for representation in blockRepresentations:
				possibleToken = possibleToken.replace(representation, '')
			for builtin in summary.builtins:
				possibleToken = possibleToken.replace(builtin, '')
			if (len(possibleToken)):
				this.tokens.structural[structure.name.upper()] = possibleToken

		this.tokens.all = this.tokens.open
		this.tokens.all.update(this.tokens.close)
		this.tokens.all.update(this.tokens.structural)

		this.tokens.all[summary.catchAllBlock.upper()] = fr"(?!{'|'.join([v[1:-1] for v in this.tokens.all.values() if len(v) > 2])})\S+"

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

	ignore = ' \\t'
	ignore_newline = '\\n+'

	# Extra action for newlines
	def ignore_newline(self, t):
		self.lineno += t.value.count('\\n')

	def error(self, t):
		print("Illegal character '%s'" % t.value[0])
		self.index += 1
""")
	
		for token,regex in this.tokens.all.items():
			this.outFile.write(f"\t{token} = r'{regex}'\n")

		this.outFile.close()

		logging.debug(f"Done writing to {this.outFileName}")