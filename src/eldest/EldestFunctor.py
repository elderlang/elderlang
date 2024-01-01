import eons
import logging

class EldestFunctor (eons.Functor):
	def __init__(this, name=eons.INVALID_NAME()):
		super().__init__(name)

		this.arg.kw.optional['context'] = None

		this.feature.autoReturn = False

		this.fetch.use = [
			'this',
			'args',
			'stack',
			'globals',
			# 'config', #local (if applicable) or per Executor; should be before 'executor' if using a local config.
			# 'precursor',
			# 'caller',
			# 'executor',
			# 'environment',
		]

	def BeforeFunction(this):
		this.executor.stack.append(
			(this.name, this)
		)
		logging.debug(f"Stack is now: {this.executor.stack}")

		if (this.context is None):
			this.context = this.executor.context

	def AfterFunction(this):
		this.executor.stack.remove(
			(this.name, this)
		)
		logging.debug(f"Stack is now: {this.executor.stack}")


	def fetch_location_stack(this, varName, default, fetchFrom, attempted):
		stack = this.executor.stack.copy()
		stack.reverse()
		for name, object in stack:
			if (name == varName):
				return object, True
		return default, False