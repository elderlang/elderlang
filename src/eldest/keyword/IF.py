from ..KEYWORD import KEYWORD
from ..EVAL import EVAL
from ..EXEC import EXEC

class IF (KEYWORD):
	def __init__(this):
		super().__init__(name = "if")

		this.arg.kw.required.append('condition')
		this.arg.kw.required.append('execution')

	def Function(this):
		this.didExecute = False
		if (this.condition):
			this.didExecute = True
			EXEC(this.execution)