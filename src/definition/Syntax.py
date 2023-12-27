import eons
from .Structure import *

@eons.kind(Structure)
def Syntax():
	pass

@eons.kind(Syntax)
def ExactSyntax(
	match = r'',
	literalMatch = False,
	recurseOn = None,
	readDirection = ">"
):
	pass

@eons.kind(ExactSyntax)
def FlexibleTokenSyntax(
	match = [],
	exclusions = [
		'lexer',
		'all.catch.block'
	],
):
	pass

@eons.kind(Syntax)
def BlockSyntax(
	blocks = [],
):
	pass

@eons.kind(BlockSyntax)
def Invokation():
	pass