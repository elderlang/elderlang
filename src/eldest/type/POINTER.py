from typing import Any
import inspect
import logging
from ..TYPE import TYPE

# The purpose of a pointer is to hold a value that lives elsewhere and allow special handling of write operations.
# For example, a POINTER could implement copy-on-write semantics.
class POINTER(TYPE):

	def __init__(this, name=None, value=None):
		if (name is None):
			name = f"Pointer to {repr(value)}"
		super().__init__()

		if (value is None and hasattr(this, 'target')):
			this.value = this.target()
		else:
			this.value = value

		this.useValue = False # But true in practice.
		this.needs.typeAssignment = False

		this.SET =  lambda val: setattr(this, 'value', val)

	@staticmethod
	def to(obj):
		cls = obj
		if (not inspect.isclass(obj)):
			cls = type(obj)

		ret = type(
			f"POINTER_TO_{cls.__name__.upper()}",
			(POINTER,),
			{'target': cls}
		)

		if (inspect.isclass(obj)):
			return ret

		return ret(None, obj)

	# Overriding the EQ method allows pointers to change how they are set.
	def EQ(this, other):
		try:
			this.SET(this.PossiblyReduceOther(other))
			logging.debug(f"Set {this} to {other}")
		except:
			try:
				this.value.EQ(other)
			except:
				try:
					this.value = other.value
				except:
					this.value = other
		return this

	# Explicit dereference operator.
	# Explicit dereferencing is not necessary at this time.
	# def TIMES(this, other=None):
	# 	if (other is not None):
	# 		try:
	# 			return this.value.TIMES(other)
	# 		except:
	# 			return super().TIMES(other)
	# 	logging.debug(f"Dereferencing {this.name}")
	# 	# object.__getattribute__(this, '__dict__').update(copy.deepcopy(object.__getattribute__(this, '__dict__')))
	# 	this.value = copy.copy(this.value)
	# 	return this

	def __getattribute__(this, attribute):
		if (attribute == "to"):
			return POINTER.to
		if (attribute in ["__class__", "__init__", "name", "value", "isPointer", "EQ", "SET"]):
			return object.__getattribute__(this, attribute)
		try:
			# Will fail if value is null.
			return object.__getattribute__(this, 'value').__getattribute__(attribute)
		except:
			# TODO: consider raising an exception when trying to dereference a null pointer.
			return super().__getattribute__(attribute)

	def __setattribute__(this, name, value):
		if (name in ["value", "SET", "to"]):
			super().__setattribute__(name, value)
		try:
			setattr(this.value, name, value)
		except:
			super().__setattribute__(name, value)