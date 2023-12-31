import eons
from ..TYPE import TYPE
from ..EVAL import EVAL
from ..EXEC import EXEC

class FUNCTOR(TYPE):
	def __init__(this, name=eons.INVALID_NAME(), value=None):
		super().__init__(name)

		this.needs.typeAssignment = False
		this.isBasicType = False
		this.value = value # Should be pointless, but who knows.
		
	def Function(this):
		return EXEC(this.execution, currentlyTryingToInvoke=this)