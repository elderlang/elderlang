from ..KEYWORD import KEYWORD
from ..EVAL import EVAL
from ..EXEC import EXEC

class CATCH (KEYWORD):
	def __init__(this):
		super().__init__(name = "catch")

		this.arg.kw.required.append('parameter')
		this.arg.kw.required.append('execution')

	def Function(this):
		if (len(this.executor.exceptions) and this.executor.exceptions[-1][1] == False):
			if (eval(this.parameter) == this.executor.exceptions[-1][0]):
				this.executor.exceptions.pop()
				EXEC(this.execution)