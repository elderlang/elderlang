from ..KEYWORD import KEYWORD
from ..EVAL import EVAL
from ..EXEC import EXEC

class NOT (KEYWORD):
	def __init__(this):
		super().__init__(name = "NOT")

		this.arg.kw.required.append('parameter')

	def Function(this):
		return not EVAL(this.parameter)
