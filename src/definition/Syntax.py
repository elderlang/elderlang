import eons
from .Structure import *

@eons.kind(Structure)
def Syntax():
	pass

@eons.kind(Syntax)
def StrictSyntax(
	match = r'',
	literalMatch = False,
	noToken = False,
	recurseOn = "",
	readDirection = ">"
):
	pass

@eons.kind(Syntax)
def AbstractSyntax(
	blocks = [],
):
	pass

@eons.kind(AbstractSyntax)
def Invokation():
	pass