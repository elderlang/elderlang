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
	nest = [
		'Execution',
	],
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
def Namespace(
	openings = [r':'],
	closings = [
		'UnformattedString',
		'FormattedString',
		'LineComment',
		'Parameter',
		'Type',
	],
	representation = r':NAMESPACE',
	recurse = True,
	nest = [
		'BlockComment',
		'Execution',
		'Container',
	]
):
	pass

@eons.kind(OpenEndedBlock)
def Expression(
	openings = [r';', r','],
	closings = [
		'LineComment',
	],
	representation = r'EXPRESSION',
	recurse = True,
	nest = [
		'UnformattedString',
		'FormattedString',
		'BlockComment',
		'Namespace',
		'Type',
		'Parameter',
		'Execution',
		'Container',
		'Name',
	]
):
	pass

@eons.kind(OpenEndedBlock)
def Type(
	openings = [r'~'],
	closings = [
		'UnformattedString',
		'FormattedString',
		'LineComment',
		'Parameter',
	],
	representation = r'~TYPE',
	recurse = True,
	doesSpaceClose = True,
	nest = [
		'Expression',
	],
):
	pass

@eons.kind(Block)
def Parameter(
	openings = [r'\('],
	closings = [r'\)'],
	representation = r'\(PARAMETER\)',
	recurse = True,
	nest = [
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
	specialStarts = [
		'/',
	],
):
	pass
