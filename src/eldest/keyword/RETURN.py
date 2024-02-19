import logging
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
				logging.debug(f"Returning from {tup[1]}.name ({tup[1]}).")
				toHalt = this.executor.stack[i-1][1] # the exec for the current functor.
				break
		if (toHalt is None):
			raise RuntimeError(f"RETURN called outside of a functor.")
		
		toReturn = this.parameter #EVAL(this.parameter, unwrapReturn=True)[0]

		this.result.data.returned = toReturn
		toHalt.result.data.returned = toReturn
		toHalt.Halt()