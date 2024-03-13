import eons
import logging
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
			this.source = EVAL([this.source], unwrapReturn = True)[0]

		isFunctor = isinstance(this.source, eons.Functor)
		if (isFunctor):
			this.context.currentlyTryingToInvoke = this.source

		shouldEvaluateParameter = True
		if (isFunctor and this.source.name in this.skipParameterEvaluationFor):
			shouldEvaluateParameter = False

		evaluatedParameter = [this.parameter] # should be double nested list

		if (this.parameter is None or not len(this.parameter) or this.parameter == [[]]):
			shouldEvaluateParameter = False
			evaluatedParameter = []

		if (shouldEvaluateParameter):
			evaluatedParameter, unwrapped = EVAL(this.parameter, shouldAttemptInvokation = True)

			if (unwrapped):
				evaluatedParameter = [evaluatedParameter]

		logging.debug(f"Invoking {this.source} with {evaluatedParameter}")

		if (isFunctor):
			return this.source(*evaluatedParameter, container=this.container, execution=this.execution)
		else:
			return this.source(*evaluatedParameter)