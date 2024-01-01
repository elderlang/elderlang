import eons
from ..EldestFunctor import EldestFunctor
from ..EVAL import EVAL
from ..EXEC import EXEC

class Invoke (EldestFunctor):
	def __init__(this, name="Invoke"):
		super().__init__(name)

		this.arg.kw.optional['name'] = None
		this.arg.kw.optional['source'] = None

		this.arg.kw.optional['parameter'] = None
		this.arg.kw.optional['container'] = None
		this.arg.kw.optional['execution'] = None

	def Function(this):
		if (this.source is None and this.name is not None):
			this.source = EVAL(this.name)
		if (this.source is None):
			raise RuntimeError(f"Neither source nor name was provided to {this.name}")

		if (this.parameter is None):
			this.parameter = ''

		evaluatedParameter = EVAL(this.parameter)
		if (not isinstance(evaluatedParameter, list)):
			evaluatedParameter = [evaluatedParameter]

		return this.source(*evaluatedParameter, container=this.container, execution=this.execution)