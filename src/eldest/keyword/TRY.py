from ..KEYWORD import KEYWORD
from ..EVAL import EVAL
from ..EXEC import EXEC

class TRY (KEYWORD):
	def __init__(this):
		super().__init__(name = "TRY")

		this.arg.kw.required.append('execution')

	def Function(this):
		try:
			EXEC(this.execution)
		except Exception as e:
			this.executor.exceptions.append((e,False))