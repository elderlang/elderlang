from typing import Any
import copy
import logging
from ..TYPE import TYPE

# The purpose of a pointer is to hold a value that lives elsewhere and allow special handling of write operations.
# For example, a POINTER could implement copy-on-write semantics.
class POINTER(TYPE):
	def __init__(this, obj):
		super().__init__(f"Pointer to {repr(obj)}")

		this.value = obj
		this.isBasicType = True
		this.needs.typeAssignment = False

		this.SET = None

	@staticmethod
	def to(obj):
		return POINTER(obj)
	
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
		if (attribute in ["value", "isPointer", "EQ", "SET"]):
			return object.__getattribute__(this, attribute)
		try:
			# Will fail if value is null.
			return object.__getattribute__(this, 'value').__getattribute__(attribute)
		except:
			# TODO: consider raising an exception when trying to dereference a null pointer.
			return super().__getattribute__(attribute)