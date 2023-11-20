from elderlang.elderlang import ElderLexer

ldrlxr = ElderLexer()

tests = [
	'if',
	'hellowolf',
	'arrays',
]

for test in tests:
    print(f"======================== {test} ========================")
    testFile = open(f'./{test}.ldr', 'r')
    ldr = testFile.read()

    for tok in ldrlxr.tokenize(ldr):
        print(tok)

    testFile.close()