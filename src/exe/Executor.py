import os
import logging
import eons
from pathlib import Path
from .lexer import *
from .parser import *
from .eldest.EXEC import EXEC
from .eldest.EVAL import EVAL
from .eldest.HOME import HOME
from .Sanitize import Sanitize

class Executor(eons.Executor):

	def __init__(this, name="Eons Language of Development for Entropic Reduction (ELDER)", descriptionStr="Elder is the best programming language"):
		super().__init__(name, descriptionStr)
		this.elder = this # Per eons.Executor, making *this "elder-enabled".

		this.lexer = ElderLexer()
		this.parser = ElderParser()
		this.parser.executor = this

		this.stack = []
		this.exceptions = []
		this.context = None

		# For external access (these are pulled from globals, not import)
		this.EXEC = EXEC
		this.EVAL = EVAL
		this.sanitize = Sanitize()

	# Register included files early so that they can be used by the rest of the system.
	# NOTE: this method needs to be overridden in all children which ship included Functors, Data, etc. This is because __file__ is unique to the eons.py file, not the child's location.
	def RegisterIncludedClasses(this):
		super().RegisterIncludedClasses()

	#Configure class defaults.
	#Override of eons.Executor method. See that class for details
	def Configure(this):
		super().Configure()

	#Override of eons.Executor method. See that class for details
	def Function(this):
		super().Function()

	# Lex, Parse, and Execute the given .ldr file
	def ExecuteLDR(this, file):

		ldrFile = open(file, 'r')
		ldr = ldrFile.read()
		ldrFile.close()
		
		# for tok in this.lexer.tokenize(ldr):
		# 	logging.info(tok)

		toExec = this.parser.parse(this.lexer.tokenize(ldr))

		return EXEC(toExec, executor=this, home=HOME.Instance())