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
	return f"Kind(type = {this.p[0]}, name = {this.p[1]}, parameter = {this.p[2]}, execution = {this.p[3]})"

@eons.kind(AbstractSyntax)
def StructKind(
	blocks = [
		'Type',
		'Name',
		'Parameter',
	],
):
	return f"StructKind(type = {this.p[0]}, name = {this.p[1]}, parameter = {this.p[2]})"

@eons.kind(AbstractSyntax)
def TypedName(
	blocks = [
		'Type',
		'Name',
	],
):
	return f"TypedName(type = {this.p[0]}, name = {this.p[1]})"

@eons.kind(Invokation)
def StandardInvokation(
	blocks = [
		'Name',
		'Parameter',
	]
):
	return f"StandardInvokation(name = {this.p[0]}, parameter = {this.p[1]})"

@eons.kind(Invokation)
def InvokationWithParametersAndExecution(
	blocks = [
		'Name',
		'Parameter',
		'Execution',
	]
):
	return f"InvokationWithParametersAndExecution(name = {this.p[0]}, parameter = {this.p[1]}, execution = {this.p[2]})"

@eons.kind(Invokation)
def InvokationWithExecution(
	blocks = [
		'Name',
		'Execution',
	]
):
	return f"InvokationWithExecution(name = {this.p[0]}, execution = {this.p[1]})"

@eons.kind(Invokation)
def ContainerInvokation(
	blocks = [
		'Name',
		'Container',
		'Execution',
	],
):
	return f"ContainerInvokation(name = {this.p[0]}, container = {this.p[1]}, execution = {this.p[2]})"

@eons.kind(Invokation)
def ContainerInvokationWithParameters(
	blocks = [
		'Name',
		'Parameter',
		'Container',
		'Execution',
	],
):
	return f"ContainerInvokationWithParameters(name = {this.p[0]}, parameter = {this.p[1]}, container = {this.p[2]}, execution = {this.p[3]})"

@eons.kind(AbstractSyntax)
def ContainerAccess(
	blocks = [
		'Name',
		'Container',
	]
):
	return f"ContainerAccess(name = {this.p[0]}, container = {this.p[1]})"

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
	match = r'name name',
	literalMatch = True,
	noToken = True,
	exclusions = [
		'all.catch.block'
	],
	recurseOn = "name",
	readDirection = "<"
):
	return f"Autofill({this.p[0]}, {this.p[1]})"

@eons.kind(StrictSyntax)
def Sequence(
	match = r'NAME/NAME',
	recurseOn = "name",
	readDirection = ">"
):
	return f"Sequence({this.p[0]}, {this.p[2]})"