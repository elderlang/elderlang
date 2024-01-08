import eons
import logging
from ..EldestFunctor import EldestFunctor
from ..EVAL import EVAL
from ..EXEC import EXEC

class String (EldestFunctor):
	def __init__(this, name="String"):
		super().__init__(name)

		this.feature.mapArgs = False

	def Function(this):
		template = this.args[0]
		ret = template
		if (len(this.args) > 1):
			arguments = []
			[arguments.append(arg) for lst in this.args[1:] for arg in lst]
			arguments = [EVAL(arg)[0] for arg in arguments]
			toEval = f"""'{template}' % '{"', '".join([str(arg) for arg in arguments])}'"""
			logging.debug(f"Constructing string from: {toEval}")
			ret = eval (toEval)
		return ret