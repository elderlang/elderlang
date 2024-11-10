import eons
import logging
from .LOOP import LOOP
from ..EVAL import EVAL
from ..EXEC import EXEC

class FOR (LOOP):
	def __init__(this):
		super().__init__(name = "FOR")

		this.arg.kw.required.append('parameter')
		this.arg.kw.required.append('container')
		this.arg.kw.required.append('execution')

		this.arg.mapping.append('parameter')
		this.arg.mapping.append('container')
		this.arg.mapping.append('execution')

	def Function(this):
		capture = ', '.join([f"{arg}={arg}" for arg in this.container])
		if (len(capture)):
			capture = f", {capture}"

		toExec = f"""\
for {', '.join(this.container)} in this.parameter:
	EXEC(this.execution{capture})
	if (this.BREAK):
		break
"""
		logging.debug(toExec)
		exec(toExec)
