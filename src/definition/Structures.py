from .Structure import *
import eons

@eons.kind(AbstractStructure)
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

@eons.kind(AbstractStructure)
def Invokation(
	requiredBlocks = [
		'Name',
		'Parameter',
	]
):
	pass

@eons.kind(StrictStructure)
def SpaceAutofillNames(
	match = r'NAME\s+NAME',
	replace = r'AUTOFILL\(\1, \2\)',
	readDirection = '<',
):
	pass

@eons.kind(StrictStructure)
def SpaceAutofillAutofillAndName(
	match = r'Name\s+AUTOFILL\(.*?\)',
	replace = r'AUTOFILL\(\1, \2\)',
	readDirection = '<',
):
	pass

@eons.kind(StrictStructure)
def IfElse (
	match = r'\(PARAMETER\)\?{{EXECUTION}}{{EXECUTION}}',
	replace = r'if \(\1\): TABOUT\(\2\) TABOUT\(else:\) TABOUT\(\3\)',
):
	pass

@eons.kind(StrictStructure)
def If(
	match = r'\(PARAMETER\)\?{{EXECUTION}}',
	replace = r'if \(\1\): TABOUT\(\2\)',
):
	pass

@eons.kind(StrictStructure)
def For(
	match = r'NAME\[CONTAINER\]{{EXECUTION}}',
	replace = r'for \2 in \1: TABOUT\(\2\)',
):
	pass

@eons.kind(StrictStructure)
def While(
	match = r'\(CONTAINER\){{EXECUTION}}',
	replace = r'while \(\1\): TABOUT\(\2\)',
):
	pass

@eons.kind(StrictStructure)
def Sigil(
	match = r'\$NAME',
	replace = r'this.\1',
):
	pass

@eons.kind(StrictStructure)
def Not(
	match = r'!NAME',
	replace = r'not \1',
):
	pass

@eons.kind(StrictStructure)
def And(
	match = r'&',
	replace = r' and ',
):
	pass

@eons.kind(StrictStructure)
def DoubleAnd(
	match = r'&&',
	replace = r' and ',
):
	pass

@eons.kind(StrictStructure)
def Or(
	match = r'\|',
	replace = r' or ',
):
	pass

@eons.kind(StrictStructure)
def DoubleOr(
	match = r'\|\|',
	replace = r' or ',
):
	pass

@eons.kind(StrictStructure)
def Return(
	match = r'@',
	replace = r'return',
):
	pass