import eons
import logging
import re
from .E___ import E___
from .Exceptions import *

class EXEC (E___):
	def __init__(this):
		super().__init__(name="exec")
		this.arg.kw.required.append('execution')
		this.arg.mapping.append('execution')

		this.fetchFrom.insert(2, 'current_invokation')

		this.arg.kw.optional['currentlyTryingToInvoke'] = None

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
				this.result.data.execution.append(exec(instruction, globals()))
		except HaltExecution:
			this.PrepareReturn()
			return this.result.data.returned
		except Exception as e:
			failMessage = f"Error in execution of {this.execution}: {e}"
			logging.error(failMessage)
			eons.util.LogStack()

		this.executor.SetGlobal('context', this.episcope)

		if (failMessage is not None):
			raise RuntimeError(failMessage)

		this.PrepareReturn
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
				return default, False

			try:
				return this.currentlyTryingToInvoke.__getattribute__(varName), True
			except:
				if (this.episcope is None):
					return default, False
				return this.episcope.Fetch(varName, default, fetchFrom=fetchFrom, start=False, attempted=attempted)
		except:
			return default, False
