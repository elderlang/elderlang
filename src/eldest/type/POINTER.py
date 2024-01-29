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

	def __getattribute__(this, __name: str):
		if (__name == "to"):
			return POINTER.to
		if (this.value is not None):
			return this.value.__getattribute__(__name)
		return super().__getattribute__(__name)