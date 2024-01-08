from ..KEYWORD import KEYWORD
from ..EVAL import EVAL
from ..EXEC import EXEC

class NOT (KEYWORD):
	def __init__(this):
		super().__init__(name = "NOT")

		this.arg.kw.required.append('parameter')

	def Function(this):
		evaluated, unwrapped = EVAL(this.parameter)
		if (unwrapped):
			return not evaluated
		else:
			# TODO: this isn't quite right, but it shouldn't be a common case. Let's improve it once we know if we should default to True or False.
			return [not i for i in evaluated]
