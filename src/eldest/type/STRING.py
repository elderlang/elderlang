from ..TYPE import TYPE

class STRING(TYPE):
	def __init__(this, name="string", value=""):
		super().__init__(name)

		this.value = value
		this.useValue = True
		this.needs.typeAssignment = False

	def Function(this):
		return this.value

	def startswith(this, other):
		return this.value.startswith(other)
	
	def endswith(this, other):
		return this.value.endswith(other)