import eons
from ..TYPE import TYPE
from ..EVAL import EVAL
from ..EXEC import EXEC
from ..HOME import HOME

class FUNCTOR(TYPE):
	def __init__(this, name=eons.INVALID_NAME(), value=None):
		super().__init__(name)

		this.needs.typeAssignment = False
		this.isBasicType = False
		this.value = value # Should be pointless, but who knows.
		this.feature.track = True
		this.feature.sequential = True
		this.feature.sequence.clone = True

		# Global variables will be fetched by going up the stack one scope at a time.
		# We should only grab an item from HOME first if we're explicitly told to.
		# this.fetch.use.append('home')

	def ValidateMethods(this):
		super().ValidateMethods()
		for okwarg in this.arg.kw.optional.keys():
			mem = getattr(this, okwarg)
			if (isinstance(mem, FUNCTOR)):
				mem.epidef = this

	def PrepareNext(this, next):
		next.feature.autoReturn = True # <- recommended if you'd like to be able to access the modified sequence result.

	def Function(this):
		pass

	# See note in constructor regarding fetching from home.
	# def fetch_location_home(this, varName, default, fetchFrom, attempted):
	# 	try:
	# 		return getattr(HOME.Instance(), varName), True
	# 	except:
	# 		return default, False
	
	# Restore lost sequence functionality (this method was overridden by TYPE).
	def __truediv__(this, next):
		return eons.Functor.__truediv__(this, next)

	def __str__(this):
		return this.name