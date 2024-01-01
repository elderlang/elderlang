from ..KEYWORD import KEYWORD
from ..EVAL import EVAL
from ..EXEC import EXEC

class SWITCH (KEYWORD):
	def __init__(this):
		super().__init__(name = "switch")

		this.arg.kw.required.append('condition')
		this.arg.kw.required.append('execution')

	def Function(this):
		this.matched = None