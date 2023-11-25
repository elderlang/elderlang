import eons
import logging
import re
from .Blocks import *
from .Summary import summary

class GenParser(eons.Functor):

	def	__init__(this, name = "Sly Parser Generator"):
		super().__init__(name)

		this.requiredKWArgs.append('gen_lexer')

		this.optionalKWArgs['outFileName'] = "parser.py"

	def Function(this):
		this.grammar = {}

		for block in this.gen_lexer.blocks:
			syntax = f"OPEN_{block.name.upper()} contents CLOSE_{block.name.upper()}"
			this.grammar[block] = syntax

		
		