import eons
from ..EldestFunctor import EldestFunctor
from ..EVAL import EVAL
from ..EXEC import EXEC

class Sequence (EldestFunctor):
	def __init__(this, name="Sequence"):
		super().__init__(name)

		this.arg.kw.optional['name'] = None
		this.arg.kw.optional['source'] = None

		this.arg.kw.required.append('target')

		this.arg.mapping.append('source')
		this.arg.mapping.append('target')

	def Function(this):
		if (this.source is not None):
			return this.source.__truediv__(EVAL(this.target))
		elif (this.name is not None):
			return EVAL(this.name).__truediv__(EVAL(this.target))
		
		raise RuntimeError(f"Neither source nor name was provided to {this.name}")