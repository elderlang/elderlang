from .Block import *
import eons

@eons.kind(CatchAllBlock)
def Name(
	representation = r'NAME',
):
	return f"'{this.p[0]}'"

@eons.kind(Expression)
def ProtoExpression(
	representation = r'PROTOEXPRESSION',
	nest = [
		'Name',
		'Number',
		'String',
		
		# ExactSyntaxes
		'AutofillAccessOrInvokation',
		'AutofillInvokation',
		'Sequence',
		'DivisionAssignment',
		'ExplicitAccess',
		'EpidefOption1',
		'EpidefOption2',
		'GlobalScope',
	],
	before = "Sequence",
):
	return this.parent.Function(this)

@eons.kind(ExpressionSet)
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
		'ProtoExpression',
		'ProtoExpressionSet',
		# 'Execution',
		# 'Container',

		# BlockSyntaxes
		'InvokationWithExecution',
		'ContainerAccess',
		'ContainerInvokation',
	],
	before = "ProtoExpressionSet"
):
	return this.parent.Function(this)

@eons.kind(ExpressionSet)
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
		'LimitedExpression',
		'LimitedExpressionSet',
		'Kind',
		# 'Parameter',

		# BlockSyntaxes
		'FunctorType',
		'StructType',
		'ExecutiveType',
		'SimpleType',
		'StandardInvokation',
		'AccessInvokation',
		'ComplexAccessInvokation',
		'InvokationWithParametersAndExecution',
		'ContainerInvokationWithParameters',

		# ExactSyntaxes
		'SimpleTypeWithShortTypeAssignment',
		'ComplexSequence',
		'DivisionOverload',
		'ComplexDivisionAssignment',
		'DivisionAssignmentOverload',
		'ComplexExplicitAccess',
	],
	before = "FunctorType",
):
	return this.parent.Function(this)

@eons.kind(ExpressionSet)
def FullExpressionSet(
	representation = r'FULLEXPRESSIONSET',
	content = "FullExpression",
	before = "FullExpression",
):
	return this.parent.Function(this)