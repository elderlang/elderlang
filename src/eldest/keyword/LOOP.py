import eons
from ..KEYWORD import KEYWORD
from ..EVAL import EVAL
from ..EXEC import EXEC

class LOOP (KEYWORD):
	def __init__(this, name = eons.INVALID_NAME()):
		super().__init__(name)
	
	def BeforeFunction(this):
		this.BREAK = False
