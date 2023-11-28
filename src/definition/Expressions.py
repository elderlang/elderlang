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
		# 'LineComment',
	],
):
	return "Expression"

@eons.kind(Expression)
def ProtoExpression(
	representation = r'PROTOEXPRESSION',
	nest = [
		'Name',
		
		# StrictSyntaxes
		'Autofill',
		# 'Sequence'
	],
):
	return f"{this.p[0]}"

@eons.kind(DefaultBlockSet)
def ProtoExpressionSet(
	representation = r'PROTOEXPRESSIONSET',
	content = "ProtoExpression",
):
	return f"{this.p[0]} {this.p[1]}"

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
	return f"{this.p[0]} {this.p[1]}"

@eons.kind(DefaultBlockSet)
def LimitedExpressionSet(
	representation = r'LIMITEDEXPRESSIONSET',
	content = "LimitedExpression",
):
	return f"{this.p[0]} {this.p[1]}"


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
	return f"{this.p[0]}"

@eons.kind(DefaultBlockSet)
def FullExpressionSet(
	representation = r'FULLEXPRESSIONSET',
	content = "FullExpression",
):
	return f"{this.p[0]} {this.p[1]}"