from .Syntax import *
import eons

@eons.kind(AbstractSyntax)
def Kind(
	blocks = [
		'Type',
		'Name',
		'Parameter',
		'Execution',
	],
	allowInBlocks = [
		'Parameter',
		'Execution',
	]
):
	pass

@eons.kind(AbstractSyntax)
def TypedName(
	blocks = [
		'Type',
		'Name',
	],
):
	pass

@eons.kind(AbstractSyntax)
def Invokation(
	blocks = [
		'Name',
	]
):
	pass

@eons.kind(Invokation)
def StandardInvokation(
	blocks = [
		'Name',
		'Parameter',
	]
):
	pass

@eons.kind(Invokation)
def InvokationWithParameterAndExecution(
	blocks = [
		'Name',
		'Parameter',
		'Execution',
	]
):
	pass

@eons.kind(Invokation)
def InvokationWithExecution(
	blocks = [
		'Name',
		'Execution',
	]
):
	pass

@eons.kind(Invokation)
def ContainerInvokation(
	blocks = [
		'Name',
		'Container',
		'Execution',
	],
):
	pass

@eons.kind(Invokation)
def ContainerInvokationWithParameters(
	blocks = [
		'Name',
		'Parameter',
		'Container',
		'Execution',
	],
):
	pass

@eons.kind(AbstractSyntax)
def ContainerAccess(
	blocks = [
		'Name',
		'Container',
	]
):
	pass

@eons.kind(StrictSyntax)
def EOL(
	match = r'\\n',
):
	pass

@eons.kind(StrictSyntax)
def Autofill(
	match = r'EXPRESSION[ +]NAME',
	excludeFromCatchAll = True,
	recurse = True,
):
	pass

@eons.kind(StrictSyntax)
def Sequence(
	match = r'NAME/NAME',
	recurse = True,
	allowInBlocks = [
		'Namespace',
		'Expression',
	]
):
	pass