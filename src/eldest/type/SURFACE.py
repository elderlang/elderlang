from ..TYPE import TYPE

class SURFACE(TYPE):
	def __init__(this, name="surface", value=[]):
		super().__init__(name)

		this.value = value
		this.isBasicType = True
		this.needsTypeAssignment = False

	def __list__(this):
		if (isinstance(this.value, dict)):
			return this.value.keys()
		return this.value
	
	def __dict__(this):
		if (isinstance(this.value, list)):
			return {key: key for key in this.value}
	
	def Function(this):
		return this.value