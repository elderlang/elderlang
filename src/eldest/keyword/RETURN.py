from ..KEYWORD import KEYWORD
from ..EVAL import EVAL
from ..EXEC import EXEC
from ..type.FUNCTOR import FUNCTOR

class RETURN (KEYWORD):
	def __init__(this):
		super().__init__(name = "RETURN")

		this.arg.kw.required.append('parameter')
		this.arg.mapping.append('parameter')

	def Function(this):
		toHalt = None
		for i, tup in enumerate(this.executor.stack):
			if (isinstance(tup[1], FUNCTOR)):
				toHalt = this.executor.stack[i-1][1] # the exec for the current functor.
		if (toHalt is None):
			raise RuntimeError(f"RETURN called outside of a functor.")
		toHalt.context.result.data.returned = this.parameter
		toHalt.context.Halt()