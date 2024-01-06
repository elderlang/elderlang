import eons
import logging
from copy import deepcopy
from .Sanitize import Sanitize

class EldestFunctor (eons.Functor):
	def __init__(this, name=eons.INVALID_NAME()):
		super().__init__(name)

		this.feature.autoReturn = False

		this.fetch.use = [
			'args',
			'this',
			'stack_name',
			# 'stack_type',
			'context',
			'history',
			'globals',
			# 'config', #local (if applicable) or per Executor; should be before 'executor' if using a local config.
			# 'precursor',
			# 'caller',
			# 'executor',
			# 'environment',
		]

		this.context = None

	def __call__(this, *args, **kwargs):
		clone = deepcopy(this)
		return super(EldestFunctor, clone).__call__(*args, **kwargs)

	def BeforeFunction(this):
		this.Set('context', this.FetchWithout(['this', 'context', 'stack', 'history'], 'context', None))

		this.executor.stack.append(
			(this.name, this)
		)
		logging.debug(f"Stack is now: {this.executor.stack}")

		if (this.context is None):
			this.context = this.executor.context

	def AfterFunction(this):
		this.executor.stack.remove(
			(this.name, this)
		)
		this.executor.history.insert(
			0,
			(this.name, this)
		)
		logging.debug(f"History is now: {this.executor.history}")

	
	def IsCurrentlyInTypeParameterBlock(this, offset=0):
		
		# FIXME: Not having an executor should be an impossibility.
		# This appears to be happening in if.ldr, where the foremost Type() is attempting assignment to bool.
		if (not this.executor):
			return False
		
		stack = this.executor.stack.copy()
		stack.reverse()
		for name, object in stack[offset:]:
			if (name == 'Autofill'):
				continue
			elif (name == 'eval'):
				continue
			elif (name == 'Within'):
				continue
			# Objects will be provided later, don't worry about where they come from.
			elif (isinstance(object, Call.__class__)):
				continue
			elif (isinstance(object, Type.__class__)):
				return True
		return False


	def fetch_location_stack_name(this, varName, default, fetchFrom, attempted):
		if (this.executor is None):
			return default, False
		
		if (varName.upper() not in Sanitize.allBuiltins):
			return default, False
		
		stack = this.executor.stack.copy()
		stack.reverse()
		for name, object in stack:
			if (name == varName):
				return object, True

		return default, False
	
	def fetch_location_stack_type(this, varName, default, fetchFrom, attempted):
		if (this.executor is None):
			return default, False
		
		if (varName.upper() not in Sanitize.allBuiltins):
			return default, False
		
		typeToFind = eval(f"{varName}.__class__")
		
		stack = this.executor.stack.copy()
		stack.reverse()
		for name, object in stack:
			if (isinstance(object, typeToFind)):
				return object, True

		return default, False
	
	def fetch_location_history(this, varName, default, fetchFrom, attempted):
		if (this.executor is None):
			return default, False
		
		if (varName.upper() not in Sanitize.allBuiltins):
			return default, False
		
		for name, object in this.executor.history:
			if (name == varName):
				return object, True

		return default, False
	

	def fetch_location_context(this, varName, default, fetchFrom, attempted):
		if (this.context is None):
			return default, False
		
		return this.context.Fetch(varName, default, start=False, fetchFrom=fetchFrom,attempted=attempted)