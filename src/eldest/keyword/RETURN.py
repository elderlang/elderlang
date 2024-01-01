from ..KEYWORD import KEYWORD
from ..EVAL import EVAL
from ..EXEC import EXEC

class RETURN (KEYWORD):
	def __init__(this):
		super().__init__(name = "return")

		this.arg.kw.required.append('parameter')

	def Function(this):
		this.context.result.data.returned = EVAL(this.parameter)
		this.context.Halt()