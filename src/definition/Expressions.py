from .Block import *
import eons

@eons.kind(CatchAllBlock)
def Name(
	representation = r'NAME',
	specialStarts = [
		'/',
	],
):
	return this.p[0]

@eons.kind(DefaultBlock)
def Expression(
	openings = [r';', r','],
	closings = [
		'LineComment',
	],
	exclusions = [],
	before = None
):
	return this.p[0]

@eons.kind(Expression)
def ProtoExpression(
	representation = r'PROTOEXPRESSION',
	nest = [
		'Name',
		
		# StrictSyntaxes
		'Autofill',
		'Sequence',
		'UnformattedString',
		'ExplicitAccess',
	],
	before = "Sequence",
):
	return this.parent.Function(this)

@eons.kind(DefaultBlockSet)
def ProtoExpressionSet(
	representation = r'PROTOEXPRESSIONSET',
	content = "ProtoExpression",
	before = "ProtoExpression",
):
	return this.parent.Function(this)

@eons.kind(Expression)
def LimitedExpression(
	representation = r'LIMITEDEXPRESSION',
	nest = [
		'ProtoExpressionSet',
		'BlockComment',
		'Execution',
		'Container',
	],
	before = "ProtoExpressionSet"
):
	return this.parent.Function(this)

@eons.kind(DefaultBlockSet)
def LimitedExpressionSet(
	representation = r'LIMITEDEXPRESSIONSET',
	content = "LimitedExpression",
	before = "LimitedExpression"
):
	return this.parent.Function(this)


@eons.kind(Expression)
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
	],
	before = "Kind",
):
	return this.parent.Function(this)

@eons.kind(DefaultBlockSet)
def FullExpressionSet(
	representation = r'FULLEXPRESSIONSET',
	content = "FullExpression",
	before = "FullExpression",
):
	return this.parent.Function(this)