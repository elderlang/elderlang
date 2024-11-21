import eons
import logging
import re
import types
from .E___ import E___
from .Exceptions import *

class EXEC (E___):
	def __init__(this):
		super().__init__(name="exec")

		this.arg.kw.required.append('execution')

		this.arg.kw.optional['shouldAutoType'] = False
		this.arg.kw.optional['shouldAttemptInvokation'] = True
		this.arg.kw.optional['home'] = None
		
		this.arg.mapping.append('execution')

		this.history = []

		this.episcope = None

		this.prevent.copying.extend([
			'episcope',
			'currentlyTryingToInvoke',
		])


	# Since we use episcope in Fetch, we have to set it before validating args.
	# This is not a perfect hook location for this logic, but it should work fine.
	def PopulatePrecursor(this):
		super().PopulatePrecursor()

		this.episcope = None
		try:
			this.Set('episcope', context) # From globals
		except:
			pass


	def Function(this):
		if (this.home is not None):
			logging.debug(f"Setting {id(this)} ({this}) as home.")
			this.home.exec = this

		if (type(this.execution) != list):
			this.execution = [this.execution]

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


	# This is the same as the EldestFunctor fetch_location_context method, but uses 'episcope' instead of 'context'.
	# Thus, one context may propagate the contextual search outward.
	def fetch_location_context(this, varName, default, fetchFrom, attempted):
		if (this.episcope is None):
			return default, False

		if (varName not in this.episcope.arg.kw.optional.keys()):
			try:
				ret = getattr(this.episcope, varName)
				if (ret is not None):
					return ret, True
			except:
				pass

		return this.episcope.Fetch(varName, default, fetchFrom=fetchFrom, start=False, attempted=attempted)
