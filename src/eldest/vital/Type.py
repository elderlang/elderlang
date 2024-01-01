import eons
import inspect
import logging
from ..EldestFunctor import EldestFunctor
from ..EVAL import EVAL
from ..EXEC import EXEC

class Type (EldestFunctor):
	def __init__(this, name="Type"):
		super().__init__(name)

		this.arg.kw.required.append('name')
		this.arg.kw.required.append('kind')

		this.arg.kw.optional['parameter'] = None
		this.arg.kw.optional['execution'] = []

	def Function(this):
		parameters = {}
		if (this.parameter is not None):
			parameters = {
				a.name: eons.util.DotDict({
					'name': a.name,
					'kind': inspect.Parameter.POSITIONALOR_KEYWORD,
					'default': a.default,
				})
				for a in EVAL(this.parameter, unwrapReturn=False)
			}
		
		source = "pass"
		if (this.execution is not None):
			if (type(this.execution) != list):
				this.execution = [this.execution]
			source = f"for instruction in {this.execution}: EXEC(instruction)"
		
		ret = eons.kind(this.kind) (
			None,
			this.name,
			parameters,
			source
		)

		ret.executor = this.executor

		return ret
