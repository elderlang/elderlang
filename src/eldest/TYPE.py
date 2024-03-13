import eons
import types
import logging
from .EldestFunctor import EldestFunctor

supportedBuiltins = [
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
	# "__eq__", # cursed.
	"__ne__",
	"__gt__",
	"__ge__",
	"__bool__",
	"__str__",
	"__int__",
	"__float__",
	"__len__",
]

class TYPE(EldestFunctor):
	def __init__(this, name=eons.INVALID_NAME(), value=None):
		super().__init__(name)

		this.value = value
		this.useValue = True
		this.default = None
		this.needs.typeAssignment = True
		this.feature.cloneOnCall = False
		this.feature.track = True
		this.feature.sequential = False

		this.fetch.attr.use = []

		# Does not work. See ArithmeticFunctor, below.
		# for name in supportedBuiltins:
		# 	setattr(getattr(this, name).__func__, 'epidef', this)
		# 	setattr(this, name, types.MethodType(getattr(this, name), this))

	# This is generally what other types will use. Those that don't can override it.
	def Function(this):
		return this.value
	
	# IMPORTANT: Children should override this.
	# Return whether or not the value in *this should be set.
	def SomehowSet(this, value):
		if (this.useValue):
			this.value = value
			return True
		return False
	
	def IMPL_EQ(this, other):
		this = other

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
			elif (isinstance(other, eons.Functor)):
				surrogate = POINTER.to(other)

			if (surrogate is not None):
				this.AssignTo(surrogate)

				logging.info(f"Making {this.name} a {surrogate.name} ({surrogate.__class__}) with value {other}")
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
			if (this.useValue):
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

	def __eq__(this, other):
		reduction = this.PossiblyReduceThis()
		if (id(reduction) == id(this)):
			return super().__eq__(other)
		return reduction == this.PossiblyReduceOther(other)

	def PossiblyReduceOther(this, other):
		ret = other
		while(True):
			try:
				if (isinstance(ret, types.FunctionType) or isinstance(ret, types.MethodType)):
					ret = ret()
				elif (isinstance(ret, POINTER) or (isinstance(ret, TYPE) and ret.useValue)):
					ret = ret.value
				elif (this.useValue and isinstance(ret, eons.Functor)):
					ret = ret()
				else:
					break
			except:
				break
		return ret

	def PossiblyReduceThis(this):
		ret = this
		while (True):
			try:
				if (isinstance(ret, POINTER)): # POINTER cannot be imported, but that's fine. Just assume it exists.
					ret = ret.value
				elif (ret.useValue):
					ret = ret.value
				else:
					break
			except AttributeError:
				break

		return ret

# This approach does not work.
# built in methods are class-based, not object-based, so persisting values like epidef does so at a class level.
#
# class ArithmeticFunctor(eons.Functor):
# 	def __init__(this, name=eons.INVALID_NAME()):
# 		super().__init__(name)

# 		this.feature.autoReturn = False
# 		this.feature.mapArgs = False
# 		this.feature.sequential = False
# 		this.feature.track = False

# 		this.abort.function = False

# 	def PopulatePrecursor(this):
# 		try:
# 			if (inspect.isclass(this.epidef)):
# 				this.epidef = None

# 			if (this.epidef is None):
# 				logging.warning(f"Failed to setup {this.name}.")
# 				if (not inspect.isclass(this.args[0])):
# 					this.epidef = this.args[0]

# 			if (not this.executor):
# 				this.executor = this.epidef.executor
		
# 		except Exception as e:
# 			logging.warning(e)
# 			this.abort.function = True

# 	def Function(this):
# 		if (this.epidef is None):
# 			return this.abort.returnWhenAborting.function

# 		if (not hasattr(this.epidef, 'PossiblyReduceThis')):
# 			logging.warning(f"epidef {this.epidef} lacks PossiblyReduceThis")
# 			return this.abort.returnWhenAborting.function

# 		operateOn = this.epidef.PossiblyReduceThis()
# 		operation = getattr(operateOn, this.name)
# 		if (id(operateOn) == id(this)):
# 			return getattr(this.epidef.parent, this.name)(*this.args[1:])

# 		return operation(*this.args[1:])

# 	# Add disarmed compatibility with eons.Method.
# 	def UpdateSource(this):
# 		return

def CreateArithmeticFunction(functionName):
	# return types.MethodType(ArithmeticFunctor(functionName), TYPE)
	return lambda this, *args: getattr(this.PossiblyReduceThis(), functionName)(*args)

for name in supportedBuiltins:
	# DOES NOT WORK
	# Apparently casts like str() call essentially this.__class__.__str__(this), rather than this.__str__().
	# This makes this approach yield METHOD PENDING POPULATION errors all over the place.
	# eons.PrepareClassMethod(TYPE, name, ArithmeticFunctor(name))

	setattr(TYPE, name, CreateArithmeticFunction(name))

# We only handle error cases for basic type casts atm.
# Operations like len() should always be called on an object, not the class (so should everything else but python is buggy).
# TYPE.__str__.abort.returnWhenAborting.function = 'ERROR: STR CALLED WITHOUT OBJECT'
# TYPE.__int__.abort.returnWhenAborting.function = 0
# TYPE.__float__.abort.returnWhenAborting.function = 0.0
# TYPE.__bool__.abort.returnWhenAborting.function = False
