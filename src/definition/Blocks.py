from .Block import *
import eons

@eons.kind(CatchAllBlock)
def Name(
	representation = r'NAME',
	specialStarts = [
		'/',
	],
):
	pass

@eons.kind(DefaultBlock)
def Expression(
	openings = [r';', r','],
	closings = [
		'LineComment',
	],
):
	pass

@eons.kind(Expression)
def ProtoExpression(
	representation = r'PROTOEXPRESSION',
	nest = [
		'Name',
		# Include StrictSyntaxes as a bridge to greater blocks.
		'Autofill',
		'Sequence'
	],
):
	pass

@eons.kind(DefaultBlockSet)
def ProtoExpressionSet(
	representation = r'PROTOEXPRESSIONSET',
	content = "ProtoExpression",
):
	pass

@eons.kind(ProtoExpression)
def LimitedExpression(
	representation = r'LIMITEDEXPRESSION',
	nest = [
		'ProtoExpressionSet',
		'BlockComment',
		'Execution',
		'Container',
	]
):
	pass

@eons.kind(DefaultBlockSet)
def LimitedExpressionSet(
	representation = r'LIMITEDEXPRESSIONSET',
	content = "LimitedExpression",
):
	pass


@eons.kind(ProtoExpression)
def FullExpression(
	representation = r'FULLEXPRESSION',
	nest = [
		'LimitedExpressionSet',
		'Parameter',
		'Namespace',
		'Type'
	]
):
	pass

@eons.kind(DefaultBlockSet)
def FullExpressionSet(
	representation = r'FULLEXPRESSIONSET',
	content = "FullExpression",
):
	pass

@eons.kind(Block)
def UnformattedString(
	openings = [r"\'"],
	closings = [r"\'"],
	representation = "\\'UNFORMATTED_STRING\\'", #NOT a raw string
	content = "FullExpressionSet",
):
	pass

@eons.kind(Block)
def FormattedString(
	openings = [r'"', r'`'],
	closings = [r'"', r'`'],
	representation = '\"FORMATTED_STRING\"', #NOT a raw string
	content = "FullExpressionSet",
):
	pass

@eons.kind(Block)
def BlockComment(
	openings = [r'/\*'],
	closings = [r'\*/'],
	representation = r'/\*BLOCK_COMMENT\*/',
	content = "FullExpressionSet",
):
	pass

@eons.kind(OpenEndedBlock)
def LineComment(
	openings = [r'#', r'//'],
	closings = [],
	representation = r'//LINE_COMMENT',
	content = "FullExpressionSet",
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
	doesSpaceClose = True,
	content = "LimitedExpressionSet",
):
	pass

@eons.kind(Block)
def Parameter(
	openings = [r'\('],
	closings = [r'\)'],
	representation = r'\(PARAMETER\)',
	content = "FullExpressionSet",
):
	pass

@eons.kind(Block)
def Execution(
	openings = [r'{'],
	closings = [r'}'],
	representation = r'{{EXECUTION}}',
	content = "FullExpressionSet",
):
	pass

@eons.kind(Block)
def Container(
	openings = [r'\['],
	closings = [r'\]'],
	representation = r'\[CONTAINER\]',
	content = "FullExpressionSet",
):
	pass
