from ..TYPE import TYPE

class CONTAINER(TYPE):
	def __init__(this, name="container", value=[]):
		super().__init__(name)

		this.value = value
		this.isBasicType = True
		this.needs.typeAssignment = False

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
			this.value.insert(index, value)
		else:
			this.value[index] = value

	def Function(this):
		return this.value