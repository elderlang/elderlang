from .LOOP import LOOP
from ..EVAL import EVAL
from ..EXEC import EXEC

class FOR (LOOP):
	def __init__(this):
		super().__init__(name = "for")

		this.arg.kw.required.append('source')
		this.arg.kw.required.append('container')
		this.arg.kw.required.append('execution')

	def Function(this):
		exec(f"""\
for {this.container[1:-1]} in this.source:
	EXEC(this.execution)
	if (this.BREAK):
		break
""")
