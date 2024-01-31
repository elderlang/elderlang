import eons
import logging
import re
import types
from .E___ import E___
from .Exceptions import *
from .Sanitize import Sanitize

class EVAL (E___):
	def __init__(this):
		super().__init__(name="eval")
		this.arg.kw.required.append('parameter')

		this.arg.kw.optional['unwrapReturn'] = None
		this.arg.kw.optional['shouldAutoType'] = False
		this.arg.kw.optional['shouldAttemptInvokation'] = False
		
		# used by Autofill
		this.arg.kw.optional['NEXTSOURCE'] = None

		this.arg.mapping.append('parameter')

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

				if (type(statement) in [int, float, bool]):
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

				# Check if the statement is a Functor name.
				if (re.search(rf"^{ElderLexer.NAME}$", statement)
					and statement not in Sanitize.allBuiltins
				):
					logging.debug(f"It looks like {statement} is a Functor or variable name.")
					possibleFunctor = this.context.Fetch(statement, None, fetchFrom = ['current_invokation'])

					if (possibleFunctor is None):
						if (this.shouldAutoType):
							logging.debug(f"Autotyping {statement}.")
							this.result.data.evaluation.append(eval(f"Type(name = '{statement}', kind = Kind())", globals(), {'this': this}))
						possibleFunctor = this.Fetch(statement)
						if (possibleFunctor is None):
							try:
								possibleFunctor = eons.SelfRegistering(statement)
							except:
								try:
									this.executor.GetRegistered(statement)
								except:
									pass

					if (possibleFunctor is not None):
						if (this.shouldAttemptInvokation 
		  					and (
								isinstance(possibleFunctor, eons.Functor)
								or isinstance(possibleFunctor, types.MethodType)
								or isinstance(possibleFunctor, types.FunctionType)
							)
						):
							logging.debug(f"Attempting to invoke {statement}.")
							this.result.data.evaluation.append(possibleFunctor())
						else:
							this.result.data.evaluation.append(possibleFunctor)
						continue

				# Detect & correct escape drift:
				# if (re.search(r"[^\\]\',", repr(statement))):
				# 	statement = re.sub(r"\',", "'", repr(statement))
				
				statement = this.CorrectForImproperQuotes(statement)

				logging.debug(f"Evaluating: {statement}")
				evaluation = eval(statement, globals(), {'this': this})
				if (isinstance(evaluation, types.MethodType) and this.shouldAttemptInvokation):
					evaluation = evaluation()
				this.result.data.evaluation.append(evaluation)

		except HaltExecution as halt:
			this.PrepareReturn()
			if (str(id(this)) == str(halt)):
				logging.debug(f"Passing on halt: {halt} ({id(this)})")
				raise halt
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
		if (this.unwrapReturn and len(this.result.data.evaluation)):
			this.result.data.returned = this.result.data.evaluation[0]
		else:
			this.result.data.returned = this.result.data.evaluation