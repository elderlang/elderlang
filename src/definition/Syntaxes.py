from .Syntax import *
import eons
import re


@eons.kind(BlockSyntax)
def SimpleType(
	blocks = [
		'Name',
		'Kind',
	],
):
	return f"Type(name={this.p[0]}, kind={this.Engulf(this.p[1])})"

@eons.kind(BlockSyntax)
def ContainerAccess(
	blocks = [
		'Name',
		'Container',
	]
):
	return f"Within(name={this.p[0]}, container={this.Engulf(this.p[1])})"

@eons.kind(Invokation)
def StandardInvokation(
	blocks = [
		'Name',
		'Parameter',
	]
):
	return f"Invokation(name={this.p[0]}, parameter={this.Engulf(this.p[1])})"

@eons.kind(Invokation)
def InvokationWithExecution(
	blocks = [
		'Name',
		'Execution',
	]
):
	return f"Invokation(name={this.p[0]}, execution={this.Engulf(this.p[1])})"

@eons.kind(BlockSyntax)
def StructType(
	blocks = [
		'Name',
		'Kind',
		'Parameter',
	],
):
	if (this.p[0].startswith('Type')):
		return f"{this.p[0][:-1]}, parameter={this.Engulf(this.p[1])})"
	return f"Type(name={this.p[0]}, kind={this.Engulf(this.p[1])}, parameter={this.Engulf(this.p[2])})"

@eons.kind(Invokation)
def InvokationWithParametersAndExecution(
	blocks = [
		'Name',
		'Parameter',
		'Execution',
	]
):
	if (this.p[0].startswith('Invokation')):
		return f"{this.p[0][:-1]}, execution = {this.Engulf(this.p[1])})"
	return f"Invokation(name={this.p[0]}, parameter={this.Engulf(this.p[1])}, execution={this.Engulf(this.p[2])})"

@eons.kind(Invokation)
def ContainerInvokation(
	blocks = [
		'Name',
		'Container',
		'Execution',
	],
):
	if (this.p[0].startswith('Within')):
		return f"{this.p[0][:-1]}, execution = {this.Engulf(this.p[1])})"
	return f"Within(name={this.p[0]}, container={this.Engulf(this.p[1])}, execution={this.Engulf(this.p[2])})"

@eons.kind(Invokation)
def ContainerInvokationWithParameters(
	blocks = [
		'Name',
		'Parameter',
		'Container',
		'Execution',
	],
):
	if (this.p[0].startswith('Invokation')):
		return f"{this.p[0][:-1]}, container = {this.Engulf(this.p[1])}, execution = {this.Engulf(this.p[2])})"
	return f"InvokationWithin(name={this.p[0]}, parameter={this.Engulf(this.p[1])}, container={this.Engulf(this.p[2])}, execution={this.Engulf(this.p[3])})"

@eons.kind(BlockSyntax)
def FunctorType(
	blocks = [
		'Name',
		'Kind',
		'Parameter',
		'Execution',
	],
):
	if (this.p[0].startswith('Type')):
		return f"{this.p[0][:-1]}, execution = {this.Engulf(this.p[1])})"
	return f"Type(name='{this.p[0]}, kind={this.Engulf(this.p[1])}, parameter={this.Engulf(this.p[2])}, execution={this.Engulf(this.p[3])})"

@eons.kind(ExactSyntax)
def EOL(
	match = r'[\\n\\r\\s]+',
	exclusions = [
		'parser',
	],
):
	return ''

@eons.kind(FlexibleTokenSyntax)
def AutofillAccessOrInvokation(
	match = [
		r'name name',
		r'name sequence',
		r'name autofillinvokation',
		r'name containeraccess',
		r'name standardinvokation',
		r'sequence name',
		r'simpletype name',
		r'simpletype sequence',
		r'simpletype autofillinvokation',
		r'simpletype containeraccess',
		r'simpletype standardinvokation',
		r'containeraccess name',
		r'containeraccess sequence',
		r'containeraccess autofillinvokation',
		r'containeraccess standardinvokation',
		r'standardinvokation name',
		r'standardinvokation sequence',
		r'standardinvokation autofillinvokation',
		r'standardinvokation containeraccess',
	],
	recurseOn = "name",
	readDirection = ">"
):
	return f"Autofill({this.Engulf(this.p[0])}, {this.Engulf(this.p[1])})"

@eons.kind(FlexibleTokenSyntax)
def AutofillInvokation(
	match = [
		r'name string',
		r'name number',
		r'name container',
	],
	readDirection = ">"
):
	return f"Call({this.p[0]}, {this.Engulf(this.p[1])})"

@eons.kind(ExactSyntax)
def Sequence(
	match = r'NAME/NAME',
	recurseOn = "name",
	readDirection = ">"
):
	return f"Sequence({this.p[0]}, {this.p[2]})"

@eons.kind(ExactSyntax)
def ExplicitAccess(
	match = r'NAME\.NAME',
	recurseOn = "name",
	readDirection = ">"
):
	return f"Get({this.p[0]}, {this.p[2]})"
