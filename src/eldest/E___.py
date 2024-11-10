import eons
import logging
import re
import sys
from .KEYWORD import KEYWORD
from .Exceptions import *

class E___ (KEYWORD):
	def __init__(this, name = eons.INVALID_NAME()):
		super().__init__(name)

		this.arg.kw.optional['unwrapReturn'] = None
		this.arg.kw.optional['shouldAutoType'] = True
		this.arg.kw.optional['currentlyTryingToDefine'] = None
		this.arg.kw.optional['currentlyTryingToInvoke'] = None
		this.arg.kw.optional['shouldAttemptInvokation'] = False

		this.fetch.possibilities.append('current_invokation')

		this.fetch.attr.use = []

		this.fetch.useForFunctorEval = [
			'args', # used in for loops, etc.
			'this',
			'current_invokation',
			'history',
			'context',
			'executor',
			'globals'
		]

		this.prevent.copying.extend([
			'currentlyTryingToInvoke',
		])

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
			or statement in this.executor.sanitize.allBuiltins
		):
			return None, False

		logging.debug(f"It looks like {statement} is a Functor or variable name.")

		possibleFunctor = None
		attemptedFetch = False
		if (this.context is not None):
			possibleFunctor = this.Fetch(statement, fetchFrom=this.fetch.useForFunctorEval)
			attemptedFetch = True

		if (possibleFunctor is None):
			if (this.shouldAutoType): #TODO: Why don't we try to Observe the Functor before creating it?
				logging.debug(f"Autotyping {statement}.")
				ret = eval(f"Type(name = '{statement}', kind = Kind())", globals().update({'currentlyTryingToDefine': this.currentlyTryingToDefine}), {'this': this})
				return ret, True

			possibleFunctorName = statement

			if (this.currentlyTryingToDefine is not None):
				possibleFunctorName = f"{this.currentlyTryingToDefine}_{statement}"
				attemptedFetch = False

			if (not attemptedFetch):
				possibleFunctor = this.Fetch(possibleFunctorName, fetchFrom=this.fetch.useForFunctorEval)

			if (possibleFunctor is None):
				try:
					possibleFunctor = eons.SelfRegistering(possibleFunctorName)
				except:
					try:
						possibleFunctor = this.executor.Observe(possibleFunctorName)
					except:
						try:
							possibleFunctor = sys.modules[possibleFunctorName]
						except:
							pass

		if (possibleFunctor is not None):
			if (isinstance(possibleFunctor, Type.__class__)):
				possibleFunctor = possibleFunctor.product

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

	def fetch_location_current_invokation(this, varName, default, fetchFrom, attempted):
		try:
			if (this.currentlyTryingToInvoke is None):
				if (this.episcope is None):
					return default, False
				return this.episcope.Fetch(varName, default, fetchFrom=fetchFrom, start=False, attempted=attempted)
			try:
				return getattr(this.currentlyTryingToInvoke, varName), True
			except:
				if (this.episcope is None):
					return default, False
				return this.episcope.Fetch(varName, default, fetchFrom=fetchFrom, start=False, attempted=attempted)
		except:
			return default, False