import eons
import logging
import re
from .E___ import E___
from .Exceptions import *

class EVAL (E___):
	def __init__(this):
		super().__init__(name="eval")
		this.arg.kw.required.append('parameter')

		this.arg.kw.optional['unwrapReturn'] = None

		this.arg.mapping.append('parameter')

	def Function(this):
		if (this.unwrapReturn is None and type(this.parameter) != list):
			this.unwrapReturn = True
			this.parameter = [this.parameter]

		this.result.data.evaluation = []
		
		failMessage = None
		try:
			for statement in this.parameter:

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
				if (re.match(r'^[0-9]+$', statement)):
					this.result.data.evaluation.append(int(statement))
					continue

				# Check if the statement is a float.
				if (re.match(r'^[0-9]+\.[0-9]+$', statement)):
					this.result.data.evaluation.append(float(statement))
					continue

				# Check if the statement is a string.
				# At this point, all strings should be wrapped in single quotes only.
				if ((statement.startswith("'") and statement.endswith("'"))):
					this.result.data.evaluation.append(statement[1:-1])
					continue
				
				# Check if the statement is a Functor name.
				if (re.match(r'^[a-zA-Z0-9_]+$', statement) 
					and statement not in [
						'BREAK',
						'CASE',
						'CATCH',
						'CONTINUE',
						'DEFAULT',
						'ELSE',
						'FOR',
						'IF',
						'RETURN',
						'SWITCH',
						'TRY',
						'WHILE',
					]
				):
					try:
						this.result.data.evaluation.append(this.executor.GetRegistered(statement))
						continue
					except:
						pass
					
				this.result.data.evaluation.append(eval(statement, globals(), {'this': this}))

		except HaltExecution:
			this.PrepareReturn()
			return this.result.data.returned

		except Exception as e:
			failMessage = f"Error in evaluation of {this.parameter}: {e}"
			logging.error(failMessage)
			eons.util.LogStack()

		if (failMessage is not None):
			raise RuntimeError(failMessage)
		
		this.PrepareReturn()

		return this.result.data.returned

	def PrepareReturn(this):
		if (this.unwrapReturn):
			this.result.data.returned = this.result.data.evaluation[0]
		else:
			this.result.data.returned = this.result.data.evaluation