import eons
import logging
import inspect
import re
from copy import deepcopy

class EldestFunctor (eons.Functor):
	def __init__(this, name=eons.INVALID_NAME()):
		super().__init__(name)

		this.feature.autoReturn = False
		this.feature.track = False

		# New features
		this.feature.cloneOnCall = True
		this.needs = eons.util.DotDict()

		this.fetch.possibilities = [
			'args',
			'this',
			'epidef',
			'stack_name',
			'stack_type',
			'context',
			'history',
			'globals',
			'config', #local (if applicable) or per Executor; should be before 'executor' if using a local config.
			'precursor',
			'caller', # Must be accessed directly.
			'executor',
			'environment',
		]

		this.fetch.use = [
			'args',
			'this',
			'stack_name',
			'context',
			'globals',
		]

		this.context = None

		this.prevent.copying.extend([
			'context',
			'home',
		])


	def __call__(this, *args, **kwargs):
		clone = this
		if (this.feature.cloneOnCall):
			clone = deepcopy(this)
			clone.executor = this.executor
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
		except Exception as e:
			logging.error(f"Could not add {this.name} ({type(this)}) to the stack: {e}")

		super().BeforeFunction()


	def AfterFunction(this):
		super().AfterFunction()

		# Failure to remove items from the stack, history, etc. is fine.

		try:
			this.executor.stack.remove(
				(this.name, this)
			)
		except Exception as e:
			logging.debug(f"Could not remove {this.name} ({type(this)}) from the stack: {e}")

		try:
			this.context.history.insert(
				0,
				(this.name, this)
			)
			logging.debug(f"History is now: {this.context.history}")
		except Exception as e:
			logging.debug(f"Could not add {this.name} ({type(this)}) to the history: {e}")


	# NOTE: USE THIS METHOD WITH EXTREME CARE.
	# Because nested classes are defined before the parent, this will always return true from a parent class if it has nested children.
	# Consider checking if currentlyTryingToDefine is set (in globals, per executor).
	def IsCurrentlyInTypeParameterBlock(this, offset=0):
		
		# FIXME: Not having an executor should be an impossibility.
		# This appears to be happening in if.ldr, where the foremost Type() is attempting assignment to bool.
		if (not this.executor):
			return False

		try:
			for name, obj in this.executor.stack[offset:]:
				# Objs will be provided later, don't worry about where they come from.
				if (isinstance(obj, Autofill.__class__)):
					continue
				if (isinstance(obj, EVAL.__class__)):
					continue
				if (isinstance(obj, Within.__class__)):
					continue
				if (isinstance(obj, Invoke.__class__)):
					continue
				if (isinstance(obj, Call.__class__)):
					continue


				# For extra certainty.
				if (name == 'Autofill'):
					continue
				if (name == 'eval'):
					continue
				if (name == 'Within'):
					continue
				if (name == 'source_name_None'): # TODO: ???
					continue
				
				if (isinstance(obj, Type.__class__)):
					return True
				else:
					break
		except:
			pass
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
		
		
		if (varName.upper() not in this.executor.sanitize.allBuiltins):
			return default, False


		if (varName.upper() not in this.executor.sanitize.allBuiltins):
			return default, False

		for name, obj in this.executor.stack:
			if (name == varName):
				return obj, True

		return default, False
	
	def fetch_location_stack_type(this, varName, default, fetchFrom, attempted):
		if (this.executor is None):
			return default, False

		if (isinstance(varName, str)):
			try:
				typeToFind = eval(varName)
			except:
				return default, False

		if (inspect.isclass(varName)):
			typeToFind = varName

		# TODO: UnboundLocalError: cannot access local variable 'obj' where it is not associated with a value
		# elif (isinstance(varName, obj)):
		# 	typeToFind = varName.__class__

		if (typeToFind is None or not inspect.isclass(typeToFind)):
			logging.debug(f"Could not find type {varName} in stack.")
			return default, False

		for name, obj in this.executor.stack:
			if (isinstance(obj, typeToFind)):
				return obj, True

		return default, False

	# History should only be used for keywords like ELSE.
	def fetch_location_history(this, varName, default, fetchFrom, attempted):
		if (this.context is None):
			return default, False
		
		for name, obj in this.context.history:
			# Types should be retrieved through eons.SelfRegistering, etc.
			# Fetching a Functor and getting a Type is just rude.
			if (type(obj) is Type.__class__):
				continue

			if (name == varName):
				return obj, True

		return default, False
	

	def fetch_location_context(this, varName, default, fetchFrom, attempted):
		if (this.context is None):
			return default, False

		# We always want to search the context's members, but we don't want to propagate 'this' in the fetchFrom upstream of the context.
		# However, we must exclude values that E___ Functors will attempt to fetch, lest they propagate the last state forever.
		# We only need to check the optional values, since the required and static values are fewer and easier to manage (i.e. will be hard coded if necessary).
		if (varName not in this.context.arg.kw.optional.keys()):
			try:
				ret = getattr(this.context, varName)
				if (ret is not None):
					return ret, True
			except:
				pass
	
		return this.context.Fetch(varName, default, start=False, fetchFrom=fetchFrom,attempted=attempted)