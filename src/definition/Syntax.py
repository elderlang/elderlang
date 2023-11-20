import eons
from .Structure import *

@eons.kind(Structure)
def Syntax(
	allowInBlocks = [
		'Execution'
	],
):
	pass

@eons.kind(Syntax)
def StrictSyntax(
	match = r'',
	replace = r'',
	readDirection = '>',
):
	pass

@eons.kind(Syntax)
def AbstractSyntax(
	requiredBlocks = [],
	optionalBlocks = [],
):
	pass