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
		parameters = {
			'constructor': eons.util.DotDict({
				'name': 'constructor',
				'kind': inspect.Parameter.POSITIONAL_OR_KEYWORD,
				'default': '''
if ('value' in kwargs):
	this.value = kwargs['value']
	del kwargs['value']
'''
			})
		}
		if (this.parameter is not None):
			parameters = {
				a.name: eons.util.DotDict({
					'name': a.name,
					'kind': inspect.Parameter.POSITIONAL_OR_KEYWORD,
					'default': a.default,
					'type': a.__class__
				})
				for a in EVAL(this.parameter, unwrapReturn=False)
				if a is not None # TODO: why???
			}

		source = "pass"
		if (this.execution is not None):
			if (type(this.execution) != list):
				this.execution = [this.execution]
			source = f"return this.executor.EXEC({this.execution}, currentlyTryingToInvoke=this)"

		ret = eons.kind(this.kind) (
			None,
			this.name,
			parameters,
			source,
			strongType=True
		)
		ret = ret()
		ret.WarmUp(executor=this.executor)

		# Export this symbol to the current context iff we're not adding a parameter to another type.
		if (not this.IsCurrentlyInTypeParameterBlock(1)):
			this.context.Set(this.name, ret)

		return ret
