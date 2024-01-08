import eons
from ..TYPE import TYPE

class NUMBER(TYPE):
	def __init__(this, name=eons.INVALID_NAME, value=0):
		super().__init__(name)

		this.value = value
		this.isBasicType = True
		this.needs.typeAssignment = False

	def __int__(this):
		return int(this.value)
	
	def __float__(this):
		return float(this.value)
	
	def Function(this):
		return this.value
	
	def PLUSPLUS(this):
		this.value += 1
		return this
	
	def MINUSMINUS(this):
		this.value -= 1
		return this