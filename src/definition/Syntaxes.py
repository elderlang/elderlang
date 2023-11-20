from .Syntax import *
import eons

@eons.kind(AbstractSyntax)
def Kind(
	requiredBlocks = [
		'Type',
		'Name',
		'Parameter',
	],
	optionalBlocks = [
		'Execution',
		'Execution',
		'BlockComment'
	],
):
	pass

@eons.kind(AbstractSyntax)
def Invokation(
	requiredBlocks = [
		'Name',
		'Parameter',
	]
):
	pass

@eons.kind(StrictSyntax)
def EOL(
	match = r'\\n',
	replace = r'\\n',
	readDirection = '<',
):
	pass

@eons.kind(StrictSyntax)
def Autofill(
	match = r'NAME[ +]NAME',
	replace = r'AUTOFILL\(\1, \2\)',
	readDirection = '<',
	excludeFromCatchAll = True,
):
	pass

@eons.kind(StrictSyntax)
def Sequence(
	match = r'NAME/NAME',
	replace = r'SEQUENCE\(\1, \2\)',
):
	pass

# @eons.kind(StrictSyntax)
# def SpaceAutofillAutofillAndName(
# 	match = r'NAME[ +]AUTOFILL\(.*?\)',
# 	replace = r'AUTOFILL\(\1, \2\)',
# 	readDirection = '<',
# 	excludeFromCatchAll = True,
# ):
# 	pass

@eons.kind(StrictSyntax)
def IfElse (
	match = r'\(PARAMETER\)\?{{EXECUTION}}{{EXECUTION}}',
	replace = r'if \(\1\): TABOUT\(\2\) TABOUT\(else:\) TABOUT\(\3\)',
):
	pass

@eons.kind(StrictSyntax)
def If(
	match = r'\(PARAMETER\)\?{{EXECUTION}}',
	replace = r'if \(\1\): TABOUT\(\2\)',
):
	pass

@eons.kind(StrictSyntax)
def For(
	match = r'NAME\[CONTAINER\]{{EXECUTION}}',
	replace = r'for \2 in \1: TABOUT\(\2\)',
):
	pass

@eons.kind(StrictSyntax)
def While(
	match = r'\(PARAMETER\){{EXECUTION}}',
	replace = r'while \(\1\): TABOUT\(\2\)',
):
	pass

# This is extraneous.
# @eons.kind(StrictSyntax)
# def Sigil(
# 	match = r'\$NAME',
# 	replace = r'this.\1',
# ):
# 	pass

# @eons.kind(StrictSyntax)
# def Not(
# 	match = r'!NAME',
# 	replace = r'not \1',
# ):
# 	pass

# @eons.kind(StrictSyntax)
# def And(
# 	match = r'&',
# 	replace = r' and ',
# ):
# 	pass

# @eons.kind(StrictSyntax)
# def DoubleAnd(
# 	match = r'&&',
# 	replace = r' and ',
# ):
# 	pass

# @eons.kind(StrictSyntax)
# def Or(
# 	match = r'\|',
# 	replace = r' or ',
# ):
# 	pass

# @eons.kind(StrictSyntax)
# def DoubleOr(
# 	match = r'\|\|',
# 	replace = r' or ',
# ):
# 	pass

# @eons.kind(StrictSyntax)
# def Return(
# 	match = r'@',
# 	replace = r'return',
# ):
# 	pass