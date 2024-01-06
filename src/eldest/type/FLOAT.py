from ..TYPE import TYPE

class FLOAT(TYPE):
	def __init__(this, name="float", value=0.0):
		super().__init__(name)

		this.value = value
		this.isBasicType = True
		this.needsTypeAssignment = False

	def __float__(this):
		return this.value
	
	def Function(this):
		return this.value