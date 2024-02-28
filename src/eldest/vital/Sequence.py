import eons
from .SourceTargetFunctor import SourceTargetFunctor
from ..EVAL import EVAL
from ..EXEC import EXEC
from ..type.FUNCTOR import FUNCTOR

class Sequence (SourceTargetFunctor):
	def __init__(this, name="Sequence"):
		super().__init__(name)

	def Function(this):

		# FIXME: This is not the right place for this patch. So far as I can tell, next should NEVER be set to None, only emply list.
		if (isinstance(this.source, FUNCTOR) and this.source.next is None):
			this.source.next = []

		if (not this.source.warm):
			this.source.WarmUp(executor=this.executor)

		return this.source.__truediv__(EVAL(this.target, unwrapReturn=True, shouldAttemptInvokation=False)[0])
