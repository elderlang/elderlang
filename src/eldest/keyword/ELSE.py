from ..KEYWORD import KEYWORD
from ..EVAL import EVAL
from ..EXEC import EXEC

class ELSE (KEYWORD):
	def __init__(this):
		super().__init__(name = "ELSE")

		# this.arg.kw.required.append('IF')
		this.arg.kw.required.append('execution')
		

	def Function(this):
		this.IF = this.Fetch('IF', None, ['history'])
		if (this.IF is None):
			raise RuntimeError("ELSE keyword must be used after an IF keyword.")
		if (not this.IF.didExecute):
			EXEC(this.execution)