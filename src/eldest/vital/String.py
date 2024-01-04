import eons
from ..EldestFunctor import EldestFunctor
from ..EVAL import EVAL
from ..EXEC import EXEC

class String (EldestFunctor):
	def __init__(this, name="String"):
		super().__init__(name)

		this.feature.mapArgs = False

	def Function(this):
		template = this.args[0]
		arguments = this.args[1:]
		return template % tuple(arguments)