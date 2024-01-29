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
	return f"Invoke(name={this.p[0]}, parameter={this.Engulf(this.p[1])})"

@eons.kind(Invokation)
def InvokationWithExecution(
	blocks = [
		'Name',
		'Execution',
	]
):
	return f"Invoke(name={this.p[0]}, execution={this.Engulf(this.p[1])})"

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

# Executive type is terminal. No other types build on it.
@eons.kind(BlockSyntax)
def ExecutiveType(
	blocks = [
		'Name',
		'Kind',
		'Execution',
	],
):
	if (this.p[0].startswith('Type')):
		return f"{this.p[0][:-1]}, execution={this.Engulf(this.p[1])})"
	return f"Type(name={this.p[0]}, kind={this.Engulf(this.p[1])}, execution={this.Engulf(this.p[2])})"

@eons.kind(Invokation)
def InvokationWithParametersAndExecution(
	blocks = [
		'Name',
		'Parameter',
		'Execution',
	]
):
	if (this.p[0].startswith('Invoke')):
		return f"{this.p[0][:-1]}, execution={this.Engulf(this.p[1])})"
	return f"Invoke(name={this.p[0]}, parameter={this.Engulf(this.p[1])}, execution={this.Engulf(this.p[2])})"

@eons.kind(Invokation)
def ContainerInvokation(
	blocks = [
		'Name',
		'Container',
		'Execution',
	],
):
	if (this.p[0].startswith('Within')):
		return f"{this.p[0][:-1]}, execution={this.Engulf(this.p[1])})"
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
	if (this.p[0].startswith('Invoke')):
		return f"{this.p[0][:-1]}, container={this.Engulf(this.p[1])}, execution={this.Engulf(this.p[2])})"
	return f"Invoke(name={this.p[0]}, parameter={this.Engulf(this.p[1])}, container={this.Engulf(this.p[2])}, execution={this.Engulf(this.p[3])})"

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
		return f"{this.p[0][:-1]}, execution={this.Engulf(this.p[1])})"
	return f"Type(name={this.p[0]}, kind={this.Engulf(this.p[1])}, parameter={this.Engulf(this.p[2])}, execution={this.Engulf(this.p[3])})"

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
		r'simpletype autofillinvokation',
		r'simpletype containeraccess',
		r'simpletype standardinvokation',
		r'simpletype sequence',
		r'containeraccess autofillinvokation',
		r'containeraccess standardinvokation',
		r'containeraccess sequence',
		r'standardinvokation autofillinvokation',
		r'standardinvokation sequence',
		r'standardinvokation containeraccess',
		r'name sequence',
		r'name autofillinvokation',
		r'name containeraccess',
		r'name standardinvokation',
		r'simpletype name',
		r'containeraccess name',
		r'standardinvokation name',
		r'sequence name',
		r'name name',
		r'number name',
		r'autofillaccessorinvokation number',
	],
	recurseOn = "name"
):
	return f"Autofill('{this.Engulf(this.p[0], escape=True)}', '{this.Engulf(this.p[1], escape=True)}')"

@eons.kind(FlexibleTokenSyntax)
def AutofillInvokation(
	match = [
		r'name string',
		r'name number',
		r'shorttype string',
		r'shorttype number',
		r'shorttype sequence',
		r'shorttype container',
		r'shorttype containeraccess',
		r'shorttype standardinvokation',
	]
):
	return f"Call({str(this.p[0])}, {this.Engulf(str(this.p[1]))})"

@eons.kind(ExactSyntax)
def Sequence(
	match = r'NAME/NAME',
	recurseOn = "name"
):
	return f"Sequence({this.p[0]}, {this.p[2]})"

@eons.kind(ExactSyntax)
def ExplicitAccess(
	match = r'NAME\.NAME',
	recurseOn = "name"
):
	return f"Get({this.p[0]}, {this.p[2]})"

@eons.kind(ExactSyntax)
def ShortType(
	match = r'NAME\s+:=\s+'
):
	return f"Get(Type(name={this.p[0]}), '=')"

@eons.kind(ExactSyntax)
def UpperScopeOption1(
	match = r'\.\.NAME'
):
	return f"Upper.{this.p[0][2:]}"

@eons.kind(ExactSyntax)
def UpperScopeOption2(
	match = r'\.\./NAME'
):
	return f"Upper.{this.p[0][3:]}"

@eons.kind(FlexibleTokenSyntax)
def GlobalScope(
	match = [
		r'SEQUENCE NAME' # The / character has already been taken, so we have to reference it
	],
):
	return f"Global.{this.p[0][1:]}"
