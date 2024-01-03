from ..TYPE import TYPE

class INT(TYPE):
	def __init__(this, name="integer", value=0):
		super().__init__(name)

		this.value = value
		this.needsTypeAssignment = False

	def __int__(this):
		return this.value
	
	def Function(this):
		return this.value