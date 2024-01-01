from .LOOP import LOOP
from ..EVAL import EVAL
from ..EXEC import EXEC

class WHILE (LOOP):
	def __init__(this):
		super().__init__(name = "while")

		this.arg.kw.required.append('parameter')
		this.arg.kw.required.append('execution')

	def Function(this):
		while (EVAL(this.parameter) and not this.BREAK):
			EXEC(this.execution)
