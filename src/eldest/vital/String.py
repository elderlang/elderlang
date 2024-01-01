import eons
from ..EldestFunctor import EldestFunctor
from ..EVAL import EVAL
from ..EXEC import EXEC

class String (EldestFunctor):
	def __init__(this, name="String"):
		super().__init__(name)

		this.feature.argMap = False

	def Function(this):
		template = this.args[0]
		arguments = this.args[1:]
		return template.format(*[EVAL(arg) for arg in arguments])