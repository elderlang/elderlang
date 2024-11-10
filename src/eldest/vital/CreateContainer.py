import eons
from ..EldestFunctor import EldestFunctor
from ..TYPE import TYPE
from ..EVAL import EVAL
from ..EXEC import EXEC

class CreateContainer (EldestFunctor):
	def __init__(this, name="CreateContainer"):
		super().__init__(name)

		this.arg.kw.optional['container'] = None

		this.arg.mapping.append('container')

		# Signal to Autofill that we want to create types if they don't exist.
		# These are key word args (e.g. var = val)
		this.shouldAutoType = True

	def Function(this):
		if (this.container is None):
			this.container = []

		ret = CONTAINER()
		for val in this.container:
			ret.append(EVAL([val], unwrapReturn = True, shouldAttemptInvokation = True)[0])
		return ret
