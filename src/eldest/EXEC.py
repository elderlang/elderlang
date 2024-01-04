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

		failMessage = None
		try:
			for instruction in this.execution:
				logging.debug(instruction)
				exec(instruction, globals())
		except HaltExecution:
			return this.result.data.returned
		except Exception as e:
			failMessage = f"Error in execution of {this.execution}: {e}"
			logging.error(failMessage)
			eons.util.LogStack()

		this.executor.SetGlobal('context', this.episcope)

		if (failMessage is not None):
			raise RuntimeError(failMessage)

		# NOTE: my return value should be set by RETURN.
		return this.result.data.returned
	
	
	def fetch_location_context(this, varName, default, fetchFrom, attempted):
		if (this.episcope is None):
			return default, False
		
		return this.episcope.Fetch(varName, default, start=False, attempted=attempted)