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
		
		# StrictSyntaxes
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
		'UnformattedString',
		'FormattedString',
		'Parameter',
		'Namespace',
		'Type',
		
		# AbstractSyntaxes
		'Kind',
		'StructKind',
		'TypedName',
		'StandardInvokation',
		'InvokationWithParametersAndExecution',
		'InvokationWithExecution',
		'ContainerAccess',
		'ContainerInvokation',
		'ContainerInvokationWithParameters',
	]
):
	pass

@eons.kind(DefaultBlockSet)
def FullExpressionSet(
	representation = r'FULLEXPRESSIONSET',
	content = "FullExpression",
):
	pass