import logging

logging.basicConfig(level=logging.DEBUG)

import elderlangdefinitions
import eons

ex = eons.Executor(name="Elder Language Generator")
ex()
# ex.RegisterAllClassesInDirectory('/home/eons/.eons/constellatus/registry')
ex.Execute('GenLexer')
