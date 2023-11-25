import eons
from .Structure import *

@eons.kind(Structure)
def Syntax(
	allowInBlocks = [
		'Expression'
	],
):
	pass

@eons.kind(Syntax)
def StrictSyntax(
	match = r'',
	recurse = False,
):
	pass

@eons.kind(Syntax)
def AbstractSyntax(
	blocks = [],
):
	pass