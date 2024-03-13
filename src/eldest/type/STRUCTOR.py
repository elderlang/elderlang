import eons
from .FUNCTOR import FUNCTOR
from ..EVAL import EVAL
from ..EXEC import EXEC
from ..HOME import HOME

# Structors are Functors that lack an execution block.
class STRUCTOR(FUNCTOR):
	def __init__(this, name=eons.INVALID_NAME(), value=None):
		super().__init__(name)

		this.feature.autoReturn = True
		this.feature.stayWarm = True
