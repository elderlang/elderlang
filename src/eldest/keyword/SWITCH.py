from ..KEYWORD import KEYWORD
from ..EVAL import EVAL
from ..EXEC import EXEC

class SWITCH (KEYWORD):
	def __init__(this):
		super().__init__(name = "SWITCH")

		this.arg.kw.required.append('condition')
		this.arg.kw.required.append('execution')

		this.arg.mapping.append('condition')
		this.arg.mapping.append('execution')

	def Function(this):
		this.matched = None