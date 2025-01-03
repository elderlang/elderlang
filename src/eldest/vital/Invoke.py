import eons
import logging
import types
from .SourceTargetFunctor import SourceTargetFunctor
from ..EVAL import EVAL
from ..EXEC import EXEC

class Invoke (SourceTargetFunctor):
	def __init__(this, name="Invoke"):
		super().__init__(name)

		this.needs.target = False

		this.arg.kw.optional['parameter'] = None
		this.arg.kw.optional['container'] = None
		this.arg.kw.optional['execution'] = None

		this.arg.kw.optional['skipParameterEvaluationFor'] = [
			'WHILE'
		]

		this.feature.mapArgs = False

	def Function(this):
		if (isinstance(this.source, str)):
			this.source = EVAL([this.source], unwrapReturn=True, shouldAutoType=False)[0]

		isFunctor = isinstance(this.source, eons.Functor)
		if (isFunctor and not isinstance(this.source, KEYWORD)):
			this.context.currentlyTryingToInvoke = this.source

		shouldEvaluateParameter = True
		if (isFunctor and this.source.name in this.skipParameterEvaluationFor):
			shouldEvaluateParameter = False

		evaluatedParameter = [this.parameter] # should be double nested list

		if (this.parameter is None or not len(this.parameter) or this.parameter == [[]]):
			shouldEvaluateParameter = False
			evaluatedParameter = []

		if (shouldEvaluateParameter):
			evaluatedParameter, unwrapped = EVAL(this.parameter, shouldAutoType=False, shouldAttemptInvokation=True)

			if (unwrapped):
				evaluatedParameter = [evaluatedParameter]

		# Happens if the source was invoked during EVAL.
		if (this.source is None):
			return evaluatedParameter

		logging.debug(f"Invoking {this.source} with {evaluatedParameter}")

		if (isFunctor):
			return this.source(*evaluatedParameter, container=this.container, execution=this.execution)

		# Support Elder -> Python casting
		elif (isinstance(this.source, types.BuiltinFunctionType)):
			if (not isinstance(evaluatedParameter[0], CONTAINER)):
				raise RuntimeError(f"Cannot call {this.source} with {evaluatedParameter[0]}: not a container.")
			if (type(this.source) is type(dict.update)):
				return this.source(evaluatedParameter[0].__dict__())
			if (type(this.source) is type(list.extend)):
				return this.source(evaluatedParameter[0].__list__())

			else:
				raise RuntimeError(f"Cannot call {this.source} with {evaluatedParameter[0]}: not supported.")

		else:
			return this.source(*evaluatedParameter)