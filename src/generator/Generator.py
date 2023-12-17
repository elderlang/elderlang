import logging

logging.basicConfig(level=logging.DEBUG)

import elderlangdefinitions
import eons

ex = eons.Executor(name="Elder Language Generator")
ex()
lexer = ex.Execute('GenLexer')
parser = ex.Execute('GenParser', gen_lexer=lexer)
