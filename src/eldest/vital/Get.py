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

		if (type(source) in [int, float, str, bool, list, dict]
			or isinstance(source, list)
			or isinstance(source, dict)
		):
			
			# For Python objects, the __eq__ method will assign to value, not to reference.
			# We want to modify the original object here.
			if (this.target == 'EQ'):
				if (isinstance(source, list)):
					source.clear()
					return source.extend
				elif (isinstance(source, dict)):
					source.clear()
					return source.update
				else:
					# TODO: What else can we do here?
					logging.warning(f"Cannot assign {source}: {type(source)} is immutable.")
					# Let's still return. Maybe we're wrong!
					return source.__eq__

			elif (this.target in this.executor.sanitize.operatorMap.keys()):
				return source.__getattribute__(this.executor.sanitize.operatorMap[this.target])

		return getattr(source, this.target)
