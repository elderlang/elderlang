import eons
from ..EldestFunctor import EldestFunctor
from ..EVAL import EVAL
from ..EXEC import EXEC

class Within (EldestFunctor):
	def __init__(this, name="Within"):
		super().__init__(name)

		this.arg.kw.optional['name'] = None
		this.arg.kw.optional['source'] = None
		this.arg.kw.optional['useInvokation'] = False

		this.arg.kw.required.append('container')

		this.arg.mapping.append('name')
		this.arg.mapping.append('container')

	def Function(this):
		if (this.source is not None):
			if (this.useInvokation):
				return this.source([EVAL(item) for item in this.container])
			return this.source[*[EVAL(item) for item in this.container]]
		elif (this.name is not None):
			return EVAL(this.name)[*[EVAL(item) for item in this.container]]

		raise RuntimeError(f"Neither source nor name was provided to {this.name}")