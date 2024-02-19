from elderlang.elderlang import ELDERLANG
from pathlib import Path
import eons
import logging

elder = ELDERLANG()
commander = eons.StandardFunctor()
commander.WarmUp(executor = elder)

tests = [
	'op',
	'if',
	'hellowolf',
	# 'arrays',
	'caller'
]

testPath = str(Path(__file__).parent.absolute())

for test in tests:
	logging.critical(f"======================== {test} Tokenized ========================")
	testFileName = f"{testPath}/{test}.ldr"
	testFile = open(testFileName, 'r')
	ldr = testFile.read()
	testFile.close()

	tokens = elder.lexer.tokenize(ldr)
	[logging.info(t) for t in tokens]
	# logging.critical(f"======================== {test} Parsed ========================")
	# logging.info(elder.parser.parse(elder.lexer.tokenize(ldr)))
	logging.critical(f"======================== {test} Executed ========================")
	logging.info(commander.RunCommand(f"elder {testFileName}", saveout=True, raiseExceptions=False))
	logging.critical(f"================================================")
