from .LOOP import LOOP
from ..EVAL import EVAL
from ..EXEC import EXEC

class WHILE (LOOP):
	def __init__(this):
		super().__init__(name = "WHILE")

		this.arg.kw.required.append('parameter')
		this.arg.kw.required.append('execution')

		this.arg.mapping.append('parameter')
		this.arg.mapping.append('execution')

	def Function(this):
		while (EVAL(this.parameter, unwrapReturn=True)[0] and not this.BREAK):
			EXEC(this.execution)
