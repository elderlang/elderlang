import os
import logging
import eons
from pathlib import Path
from .lexer import *
from .parser import *
from .eldest.EXEC import EXEC
from .eldest.EVAL import EVAL
from .eldest.Sanitize import Sanitize

class ELDERLANG(eons.Executor):

	def __init__(this, name="Eons Language of Development for Entropic Reduction (ELDER)", descriptionStr="The best programming language"):
		super().__init__(name, descriptionStr)

		this.lexer = ElderLexer()
		this.parser = ElderParser()

		this.stack = []
		this.exceptions = []
		this.history = []
		this.context = None

		# For external access (these are pulled from globals, not import)
		this.EXEC = EXEC
		this.EVAL = EVAL
		this.Sanitize = Sanitize()

	# Register included files early so that they can be used by the rest of the system.
	# NOTE: this method needs to be overridden in all children which ship included Functors, Data, etc. This is because __file__ is unique to the eons.py file, not the child's location.
	def RegisterIncludedClasses(this):
		super().RegisterIncludedClasses()

	#Configure class defaults.
	#Override of eons.Executor method. See that class for details
	def Configure(this):
		super().Configure()

	#Override of eons.Executor method. See that class for details
	def AddArgs(this):
		super().AddArgs()
		this.arg.parser.add_argument(type = str, metavar = 'ldr', help = 'the Elderlang script to execute', dest = 'ldr')

	#Override of eons.Executor method. See that class for details
	def Function(this):
		super().Function()
		
		ldrFile = open(this.parsedArgs.ldr, 'r')
		ldr = ldrFile.read()
		ldrFile.close()
		
		toExec = this.parser.parse(this.lexer.tokenize(ldr))
		toExec = this.Sanitize(toExec).returned
		logging.info(f"Sanitized: {toExec}")
		return EXEC(toExec, executor=this)