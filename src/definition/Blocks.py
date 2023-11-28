from .Block import *
import eons

@eons.kind(Block)
def UnformattedString(
	openings = [r"\'"],
	closings = [r"\'"],
	representation = "\\'UNFORMATTED_STRING\\'", #NOT a raw string
	content = "FullExpressionSet",
):
	return str(this.p[1])

@eons.kind(Block)
def FormattedString(
	openings = [r'"', r'`'],
	closings = [r'"', r'`'],
	representation = '\"FORMATTED_STRING\"', #NOT a raw string
	content = "FullExpressionSet",
):
	return eval(f"f'{this.p[1]}'")

@eons.kind(Block)
def BlockComment(
	openings = [r'/\*'],
	closings = [r'\*/'],
	representation = r'/\*BLOCK_COMMENT\*/',
	content = "FullExpressionSet",
):
	return ""

@eons.kind(OpenEndedBlock)
def LineComment(
	openings = [r'#', r'//'],
	closings = [],
	representation = r'//LINE_COMMENT',
	content = "FullExpressionSet",
):
	return ""

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
	content = "LimitedExpressionSet",
):
	return "Namespace"

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
	doesSpaceClose = True,
	content = "LimitedExpressionSet",
):
	return "Type"

@eons.kind(Block)
def Parameter(
	openings = [r'\('],
	closings = [r'\)'],
	representation = r'\(PARAMETER\)',
	content = "FullExpressionSet",
):
	return "Parameter"

@eons.kind(Block)
def Execution(
	openings = [r'{'],
	closings = [r'}'],
	representation = r'{{EXECUTION}}',
	content = "FullExpressionSet",
):
	return "Execution"

@eons.kind(Block)
def Container(
	openings = [r'\['],
	closings = [r'\]'],
	representation = r'\[CONTAINER\]',
	content = "FullExpressionSet",
):
	return "Container"
