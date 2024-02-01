import eons
import types
from .SourceTargetFunctor import SourceTargetFunctor
from ..Sanitize import Sanitize
from ..EVAL import EVAL
from ..EXEC import EXEC

class Get (SourceTargetFunctor):
	def __init__(this, name="Get"):
		super().__init__(name)

	def Function(this):
		if (isinstance(this.target, list)):
			this.target = this.target[0]
		elif (isinstance(this.target, str)):
			this.target = EVAL(this.target, unwrapReturn=True)[0]

		source = this.source
		if (isinstance(source, types.FunctionType) or isinstance(source, types.MethodType)):
			source = source()
		if (isinstance(source, eons.Functor)):
			try:
				return getattr(source, this.target)
			except AttributeError:
				source = source()
		
		if (type(source) in [int, float, str, bool] and this.target in Sanitize.operatorMap.keys()):
			return source.__getattribute__(Sanitize.operatorMap[this.target])
		
		return getattr(source, this.target)
