import eons
from .EldestFunctor import EldestFunctor

class TYPE(EldestFunctor):
	def __init__(this, name=eons.INVALID_NAME()):
		super().__init__(name)

		this.value = None
		this.needsTypeAssignment = True

	def EQ(this, other):
		# TODO: change the actual class?
		if (this.needsTypeAssignment):
			if (
				isinstance(other, bool)
				or isinstance(other, int)
				or isinstance(other, float)
				or isinstance(other, str)
			):
				this.value = other
				this.needsTypeAssignment = False
			else:
				# It's complex, so we'll leave it as a functor.
				pass
			this.needsTypeAssignment = False

		if (this.executor is not None):
			# Determine if this is assignment or setting a default value.
			isDefault = False
			stack = this.executor.stack.copy()
			stack.reverse()
			for name, object in stack:
				if (name == 'Autofill'):
					continue
				elif (name == 'Within'):
					continue
				elif (name == 'Type'):
					isDefault = True
					break
				break
		
			if (isDefault):
				this.default = other
				return this
		
		this = other
		return this

	def GT(this, other):
		return this > other

	def LT(this, other):
		return this < other

	def EQEQ(this, other):
		return this == other
	
	def NOTEQ(this, other):
		return this != other

	def GTEQ(this, other):
		return this >= other

	def LTEQ(this, other):
		return this <= other

	def POW(this, other):
		return pow(this, other)

	def AND(this, other):
		return this and other

	def ANDAND(this, other):
		return this.AND(other)

	def OR(this, other):
		return this or other

	def OROR(this, other):
		return this.OR(other)

	def PLUS(this, other):
		return this + other

	def MINUS(this, other):
		return this - other

	def TIMES(this, other):
		return this * other

	def DIVIDE(this, other):
		return this / other

	def PLUSEQ(this, other):
		this = this + other
		return this

	def MINUSEQ(this, other):
		this = this - other
		return this

	def TIMESEQ(this, other):
		this = this * other
		return this

	def DIVIDEEQ(this, other):
		this = this / other
		return this

	def MOD(this, other):
		return this % other
	
	def MODEQ(this, other):
		this = this % other
		return this
	
	def size(this):
		return len(this)

	def length(this):
		return this.size()
	

def CreateArithmeticFunction(functionName):
	return lambda this, *args: getattr(this.value if this.value is not None else this, functionName)(*args)
	
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
	"__EQ_",
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
