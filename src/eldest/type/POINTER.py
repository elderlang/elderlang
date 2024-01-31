from typing import Any
from ..TYPE import TYPE

class POINTER(TYPE):
	def __init__(this, obj):
		super().__init__(f"Pointer to {repr(obj)}")

		this.value = obj
		this.isBasicType = True
		this.needs.typeAssignment = False

	@staticmethod
	def to(obj):
		return POINTER(obj)

	def __getattribute__(this, attribute):
		if (attribute == "to"):
			return POINTER.to
		if (attribute in ["value", "isPointer"]):
			return object.__getattribute__(this, attribute)
		try:
			# Will fail if value is null.
			return object.__getattribute__(this, 'value').__getattribute__(attribute)
		except:
			# TODO: consider raising an exception when trying to dereference a null pointer.
			return super().__getattribute__(attribute)