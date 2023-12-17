from .Block import *
import eons

@eons.kind(SymmetricBlock)
def UnformattedString(
	openings = [r"\'"],
	representation = "\\'UNFORMATTED_STRING\\'", #NOT a raw string
	content = None
):
	# UnformattedStrings are lexed wholesale.
	return this.p[0]

@eons.kind(SymmetricBlock)
def FormattedString(
	openings = [r'"', r'`'],
	representation = '\"FORMATTED_STRING\"', #NOT a raw string
	content = "FullExpressionSet",
	nest = [
		'Execution',
	]
):
	return this.parent.Function(this)

@eons.kind(Block)
def BlockComment(
	openings = [r'/\*'],
	closings = [r'\*/'],
	representation = r'/\*BLOCK_COMMENT\*/',
	content = None,
	exclusions = ['parser'],
):
	pass

@eons.kind(OpenEndedBlock)
def LineComment(
	openings = [r'#', r'//'],
	closings = [],
	representation = r'//LINE_COMMENT',
	content = None,
	exclusions = ['parser'],
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
	content = "LimitedExpressionSet",
):
	return this.parent.Function(this)

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
	return this.parent.Function(this)

@eons.kind(Block)
def Parameter(
	openings = [r'\('],
	closings = [r'\)'],
	representation = r'\(PARAMETER\)',
	content = "FullExpressionSet",
):
	logging.critical(f"{this.name} executing function from {this.parent}")
	return this.parent.Function(this)

@eons.kind(Block)
def Execution(
	openings = [r'{'],
	closings = [r'}'],
	representation = r'{{EXECUTION}}',
	content = "FullExpressionSet",
):
	return this.parent.Function(this)

@eons.kind(Block)
def Container(
	openings = [r'\['],
	closings = [r'\]'],
	representation = r'\[CONTAINER\]',
	content = "FullExpressionSet",
):
	return this.parent.Function(this)
