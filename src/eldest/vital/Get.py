import eons
from .SourceTargetFunctor import SourceTargetFunctor
from ..EVAL import EVAL
from ..EXEC import EXEC

class Get (SourceTargetFunctor):
	def __init__(this, name="Get"):
		super().__init__(name)

	def Function(this):
		retrieved = [getattr(this.source, t) for t in this.target]
		return retrieved[0] if len(retrieved) == 1 else retrieved
