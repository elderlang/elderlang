import eons
from ..EldestFunctor import EldestFunctor
from ..EVAL import EVAL
from ..EXEC import EXEC

class SourceTargetFunctor (EldestFunctor):
	def __init__(this, name="Call"):
		super().__init__(name)

		this.nameStack = [name]

		this.needs = eons.util.DotDict()
		this.needs.source = True
		this.needs.target = True

		this.feature.mapArgs = False

	def BeforeFunction(this):
		if (this.needs.source):
			this.Set('name', f"source_name_{this.Fetch('name', None, ['args'])}")
			this.Set('source', this.Fetch('source', None, ['args']))
			if (this.source is not None):
				pass
			elif (this.source is None and this.name != 'source_name_None'):
				this.Set('source', EVAL(this.name[len('source_name_'):]))
			else:
				possibleSource = None
				if (len(this.args)):
					possibleSource = this.args[0]
				if (possibleSource is None):
					raise RuntimeError(f"Neither source nor name was provided to {this.nameStack[-1]}")
				elif (isinstance(possibleSource, str)):
					this.Set('source', EVAL(possibleSource))
				else:
					this.Set('source', possibleSource)

		# Not strictly necessary, but useful for keeping the nameStack indices static/
		this.nameStack.append(this.name)

		if (this.needs.target):
			this.Set('target', this.Fetch('target', None, ['args']))

			if (this.target is None):
				if (len(this.args) > 1):
					this.Set('target', this.args[1:])
				else:
					raise RuntimeError(f"Target was not provided to {this.nameStack[-2]}")
			if (not isinstance(this.target, list)):
				this.Set('target', [this.target])

		super().BeforeFunction()

	def AfterFunction(this):
		this.name = this.nameStack.pop()
		super().AfterFunction()
