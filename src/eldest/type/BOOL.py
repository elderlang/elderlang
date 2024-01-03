from ..TYPE import TYPE

class BOOL(TYPE):
	def __init__(this, name="bool", value=False):
		super().__init__(name)

		this.value = value
		this.needsTypeAssignment = False

	def __bool__(this):
		return this.value
	
	def Function(this):
		return this.value