from ..TYPE import TYPE
from .POINTER import POINTER

# Containers always store data by reference.
class CONTAINER(TYPE):
	def __init__(this, name="container", value=[]):
		super().__init__(name)

		this.value = []
		if (value is not None):
			for item in value:
				this.value.append(item)
		this.useValue = True
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
		ret = POINTER(f"{this.name}[{index}]", this.value[index])
		ret.SET = lambda x: this.__setitem__(index, x)
		return ret

	def __setitem__(this, index, value):
			this.value[index] = value

	def insert(this, index, value):
		this.value.insert(index, value)

	def Function(this):
		return this.value