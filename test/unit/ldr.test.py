from elderlang.elderlang import ElderLexer, ElderParser
from pathlib import Path
import eons
import logging

ldrlxr = ElderLexer()
ldrpsr = ElderParser()

tests = [
	'op',
	'if',
	# 'hellowolf',
	# 'arrays',
]

ex = eons.Executor(name="Elder Language Tester")
ex()

testPath = str(Path(__file__).parent.absolute())

for test in tests:
	logging.critical(f"======================== {test} ========================")
	testFile = open(f'{testPath}/{test}.ldr', 'r')
	ldr = testFile.read()

	tokens = ldrlxr.tokenize(ldr)
	# [logging.info(t) for t in tokens]

	logging.critical(ldrpsr.parse(tokens))

	testFile.close()