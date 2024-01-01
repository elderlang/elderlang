from ..TYPE import TYPE

class STRING(TYPE):
	def __init__(this, name="string", value=""):
		super().__init__(name)

		this.value = value
		this.needsTypeAssignment = False