import eons
import logging
import re
import types
from .E___ import E___
from .Exceptions import *

class EXEC (E___):
	def __init__(this):
		super().__init__(name="exec")
		this.fetchFrom.insert(2, 'current_invokation')

		this.arg.kw.required.append('execution')

		this.arg.kw.optional['shouldAttemptInvokation'] = True
		
		this.arg.mapping.append('execution')

		this.history = []

		this.episcope = None

		this.cloning.exclusions += [
			'episcope',
			'currentlyTryingToInvoke',
		]

	def Function(this):
		if (type(this.execution) != list):
			this.execution = [this.execution]

		this.episcope = None
		try:
			this.Set('episcope', context) # From globals
		except:
			pass

		this.executor.SetGlobal('context', this)

		this.result.data.execution = []

		failMessage = None
		try:
			for instruction in this.execution:
				logging.debug(instruction)
				instruction = this.CorrectReferencesToThis(instruction)
				evaluatedFunctor, wasFunctor = this.AttemptEvaluationOfFunctor(instruction)
				if (wasFunctor):
					this.result.data.execution.append(evaluatedFunctor)
					continue

				# eval instead of exec to grab result.
				result = eval(instruction, globals().update({'context': this}), {'this': this.currentlyTryingToInvoke, 'currentlyTryingToInvoke': this.currentlyTryingToInvoke})
				if (isinstance(result, types.MethodType)
					or isinstance(result, types.FunctionType)
					or (
						isinstance(result, eons.Functor)
						and not hasattr(result, 'EXEC_NO_EXECUTE')
					)
				):
					result = result()
				this.result.data.execution.append(result)

		except HaltExecution as halt:
			if (str(id(this)) != str(halt)):
				logging.debug(f"Passing on halt: {halt} ({id(this)})")
				raise halt
			logging.debug(f"Caught halt: {halt} ({id(this)})")
			this.PrepareReturn()
			return this.result.data.returned

		except Exception as e:
			failMessage = f"Error in execution of {this.execution}: {e}"
			logging.error(failMessage)
			eons.util.LogStack()

		this.executor.SetGlobal('context', this.episcope)

		if (failMessage is not None):
			raise RuntimeError(failMessage)

		this.PrepareReturn()
		return this.result.data.returned

	# NOTE: my return value should be set by RETURN as this.result.data.returned
	def PrepareReturn(this):
		if (this.result.data.returned is not None):
			return
		if (not len(this.result.data.execution)):
			return
		this.result.data.returned = this.result.data.execution[-1]

	def fetch_location_context(this, varName, default, fetchFrom, attempted):
		if (this.episcope is None):
			return default, False
		
		return this.episcope.Fetch(varName, default, fetchFrom=fetchFrom, start=False, attempted=attempted)

	def fetch_location_current_invokation(this, varName, default, fetchFrom, attempted):
		try:
			if (this.currentlyTryingToInvoke is None):
				if (this.episcope is None):
						return default, False
				return this.episcope.Fetch(varName, default, fetchFrom=fetchFrom, start=False, attempted=attempted)
			try:
				return this.currentlyTryingToInvoke.__getattribute__(varName), True
			except:
				if (this.episcope is None):
					return default, False
				return this.episcope.Fetch(varName, default, fetchFrom=fetchFrom, start=False, attempted=attempted)
		except:
			return default, False
