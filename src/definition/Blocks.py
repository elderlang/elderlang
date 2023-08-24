from .Block import *
import eons

@eons.kind(Block)
def UnformattedString(
	openings = [r"\'"],
	closings = [r"\'"],
	representation = "\\'UNFORMATTED_STRING\\'", #NOT a raw string
):
	pass

@eons.kind(Block)
def FormattedString(
	openings = [r'"', r'`'],
	closings = [r'"', r'`'],
	representation = '\"FORMATTED_STRING\"', #NOT a raw string
):
	pass

@eons.kind(Block)
def BlockComment(
	openings = [r'/\*'],
	closings = [r'\*/'],
	representation = r'/\*BLOCK_COMMENT\*/',
):
	pass

@eons.kind(OpenEndedBlock)
def LineComment(
	openings = [r'#', r'//'],
	closings = [],
	representation = r'//LINE_COMMENT',
):
	pass

@eons.kind(OpenEndedBlock)
def GlobalNamespace(
	openings = [r'::'],
	closings = [
		'LineComment',
		'BlockComment',
		'LocalNamespace'
	],
	representation = r'::GLOBAL_NAMESPACE',
	recurse = True,
	nest = [
		'Expression',
	]
):
	pass

@eons.kind(OpenEndedBlock)
def LocalNamespace(
	openings = [r':'],
	closings = [
		'LineComment',
		'BlockComment',
	],
	representation = r':LOCAL_NAMESPACE',
	recurse = True,
	nest = [
		'Expression',
	]
):
	pass

@eons.kind(OpenEndedBlock)
def Expression(
	openings = [r'^', r';', r','],
	closings = [
		'LineComment',
		'BlockComment',
	],
	representation = r'EXPRESSION',
	recurse = True,
	nest = [
		'String',
		'BlockComment',
		'GlobalNamespace',
		'LocalNamespace',
		'Name',
		'Parameter',
		'Execution',
		'Container',
	]
):
	pass

@eons.kind(Block)
def Type(
	openings = [r'<'],
	closings = [r'>'],
	representation = r'<TYPE>',
	recurse = True,
	nest = [
		'Type',
		'Expression',
	]
):
	pass

@eons.kind(Block)
def Parameter(
	openings = [r'\('],
	closings = [r'\)'],
	representation = r'\(PARAMETER\)',
	recurse = True,
	nest = [
		'Type',
		'Expression',
	],
):
	pass

@eons.kind(Block)
def Execution(
	openings = [r'{'],
	closings = [r'}'],
	representation = r'{{EXECUTION}}',
	recurse = True,
	nest = [
		'Type',
		'Expression',
	]
):
	pass

@eons.kind(Block)
def Container(
	openings = [r'\['],
	closings = [r'\]'],
	representation = r'\[CONTAINER\]',
	recurse = True,
	nest = [
		'Expression',
	]
):
	pass

@eons.kind(CatchAllBlock)
def Name(
	representation = r'NAME',
):
	pass
