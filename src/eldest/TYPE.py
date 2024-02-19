import eons
import types
import logging
from .EldestFunctor import EldestFunctor

class TYPE(EldestFunctor):
	def __init__(this, name=eons.INVALID_NAME(), value=None):
		super().__init__(name)

		this.value = value
		this.isBasicType = True
		this.default = None
		this.needs.typeAssignment = True
		this.feature.cloneOnCall = False
		this.feature.track = True

	# This is generally what other types will use. Those that don't can override it.
	def Function(this):
		return this.value
	
	# IMPORTANT: Children should override this.
	# Return whether or not the value in *this should be set.
	def SomehowSet(this, value):
		if (this.isBasicType):
			this.value = value
			return True
		return False
	
	def IMPL_EQL(this, other):
		this = other

	def EQ(this, other):
		other = this.PossiblyReduceOther(other)
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
					for key, val in surrogate.__dict__().items():
						if (key in excludeDictKeys):
							continue
						try:
							this.__dict__.update({key: val})
						except:
							logging.warning(f"Unable to update the dict of {this.name} ({type(this)}).")

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
			if (this.isBasicType):
				this.value = this.PossiblyReduceOther(other)
			else:
				this.IMPL_EQ(other)

		return this

	def GT(this, other):
		return this.PossiblyReduceThis() > this.PossiblyReduceOther(other)

	def LT(this, other):
		return this.PossiblyReduceThis() < this.PossiblyReduceOther(other)

	def EQEQ(this, other):
		return this.PossiblyReduceThis() == this.PossiblyReduceOther(other)
	
	def NOTEQ(this, other):
		return this.PossiblyReduceThis() != this.PossiblyReduceOther(other)

	def GTEQ(this, other):
		return this.PossiblyReduceThis() >= this.PossiblyReduceOther(other)

	def LTEQ(this, other):
		return this.PossiblyReduceThis() <= this.PossiblyReduceOther(other)

	def POW(this, other):
		return pow(this.PossiblyReduceThis(), this.PossiblyReduceOther(other))

	def AND(this, other):
		return this.PossiblyReduceThis() and this.PossiblyReduceOther(other)

	def ANDAND(this, other):
		return this.AND(other)

	def OR(this, other):
		return this.PossiblyReduceThis() or this.PossiblyReduceOther(other)

	def OROR(this, other):
		return this.OR(other)

	def PLUS(this, other):
		return this.PossiblyReduceThis() + this.PossiblyReduceOther(other)

	def MINUS(this, other):
		return this.PossiblyReduceThis() - this.PossiblyReduceOther(other)

	def TIMES(this, other):
		return this.PossiblyReduceThis() * this.PossiblyReduceOther(other)

	def DIVIDE(this, other):
		return this.PossiblyReduceThis() / this.PossiblyReduceOther(other)

	def PLUSEQ(this, other):
		this.SomehowSet(this.PossiblyReduceThis() + this.PossiblyReduceOther(other))
		return this

	def MINUSEQ(this, other):
		this.SomehowSet(this.PossiblyReduceThis() - this.PossiblyReduceOther(other))
		return this

	def TIMESEQ(this, other):
		this.SomehowSet(this.PossiblyReduceThis() * this.PossiblyReduceOther(other))
		return this

	def DIVIDEEQ(this, other):
		this.SomehowSet(this.PossiblyReduceThis() / this.PossiblyReduceOther(other))
		return this

	def MOD(this, other):
		return this.PossiblyReduceThis() % this.PossiblyReduceOther(other)
	
	def MODEQ(this, other):
		this.SomehowSet(this.PossiblyReduceThis() % this.PossiblyReduceOther(other))
		return this
	
	def size(this):
		return len(this)

	def length(this):
		return this.size()

	def PossiblyReduceOther(this, other):
		if (isinstance(other, types.FunctionType) or isinstance(other, types.MethodType)):
			other = other()
		elif (isinstance(other, TYPE) and other.isBasicType):
			other = other.value
		elif (this.isBasicType and isinstance(other, eons.Functor)):
			other = other()
		return other

	def PossiblyReduceThis(this):
		ret = this
		while (True):
			try:
				if (isinstance(this, POINTER)): # POINTER cannot be imported, but that's fine. Just assume it exists.
					ret = ret.value
				elif (ret.isBasicType):
					ret = ret.value
				else:
					break
			except AttributeError:
				break

		return ret

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
