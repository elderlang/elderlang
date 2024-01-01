import eons
from ..TYPE import TYPE
from ..EVAL import EVAL
from ..EXEC import EXEC

class FUNCTOR(TYPE):
	def __init__(this, name=eons.INVALID_NAME()):
		super().__init__(name)

		this.needsTypeAssignment = False
		
	def Function(this):
		return EXEC(this.execution)