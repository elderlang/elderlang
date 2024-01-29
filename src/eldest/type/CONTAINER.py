from ..TYPE import TYPE
from .POINTER import POINTER

# Containers always store data by reference.
class CONTAINER(TYPE):
	def __init__(this, name="container", value=[]):
		super().__init__(name)

		this.value = []
		if (value is not None):
			for item in value:
				this.value.append(POINTER(item))
		this.isBasicType = True
		this.needs.typeAssignment = False

	@staticmethod
	def of(value):
		return CONTAINER(value=value)

	def __list__(this):
		if (isinstance(this.value, dict)):
			return this.value.keys()
		return this.value

	def __dict__(this):
		if (isinstance(this.value, list)):
			return {key: key for key in this.value}

	def __getitem__(this, index):
		return this.value[index]

	def __setitem__(this, index, value):
		if (isinstance(this.value, list)):
			this.value.insert(index, POINTER(value))
		else:
			this.value[index] = POINTER(value)

	def insert(this, index, value):
		this.value.insert(index, POINTER(value))

	def Function(this):
		return this.value