import eons
from ..EldestFunctor import EldestFunctor
from ..TYPE import TYPE
from ..EVAL import EVAL
from ..EXEC import EXEC

class Kind (EldestFunctor):
	def __init__(this, name="Kind"):
		super().__init__(name)

		this.arg.kw.optional['kind'] = None

		this.arg.mapping.append('kind')

	def Function(this):
		if (this.kind is None):
			this.kind = [TYPE]
		elif (isinstance(this.kind, str)):
			this.kind = EVAL([this.kind], unwrapReturn=True)[0]

		if (type(this.kind) != list):
			this.kind = [this.kind]

		# We shouldn't need to actually do anything here.

		return this.kind
