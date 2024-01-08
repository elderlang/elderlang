from ..KEYWORD import KEYWORD
from ..EVAL import EVAL
from ..EXEC import EXEC
from .LOOP import LOOP

class BREAK (KEYWORD):
	def __init__(this):
		super().__init__(name = "BREAK")

	def Function(this):
		loop = this.Fetch(LOOP, None, ['stack_type'])

		if (loop is None):
			raise RuntimeError("Cannot break outside of loop")

		loop.BREAK = True
		loop.context.Halt()