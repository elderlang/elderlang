from ..KEYWORD import KEYWORD
from ..EVAL import EVAL
from ..EXEC import EXEC

class DEFAULT (KEYWORD):
	def __init__(this):
		super().__init__(name = "default")

		this.arg.kw.required.append('SWITCH')
		this.arg.kw.required.append('execution')

	def Function(this):
		if (this.SWITCH.matched is None):
			this.SWITCH.matched = this
			EXEC(this.execution)