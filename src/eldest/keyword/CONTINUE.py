from ..KEYWORD import KEYWORD
from ..EVAL import EVAL
from ..EXEC import 
from .LOOP import LOOP

class CONTINUE (KEYWORD):
	def __init__(this):
		super().__init__(name = "CONTINUE")

	def Function(this):
		loop = None
		for name, object in this.executor.stack.reverse():
			if (isinstance(object, LOOP)):
				loop = object
				break

		if (loop is None):
			raise RuntimeError("Cannot continue outside of loop")

		loop.context.Halt()