from ..TYPE import TYPE

class STRING(TYPE):
	def __init__(this, name="string", value=""):
		super().__init__(name)

		this.value = value
		this.isBasicType = True
		this.needs.typeAssignment = False

	def __str__(this):
		return this.value

	def Function(this):
		return this.value