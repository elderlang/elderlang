import os
import logging
from pathlib import Path
from .lexer import *
from .parser import *
from .eldest.EXEC import EXEC
from .eldest.EVAL import EVAL
from .eldest.HOME import HOME
from .Sanitize import Sanitize
from .Executor import Executor

class ELDERLANG(Executor):

	def __init__(this, name="Eons Language of Development for Entropic Reduction (ELDER)", descriptionStr="The best programming language"):
		super().__init__(name, descriptionStr)

	#Override of eons.Executor method. See that class for details
	def AddArgs(this):
		super().AddArgs()
		this.arg.parser.add_argument(type = str, metavar = 'ldr', help = 'the Elderlang script to execute', dest = 'ldr')

	#Override of eons.Executor method. See that class for details
	def Function(this):
		super().Function()

		return this.ExecuteLDR(this.parsedArgs.ldr)