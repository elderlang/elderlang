import eons
from .SourceTargetFunctor import SourceTargetFunctor
from ..EVAL import EVAL
from ..EXEC import EXEC

class Sequence (SourceTargetFunctor):
	def __init__(this, name="Sequence"):
		super().__init__(name)

	def Function(this):
		return this.source.__truediv__(EVAL(this.target))
