import eons
import logging
import re
from .KEYWORD import KEYWORD
from .Exceptions import *
from .Sanitize import Sanitize

class E___ (KEYWORD):
	def __init__(this, name = eons.INVALID_NAME()):
		super().__init__(name)

		this.arg.kw.optional['shouldAutoType'] = False
		this.arg.kw.optional['unwrapReturn'] = None
		this.arg.kw.optional['currentlyTryingToDefine'] = None
		this.arg.kw.optional['currentlyTryingToInvoke'] = None
		this.arg.kw.optional['shouldAttemptInvokation'] = False

		this.HALT = False

	def BeforeFunction(this):
		super().BeforeFunction()
		this.HALT = False

	def Halt(this):
		logging.debug(f"Halting {this.name} ({id(this)}). Will return {this.result.data.returned}.")
		this.HALT = True
		raise HaltExecution(str(id(this)))
	
	def CorrectReferencesToThis(this, statement):
		if (this.currentlyTryingToInvoke is not None and 'currentlyTryingToInvoke' not in statement):
			# Regex copied from eons.kind
			statement = re.sub(r"this([\s\[\]\.\(\)\}}\*\+/-=%,]|$)", r"this.currentlyTryingToInvoke\1", statement)
		statement = re.sub(r"E____OBJECT", r"this", statement)
		return statement
	
	def AttemptEvaluationOfFunctor(this, statement):
		# Check if the statement is a Functor name.
		if (not re.search(rf"^{ElderLexer.NAME}$", statement)
			or statement in Sanitize.allBuiltins
		):
			return None, False
		
		logging.debug(f"It looks like {statement} is a Functor or variable name.")

		possibleFunctor = None
		if (this.context is not None):
			possibleFunctor = this.context.Fetch(statement)

		if (isinstance(possibleFunctor, Type.__class__)):
			# Same as below, just faster.
			possibleFunctor = possibleFunctor.product

		if (possibleFunctor is None):
			if (this.shouldAutoType):
				logging.debug(f"Autotyping {statement}.")
				ret = eval(f"Type(name = '{statement}', kind = Kind())", globals().update({'currentlyTryingToDefine': this.currentlyTryingToDefine}), {'this': this})
				return ret, True

			possibleFunctorName = statement

			if (this.currentlyTryingToDefine is not None):
				possibleFunctorName = f"{this.currentlyTryingToDefine}_{statement}"

			possibleFunctor = this.Fetch(statement)

			if (isinstance(possibleFunctor, Type.__class__)):
				possibleFunctor = possibleFunctor.product

			if (possibleFunctor is None):
				try:
					possibleFunctor = eons.SelfRegistering(possibleFunctorName)
				except:
					try:
						this.executor.GetRegistered(possibleFunctorName)
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
				return possibleFunctor(), True
			else:
				return possibleFunctor, True
