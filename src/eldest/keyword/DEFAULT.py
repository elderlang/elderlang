from ..KEYWORD import KEYWORD
from ..EVAL import EVAL
from ..EXEC import EXEC

class DEFAULT (KEYWORD):
	def __init__(this):
		super().__init__(name = "DEFAULT")

		this.arg.kw.required.append('switch')
		this.arg.kw.required.append('execution')

	def Function(this):
		if (this.switch.matched is None):
			this.switch.matched = this
			EXEC(this.execution)