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
):
	pass

@eons.kind(AbstractSyntax)
def StructKind(
	blocks = [
		'Type',
		'Name',
		'Parameter',
	],
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

@eons.kind(Invokation)
def StandardInvokation(
	blocks = [
		'Name',
		'Parameter',
	]
):
	pass

@eons.kind(Invokation)
def InvokationWithParametersAndExecution(
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
	exclusions = [
		'parser'
	],
):
	pass

@eons.kind(StrictSyntax)
def Autofill(
	match = r'NAMESPACENAME',
	exclusions = [
		'all.catch.block'
	],
	recurseOn = "NAME",
	readDirection = "<"
):
	pass

@eons.kind(StrictSyntax)
def Sequence(
	match = r'NAME/NAME',
	recurseOn = "NAME",
	readDirection = ">"
):
	pass