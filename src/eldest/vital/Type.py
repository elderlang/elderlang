import eons
import inspect
import logging
from ..EldestFunctor import EldestFunctor
from ..EVAL import EVAL
from ..EXEC import EXEC
from ..TYPE import TYPE

class Type (EldestFunctor):
	def __init__(this, name="Type"):
		super().__init__(name)

		this.arg.kw.required.append('name')
		this.arg.kw.optional['kind'] = [TYPE]

		this.arg.kw.optional['parameter'] = None
		this.arg.kw.optional['execution'] = []

	def Function(this):
		try:
			this.Set('currentlyTryingToDefine', currentlyTryingToDefine) # easy global fetch.
		except:
			this.Set('currentlyTryingToDefine', None)

		if (this.currentlyTryingToDefine is not None):
			this.name = f"{this.currentlyTryingToDefine}_{this.name}"

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
					'default': a.default if hasattr(a, 'default') else None,
					'type': a.__class__
				})
				for a in EVAL(this.parameter, unwrapReturn=False, shouldAutoType=True, currentlyTryingToDefine=this.name)[0]
				if a is not None # TODO: why???
			}

		toDelete = []
		for key in parameters.keys():
			if (key.startswith(this.name)):
				toDelete.append(key)
		for key in toDelete:
			parameters[key[len(this.name)+1:]] = parameters[key]
			parameters[key[len(this.name)+1:]].update({'name': key[len(this.name)+1:]})
			del parameters[key]

		source = "return this.parent.Function(this)"
		if (this.execution is not None and len(this.execution) > 0):
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
		ret = ret() # class -> object

		ret.WarmUp(executor=this.executor)

		# Export this symbol to the current context iff we're not adding a parameter to another type.
		if (not this.IsCurrentlyInTypeParameterBlock(1)):
			if (this.currentlyTryingToDefine is not None):
				this.context.Set(this.name[len(this.currentlyTryingToDefine)+1:], ret)
			else:
				this.context.Set(this.name, ret)

		this.result.data.returned = ret
		return ret
