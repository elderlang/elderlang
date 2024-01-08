import eons
import types
import logging
from .vital.Call import Call
from .vital.Type import Type
from .EldestFunctor import EldestFunctor

class TYPE(EldestFunctor):
	def __init__(this, name=eons.INVALID_NAME(), value=None):
		super().__init__(name)

		this.value = value
		this.isBasicType = True
		this.default = None
		this.needs.typeAssignment = True
		this.feature.cloneOnCall = False

	# This is generally what other types will use. Those that don't can override it.
	def Function(this):
		return this.value

	def EQ(this, other):
		valueSet = False

		if (this.needs.typeAssignment):
			surrogate = None
			if (isinstance(other, bool)):
				surrogate = BOOL()
			elif (isinstance(other, int)):
				surrogate = INT()
			elif (isinstance(other, float)):
				surrogate = FLOAT()
			elif (isinstance(other, str)):
				surrogate = STRING()
			elif (isinstance(other, list)
		 		or isinstance(other, tuple)
				or isinstance(other, set)
				or isinstance(other, dict)
			):
				surrogate = CONTAINER()

			if (surrogate is not None):
				this.__class__ = surrogate.__class__

				excludeDictKeys = [
					'initialized',
					'name',
					'executor',
					'precursor',
					'next',
				]

				# TODO: WTF??
				try:
					for key, val in surrogate.__dict__.items():
						if (key in excludeDictKeys):
							continue
						try:
							this.__dict__[key] = surrogate.__dict__[key]
						except:
							logging.warning(f"Unable to set {this.name} ({type(this)}).{key} to {val}")
				except:
					exclusions = {}
					for key in excludeDictKeys:
						exclusions[key] = this.__dict__[key]
					try:
						this.__dict__.update(surrogate.__dict__())
					except:
						logging.warning(f"Unable to update the dict of {this.name} ({type(this)}).")
					this.__dict__.update(exclusions)

				logging.info(f"Making {this.name} a {surrogate.name} with value {other}")
				this.value = other
				valueSet = True
				this.needs.typeAssignment = False
			else:
				# It's complex, so we'll leave it as a functor.
				this.needs.typeAssignment = False

		if (this.IsCurrentlyInTypeParameterBlock()):
			logging.info(f"Setting default value of {this.name} to {other}")
			this.default = other
			valueSet = True

		if (not valueSet):
			logging.info(f"Setting {this.name} to {other}")
			this = other

		return this

	def GT(this, other):
		other = this.PossiblyReduceOther(other)
		return this > other

	def LT(this, other):
		other = this.PossiblyReduceOther(other)
		return this < other

	def EQEQ(this, other):
		other = this.PossiblyReduceOther(other)
		return this == other
	
	def NOTEQ(this, other):
		other = this.PossiblyReduceOther(other)
		return this != other

	def GTEQ(this, other):
		other = this.PossiblyReduceOther(other)
		return this >= other

	def LTEQ(this, other):
		other = this.PossiblyReduceOther(other)
		return this <= other

	def POW(this, other):
		other = this.PossiblyReduceOther(other)
		return pow(this, other)

	def AND(this, other):
		other = this.PossiblyReduceOther(other)
		return this and other

	def ANDAND(this, other):
		other = this.PossiblyReduceOther(other)
		return this.AND(other)

	def OR(this, other):
		other = this.PossiblyReduceOther(other)
		return this or other

	def OROR(this, other):
		other = this.PossiblyReduceOther(other)
		return this.OR(other)

	def PLUS(this, other):
		other = this.PossiblyReduceOther(other)
		return this + other

	def MINUS(this, other):
		other = this.PossiblyReduceOther(other)
		return this - other

	def TIMES(this, other):
		other = this.PossiblyReduceOther(other)
		return this * other

	def DIVIDE(this, other):
		other = this.PossiblyReduceOther(other)
		return this / other

	def PLUSEQ(this, other):
		other = this.PossiblyReduceOther(other)
		this = this + other
		return this

	def MINUSEQ(this, other):
		other = this.PossiblyReduceOther(other)
		this = this - other
		return this

	def TIMESEQ(this, other):
		other = this.PossiblyReduceOther(other)
		this = this * other
		return this

	def DIVIDEEQ(this, other):
		other = this.PossiblyReduceOther(other)
		this = this / other
		return this

	def MOD(this, other):
		other = this.PossiblyReduceOther(other)
		return this % other
	
	def MODEQ(this, other):
		other = this.PossiblyReduceOther(other)
		this = this % other
		return this
	
	def size(this):
		return len(this)

	def length(this):
		return this.size()
	
	def PossiblyReduceOther(this, other):
		if (isinstance(other, types.FunctionType) or isinstance(other, types.MethodType)):
			other = other()
		elif (this.isBasicType and isinstance(other, eons.Functor)):
			other = other()
		elif (isinstance(other, TYPE) and other.isBasicType):
			other = other.value
		return other
	

def CreateArithmeticFunction(functionName):
	return lambda this, *args: getattr(this.value, functionName)(*args)

for name in [
	"__add__",
	"__sub__",
	"__mul__",
	"__matmul__",
	"__truediv__",
	"__floordiv__",
	"__mod__",
	"__divmod__",
	"__pow__",
	"__lshift__",
	"__rshift__",
	"__and__",
	"__xor__",
	"__or__",
	"__iadd__",
	"__isub__",
	"__imul__",
	"__imatmul__",
	"__itruediv__",
	"__ifloordiv__",
	"__imod__",
	"__ipow__",
	"__ilshift__",
	"__irshift__",
	"__iand__",
	"__ixor__",
	"__ior__",
	"__lt__",
	"__le__",
	"__eq__",
	"__ne__",
	"__gt__",
	"__ge__",
	"__bool__",
	"__str__",
	"__int__",
	"__float__",
	"__len__",
]:
	setattr(TYPE, name, CreateArithmeticFunction(name))
