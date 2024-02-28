import eons
from .Structure import *

@eons.kind(Structure)
def Syntax():
	pass

@eons.kind(Syntax)
def ExactSyntax(
	match = r'',
	# literalMatch = False,
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

@eons.kind(FlexibleTokenSyntax)
def OperatorOverload():
	args = {
		'name': this.p[0],
		'kind': this.Engulf(this.p[1]),
		'parameter': None,
		'execution': None,
	}
	if (len(this.p) == 3):
		args['execution'] = this.Engulf(this.p[2])
	elif (len(this.p) == 4):
		args['parameter'] = this.Engulf(this.p[2])
		args['execution'] = this.Engulf(this.p[3])

	argString = ','.join([f'{k}={v}' for k, v in args.items()])

	return f"Type({argString})"