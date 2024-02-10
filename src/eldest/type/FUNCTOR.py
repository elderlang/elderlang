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

		this.fetch.use.append('home')

	def ValidateMethods(this):
		super().ValidateMethods()
		for okwarg in this.arg.kw.optional.keys():
			mem = getattr(this, okwarg)
			if (isinstance(mem, FUNCTOR)):
				mem.epidef = this

	def Function(this):
		return EXEC(this.execution, currentlyTryingToInvoke=this)

	def fetch_location_home(this, varName, default, fetchFrom, attempted):
		return default, False