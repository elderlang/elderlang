from ..KEYWORD import KEYWORD
from ..EVAL import EVAL
from ..EXEC import EXEC

class CASE (KEYWORD):
	def __init__(this):
		super().__init__(name = "CASE")

		this.arg.kw.required.append('condition')
		this.arg.kw.required.append('execution')
		this.arg.kw.required.append('SWITCH')

	def Function(this):
		if (this.condition == this.SWITCH.condition):
			this.SWITCH.matched = this
			EXEC(this.execution)