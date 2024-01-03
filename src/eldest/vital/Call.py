import eons
from .SourceTargetFunctor import SourceTargetFunctor
from ..EVAL import EVAL
from ..EXEC import EXEC

class Call (SourceTargetFunctor):
	def __init__(this, name="Call"):
		super().__init__(name)

	def Function(this):
		return this.source(EVAL(this.target))