import eons
import logging
import types
from .E___ import E___
from .Exceptions import *

class EVAL (E___):
	def __init__(this):
		super().__init__(name="eval")
		this.arg.kw.required.append('parameter')

		# used by Autofill
		this.arg.kw.optional['NEXTSOURCE'] = None

		this.arg.mapping.append('parameter')

		this.prevent.copying.extend([
			'NEXTSOURCE',
		])

	def Function(this):
		if (this.unwrapReturn is None):
			if (type(this.parameter) != list):
				this.unwrapReturn = True
				this.parameter = [this.parameter]
			if (type(this.parameter) == list and len(this.parameter) == 1):
				this.unwrapReturn = True

		this.result.data.evaluation = []
		
		failMessage = None
		try:
			for statement in this.parameter:

				# Dereference pointers, but otherwise continue.
				if (isinstance(statement, POINTER)):
					statement = statement()

				if (type(statement) in [int, float, bool]):
					this.result.data.evaluation.append(statement)
					continue

				if (isinstance(statement, CONTAINER)):
					this.result.data.evaluation.append(statement)
					continue

				if (statement == 'true' or statement == 'True'):
					this.result.data.evaluation.append(True)
					continue

				if (statement == 'false' or statement == 'False'):
					this.result.data.evaluation.append(False)
					continue

				if (statement == 'null' or statement == 'Null'
					or statement == 'none' or statement == 'None'
					or statement == 'void' or statement == 'Void'
				):
					this.result.data.evaluation.append(None)
					continue

				# Check if the statement is an integer.
				if (re.search(r'^[0-9]+$', statement)):
					this.result.data.evaluation.append(int(statement))
					continue

				# Check if the statement is a float.
				if (re.search(r'^[0-9]+\.[0-9]+$', statement)):
					this.result.data.evaluation.append(float(statement))
					continue

				# Check if the statement is a string.
				# At this point, all strings should be wrapped in single quotes only.
				if ((statement.startswith("'") and statement.endswith("'"))):
					this.result.data.evaluation.append(statement[1:-1])
					continue

				statement = this.CorrectReferencesToThis(statement)

				evaluatedFunctor, wasFunctor = this.AttemptEvaluationOfFunctor(statement)
				if (wasFunctor):
					this.result.data.evaluation.append(evaluatedFunctor)
					continue

				statement = this.CorrectForImproperQuotes(statement)

				logging.debug(f"Evaluating: {statement}")
				evaluation = eval(statement, globals().update({'currentlyTryingToDefine': this.currentlyTryingToDefine, 'currentlyTryingToInvoke': this.currentlyTryingToInvoke}), {'this': this})
				if (isinstance(evaluation, types.MethodType) and this.shouldAttemptInvokation):
					evaluation = evaluation()
				this.result.data.evaluation.append(evaluation)

		except HaltExecution as halt:
			if (str(id(this)) != str(halt)):
				logging.debug(f"Passing on halt: {halt} ({id(this)})")
				raise halt
			this.PrepareReturn()
			logging.debug(f"Caught halt: {halt} ({id(this)})")
			return this.result.data.returned, this.unwrapReturn

		except Exception as e:
			failMessage = f"Error in evaluation of {this.parameter}: {e}"
			logging.error(failMessage)
			eons.util.LogStack()

		if (failMessage is not None):
			raise RuntimeError(failMessage)

		this.PrepareReturn()

		return this.result.data.returned, this.unwrapReturn

	def PrepareReturn(this):
		if (this.result.data.returned is not None):
			return
		
		if (this.unwrapReturn and len(this.result.data.evaluation)):
			this.result.data.returned = this.result.data.evaluation[0]
		else:
			this.result.data.returned = this.result.data.evaluation