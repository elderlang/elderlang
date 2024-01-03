from ..KEYWORD import KEYWORD
from ..EVAL import EVAL
from ..EXEC import EXEC

class ELSE (KEYWORD):
	def __init__(this):
		super().__init__(name = "ELSE")

		this.arg.kw.required.append('IF')
		this.arg.kw.required.append('execution')
		

	def Function(this):
		if (not this.IF.didExecute):
			EXEC(this.execution)