from ..KEYWORD import KEYWORD
from ..EVAL import EVAL
from ..EXEC import EXEC
from .LOOP import LOOP

class CONTINUE (KEYWORD):
	def __init__(this):
		super().__init__(name = "CONTINUE")

	def Function(this):
		loop = this.Fetch(LOOP, None, ['stack_type'])

		if (loop is None):
			raise RuntimeError("Cannot continue outside of loop")

		loop.context.Halt()