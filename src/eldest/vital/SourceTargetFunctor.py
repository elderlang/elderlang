import eons
from ..EldestFunctor import EldestFunctor
from ..EVAL import EVAL
from ..EXEC import EXEC

class SourceTargetFunctor (EldestFunctor):
	def __init__(this, name="Call"):
		super().__init__(name)

		this.nameStack = [name]

		this.needs.source = True
		this.needs.target = True

		this.feature.mapArgs = False

	def BeforeFunction(this):
		if (this.needs.source):
			this.Set('name', f"source_name_{this.Fetch('name', None, ['args'])}")
			possibleSource = this.Fetch('source', None, ['args'])
			if (hasattr(this, 'source') and this.source is not None):
				possibleSource = this.source
			elif (this.name != 'source_name_None'):
				possibleSource = EVAL(this.name[len('source_name_'):], shouldAutoType=False)[0]
			else:
				if (len(this.args)):
					possibleSource = this.args[0]
				if (possibleSource is None):
					raise RuntimeError(f"Neither source nor name was provided to {this.nameStack[-1]}")
				elif (isinstance(possibleSource, str)):
					possibleSource = EVAL(possibleSource, shouldAutoType=False)[0]

		if (isinstance(possibleSource, Type.__class__)):
			possibleSource = possibleSource.product

		this.Set('source', possibleSource)

		# Not strictly necessary, but useful for keeping the nameStack indices static/
		this.nameStack.append(this.name)

		if (this.needs.target):
			possibleTarget = this.Fetch('target', None, ['args'])

			if (hasattr(this, 'target') and this.target is not None):
				possibleTarget = this.target
			else:
				if (len(this.args) > 1):
					possibleTarget = this.args[1:]
				else:
					raise RuntimeError(f"Target was not provided to {this.nameStack[-2]}")

			if (not isinstance(possibleTarget, list)):
				possibleTarget = [possibleTarget]

			this.Set('target', possibleTarget)

		super().BeforeFunction()

	def AfterFunction(this):
		this.name = this.nameStack.pop()
		super().AfterFunction()
