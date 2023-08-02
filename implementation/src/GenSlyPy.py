from elderlangdefinitions import Block, AbstractStructure, StrictStructure
import elderlangdefinitions
import eons

@eons.kind(eons.Functor)
def GenSlyPy(
	blocks = {},
	structures = eons.util.DotDict(),
	outFileName = "elder.grammar.py",
):
	
	blocks = []
	structures.abstract = []
	structures.strict = []

	for cls in elderlangdefinitions:
		if (isinstance(cls, Block)):
			blocks.append(cls())
		elif (isinstance(cls, AbstractStructure)):
			structures.abstract.append(cls())
		elif (isinstance(cls, StrictStructure)):
			structures.strict.append(cls())

	tokens = eons.util.DotDict()
	tokens.open = {}
	tokens.close = {}
	tokens.structural = {}

	for name,block in blocks.items():
		tokens.open[f"OPEN_{block.name.upper()}"] = fr"({'|'.join(block.openings)})"
		tokens.close[f"CLOSE_{block.name.upper()}"] = fr"({'|'.join(block.closings)})"

	blockRepresentations = [block.representation for block in blocks]

	for structure in (structures.abstract + structures.strict):
		possibleToken = structure.match
		for representation in blockRepresentations:
			possibleToken = possibleToken.replace(representation, '')
		if (len(possibleToken)):
			tokens.structural[structure.name.upper()] = possibleToken

	tokens.all = tokens.open
	tokens.all.update(tokens.close)
	tokens.all.update(tokens.structural)

	outFile = open(outFileName, 'w')
	outFile.write(f"""\
import elderlang

class ElderLexer(elderlang.Lexer):
	tokens = {{ {', '.join([t for t in tokens.all.keys()])} }}

	ignore = ' \\t'
	ignore_newline = '\\n+'

	# Extra action for newlines
	def ignore_newline(self, t):
		self.lineno += t.value.count('\\n')

	def error(self, t):
		print("Illegal character '%s'" % t.value[0])
		self.index += 1
""")
	
	for token,regex in tokens.all.items():
		outFile.write(f"\t{token} = r'{regex}'\n")

	outFile.close()