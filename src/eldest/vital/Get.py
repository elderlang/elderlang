import eons
import types
from .SourceTargetFunctor import SourceTargetFunctor
from ..EVAL import EVAL
from ..EXEC import EXEC

class Get (SourceTargetFunctor):
	def __init__(this, name="Get"):
		super().__init__(name)

	def Function(this):
		if (isinstance(this.target, list)):
			this.target = this.target[0]
		# elif (isinstance(this.target, str)):
		# 	this.target = EVAL(this.target, unwrapReturn=True)[0]

		source = this.source
		if (isinstance(source, eons.Functor)):
			if (not source.isWarm):
				source.WarmUp()
			try:
				return getattr(source, this.target)
			except AttributeError:
				source = source()
		elif (isinstance(source, types.FunctionType) or isinstance(source, types.MethodType)):
			source = source()

		if (type(source) in [int, float, str, bool, list, dict] and this.target in this.executor.sanitize.operatorMap.keys()):
			return source.__getattribute__(this.executor.sanitize.operatorMap[this.target])

		return getattr(source, this.target)
