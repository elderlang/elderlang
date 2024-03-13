import eons
from ..TYPE import TYPE
from ..EVAL import EVAL
from ..EXEC import EXEC
from ..HOME import HOME

class FUNCTOR(TYPE):
	def __init__(this, name=eons.INVALID_NAME(), value=None):
		super().__init__(name)

		this.needs.typeAssignment = False
		this.useValue = False
		delattr(this, 'value')
		this.feature.track = True
		this.feature.sequential = True
		this.feature.sequence.clone = True
		this.feature.autoReturn = False

		# TODO: Solidify this behavior.
		# cloneOnCall being True is required to make changes from one call not persist to the next.
		# See the pointer.ldr unit test for an example.
		# FIXME: Making this True induces very strange behavior.
		this.feature.cloneOnCall = False #True

		this.fetch.use = [
			'args',
			'this',
			'precursor',
			'epidef',
			'caller',
			'context',
			'history',
			'globals',
			'executor',
			'config',
			'environment',
		]
		this.fetch.attr.use = [
			'precursor',
			'epidef',
		]

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

	# Restore lost sequence functionality (this method was overridden by TYPE).
	def __truediv__(this, next):
		return eons.Functor.__truediv__(this, next)

	def __str__(this = None):
		if (this is None):
			return 'FUNCTOR'
		return this.name