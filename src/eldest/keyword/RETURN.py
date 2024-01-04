from ..KEYWORD import KEYWORD
from ..EVAL import EVAL
from ..EXEC import EXEC

class RETURN (KEYWORD):
	def __init__(this):
		super().__init__(name = "RETURN")

		this.arg.kw.required.append('parameter')
		this.arg.mapping.append('parameter')

	def Function(this):
		this.context.result.data.returned = this.parameter
		this.context.Halt()