from ..KEYWORD import KEYWORD
from ..EVAL import EVAL
from ..EXEC import EXEC
from .LOOP import LOOP

class BREAK (KEYWORD):
	def __init__(this):
		super().__init__(name = "BREAK")

	def Function(this):
		loop = None
		stack = this.executor.stack.copy()
		stack.reverse()
		for name, object in stack:
			if (isinstance(object, LOOP)):
				loop = object
				break

		if (loop is None):
			raise RuntimeError("Cannot break outside of loop")

		loop.BREAK = True
		loop.context.Halt()