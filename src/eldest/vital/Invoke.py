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

		this.feature.mapArgs = False

	def Function(this):
		isFunctor = isinstance(this.source, eons.Functor)
		if (isFunctor):
			this.context.currentlyTryingToInvoke = this.source

		evaluatedParameter = []
		if (this.parameter is not None):
			evaluatedParameter = EVAL(this.parameter, shouldAttemptInvokation = True)

			if (not isinstance(evaluatedParameter, list)):
				evaluatedParameter = [evaluatedParameter]

		logging.debug(f"Invoking {this.source} with {evaluatedParameter}")

		if (isFunctor):
			return this.source(*evaluatedParameter, container=this.container, execution=this.execution)
		else:
			return this.source(*evaluatedParameter)