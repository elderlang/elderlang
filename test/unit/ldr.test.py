from elderlang.elderlang import ElderLexer, ElderParser
from pathlib import Path

ldrlxr = ElderLexer()
ldrpsr = ElderParser()

tests = [
	'if',
	'hellowolf',
	'arrays',
]

testPath = str(Path(__file__).parent.absolute())

for test in tests:
	print(f"======================== {test} ========================")
	testFile = open(f'{testPath}/{test}.ldr', 'r')
	ldr = testFile.read()

	tokens = ldrlxr.tokenize(ldr)

	for tok in tokens:
		print(tok)

	ldrpsr.parse(tokens)

	testFile.close()