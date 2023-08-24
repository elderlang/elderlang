from elderlang import ElderLexer

ldrlxr = ElderLexer()

hellowolfFile = open('./hellowolf.ldr', 'r')
hellowolf = hellowolfFile.read()

for tok in ldrlxr.tokenize(hellowolf):
    print(tok)

hellowolfFile.close()