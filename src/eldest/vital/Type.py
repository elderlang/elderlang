import eons
import inspect
import logging
from ..EldestFunctor import EldestFunctor
from ..EVAL import EVAL
from ..EXEC import EXEC
from ..TYPE import TYPE
from ..type.FUNCTOR import FUNCTOR
from ..type.STRUCTOR import STRUCTOR

class Type (EldestFunctor):
	def __init__(this, name="Type"):
		super().__init__(name)

		this.arg.kw.required.append('name')
		this.arg.kw.optional['kind'] = [TYPE]

		this.arg.kw.optional['parameter'] = None
		this.arg.kw.optional['execution'] = []


	def BeforeFunction(this):
		this.unsetCurrentlyTryingToDefine = False

		try:
			this.Set('currentlyTryingToDefine', currentlyTryingToDefine) # easy global fetch.
		except:
			this.Set('currentlyTryingToDefine', None)

		if (this.currentlyTryingToDefine):
			this.originalName = this.name
			this.originallyTryingToDefine = this.currentlyTryingToDefine
			this.name = f"{this.currentlyTryingToDefine}_{this.name}"
			this.executor.SetGlobal('currentlyTryingToDefine', this.name)
		else:
			this.executor.SetGlobal('currentlyTryingToDefine', this.name)
			this.unsetCurrentlyTryingToDefine = True

		return super().BeforeFunction()


	def Function(this):
		# alreadyDefined = None
		# try:
		# 	alreadyDefined = EVAL(this.parameter, unwrapReturn=False, shouldAutoType=False, currentlyTryingToDefine=this.name)
		# except:
		# 	pass

		parameters = {
			'constructor': eons.util.DotDict({
				'name': 'constructor',
				'kind': inspect.Parameter.POSITIONAL_OR_KEYWORD,
				'default': f'''
if (this.name is None):
	this.name = {this.name}

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

			# Having a parameter implies this is a functor or structor
			if (this.kind == [TYPE]):
				this.kind = [STRUCTOR]

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

			# Having an execution block implies this is a functor.
			if (this.kind == [TYPE] or this.kind == [STRUCTOR]):
				this.kind = [FUNCTOR]

		ret = eons.kind(this.kind) (
			None,
			this.name,
			parameters,
			source,
			strongType=True
		)
		ret = ret() # class -> object

		ret.WarmUp(executor=this.executor)

		# if (alreadyDefined is not None and this.kind == [TYPE]):
		# 	this.CombineWithExisting(alreadyDefined, ret)
		# 	return alreadyDefined

		# Export this symbol to the current context iff we're not adding a parameter to another type.
		if (this.currentlyTryingToDefine is None):
			this.context.Set(this.name, ret)

		ret.EXEC_NO_EXECUTE = True
		this.result.data.product = ret
		return ret


	def AfterFunction(this):
		# NOTE Python bug: any access of currentlyTryingToDefine here, even within uninterpreted code, will cause it to be set to None.
		if (this.unsetCurrentlyTryingToDefine):
			this.executor.ExpireGlobal('currentlyTryingToDefine')
			globals()['currentlyTryingToDefine'] = None # TODO: the above is not enough???

		# If nothing was added, i.e. no sub-types were declared, and we're done, but 
		# Only occurs with short-typed functor pointers, like 'inner' in pointer.ldr. 
		else:
			this.executor.SetGlobal('currentlyTryingToDefine', this.originallyTryingToDefine)

		return super().AfterFunction()


	def CombineWithExisting(this, existing, new):
		pass
		# for key, val in new.__dict__.items():
		# 	if (key in existing.__dict__):
		# 		if (isinstance(val, eons.Functor)):
		# 			this.CombineWithExisting(existing.__dict__[key], val)
		# 		else:
		# 			existing.__dict__[key] = val
