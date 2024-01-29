import eons
import logging
from .KEYWORD import KEYWORD
from .Exceptions import *

class E___ (KEYWORD):
	def __init__(this, name = eons.INVALID_NAME()):
		super().__init__(name)

		this.HALT = False

	def BeforeFunction(this):
		super().BeforeFunction()
		this.HALT = False

	def Halt(this):
		logging.debug(f"Halting {this.name} ({id(this)})")
		this.HALT = True
		raise HaltExecution(str(id(this)))