import eons
from ..EldestFunctor import EldestFunctor
from ..EVAL import EVAL
from ..EXEC import EXEC

class SourceTargetFunctor (EldestFunctor):
	def __init__(this, name="Call"):
		super().__init__(name)

		this.nameStack = [name]

		this.feature.mapArgs = False

	def BeforeFunction(this):
		this.Set('name', f"source_name_{this.Fetch('name', None, ['args'])}")
		this.Set('source', this.Fetch('source', None, ['args']))
		this.Set('target', this.Fetch('target', None, ['args']))

		this.nameStack.append(this.name)

		if (this.source is not None):
			pass
		elif (this.source is None and this.name is not None):
			this.source = EVAL(this.name[len('source_name_'):])
		else:
			possibleSource = None
			if (len(this.args)):
				possibleSource = this.args[0]
			if (possibleSource is None):
				raise RuntimeError(f"Neither source nor name was provided to {this.name}")
			elif (isinstance(possibleSource, str)):
				this.source = EVAL(possibleSource)
			else:
				this.source = possibleSource

		super().BeforeFunction()

	def AfterFunction(this):
		this.name = this.nameStack.pop()
		super().AfterFunction()
