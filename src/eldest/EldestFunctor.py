import eons
import logging
import inspect
import re
from copy import deepcopy
from .Sanitize import Sanitize

class EldestFunctor (eons.Functor):
	def __init__(this, name=eons.INVALID_NAME()):
		super().__init__(name)

		this.feature.autoReturn = False

		# New features
		this.feature.cloneOnCall = True
		this.needs = eons.util.DotDict()

		this.fetch.use = [
			'args',
			'this',
			'stack_name',
			# 'stack_type',
			'context',
			# 'history',
			'globals',
			# 'config', #local (if applicable) or per Executor; should be before 'executor' if using a local config.
			# 'precursor',
			# 'caller',
			# 'executor',
			# 'environment',
		]

		this.context = None


	def __call__(this, *args, **kwargs):
		clone = this
		if (this.feature.cloneOnCall):
			clone = deepcopy(this)
		return super(EldestFunctor, clone).__call__(*args, **kwargs)


	def ValidateArgs(this):
		this.Set('context', this.Fetch('context', None, ['args', 'globals']))
		if (this.context is None and this.executor is not None):
			this.context = this.executor.context
		return super().ValidateArgs()


	def BeforeFunction(this):
		try:
			this.executor.stack.insert(
				0,
				(this.name, this)
			)
			logging.debug(f"Stack is now: {this.executor.stack}")
		except:
			logging.error(f"Could not add {this.name} ({type(this)}) to the stack.")

		super().BeforeFunction()


	def AfterFunction(this):
		super().AfterFunction()

		# Failure to remove items from the stack, history, etc. is fine.

		try:
			this.executor.stack.remove(
				(this.name, this)
			)
		except:
			logging.debug(f"Could not remove {this.name} ({type(this)}) from the stack.")

		try:
			this.context.history.insert(
				0,
				(this.name, this)
			)
			logging.debug(f"History is now: {this.context.history}")
		except:
			logging.debug(f"Could not add {this.name} ({type(this)}) to the history.")

	
	def IsCurrentlyInTypeParameterBlock(this, offset=0):
		
		# FIXME: Not having an executor should be an impossibility.
		# This appears to be happening in if.ldr, where the foremost Type() is attempting assignment to bool.
		if (not this.executor):
			return False

		for name, object in this.executor.stack[offset:]:
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
	
	def IsCurrentlyInTypeExecutionBlock(this):
		
		# FIXME: Not having an executor should be an impossibility.
		# This appears to be happening in if.ldr, where the foremost Type() is attempting assignment to bool.
		if (not this.executor):
			return False

		name, obj = this.executor.stack[0]
		if (obj == this.context):
			return True

		return False
	

	def CorrectForImproperQuotes(this, string):
		if (re.search(r"\('[a-zA-Z0-9]*\('", string)):
			string = string.replace("('", '("', 1)
			string = string.replace(")', '", ')", "', 1)
			string = re.sub(r"\)'(.*)$", r')"\1', string)
		elif (re.search(r"'[a-zA-Z0-9]*\('", string)):
			string = re.sub(r"'([a-zA-Z0-9]*)\('", r'"\1(\'', string)
			string = re.sub(r"\)'(.*)$", r')"\1', string)
		return string


	def fetch_location_stack_name(this, varName, default, fetchFrom, attempted):
		if (this.executor is None):
			return default, False
		
		if (varName.upper() not in Sanitize.allBuiltins):
			return default, False

		for name, object in this.executor.stack:
			if (name == varName):
				return object, True

		return default, False
	
	def fetch_location_stack_type(this, varName, default, fetchFrom, attempted):
		if (this.executor is None):
			return default, False

		if (varName.upper() not in Sanitize.allBuiltins):
			return default, False

		if (isinstance(varName, str)):
			typeToFind, unwrapped = eval(varName)

		if (inspect.isclass(varName)):
			typeToFind = varName
		elif (isinstance(varName, object)):
			typeToFind = varName.__class__

		if (typeToFind is None or not inspect.isclass(typeToFind)):
			logging.debug(f"Could not find type {varName} in stack.")
			return default, False

		for name, object in this.executor.stack:
			if (isinstance(object, typeToFind)):
				return object, True

		return default, False

	# History should only be used for keywords like ELSE.
	def fetch_location_history(this, varName, default, fetchFrom, attempted):
		if (this.context is None):
			return default, False
		
		if (varName.upper() not in Sanitize.allBuiltins):
			return default, False
		
		for name, object in this.context.history:
			if (name == varName):
				return object, True

		return default, False
	

	def fetch_location_context(this, varName, default, fetchFrom, attempted):
		if (this.context is None):
			return default, False
		
		return this.context.Fetch(varName, default, start=False, fetchFrom=fetchFrom,attempted=attempted)