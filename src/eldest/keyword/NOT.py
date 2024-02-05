from ..KEYWORD import KEYWORD
from ..EVAL import EVAL
from ..EXEC import EXEC

class NOT (KEYWORD):
	def __init__(this):
		super().__init__(name = "NOT")

		this.arg.kw.required.append('parameter')
		this.arg.mapping.append('parameter')

	def Function(this):
		if (isinstance(this.parameter, bool)):
			return not this.parameter

		unwrapped = True
		if (isinstance(this.parameter, str)):
			this.parameter, unwrapped = EVAL([this.parameter])
		elif(isinstance(this.parameter, list)):
			unwrapped = False
		
		if (unwrapped):
			return not this.parameter
		else:
			# TODO: this isn't quite right, but it shouldn't be a common case. Let's improve it once we know if we should default to True or False.
			return [not i for i in this.parameter]
