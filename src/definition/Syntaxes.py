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
		r'simpletype this',
		r'simpletype epidefoption1',
		r'simpletype epidefoption2',
		r'simpletype globalscope',
		r'simpletype caller',

		r'containeraccess autofillinvokation',
		r'containeraccess standardinvokation',
		r'containeraccess containeraccess',
		r'containeraccess sequence',
		r'containeraccess this',
		r'containeraccess epidefoption1',
		r'containeraccess epidefoption2',
		r'containeraccess globalscope',
		r'containeraccess caller',

		r'standardinvokation autofillinvokation',
		r'standardinvokation sequence',
		r'standardinvokation containeraccess',
		r'standardinvokation this',
		r'standardinvokation epidefoption1',
		r'standardinvokation epidefoption2',
		r'standardinvokation globalscope',
		r'standardinvokation caller',

		r'this autofillinvokation',
		r'this containeraccess',
		r'this standardinvokation',
		r'this sequence',
		r'this this',
		r'this epidefoption1',
		r'this epidefoption2',
		r'this globalscope',
		r'this caller',

		r'epidefoption1 autofillinvokation',
		r'epidefoption1 containeraccess',
		r'epidefoption1 standardinvokation',
		r'epidefoption1 sequence',
		r'epidefoption1 this',
		r'epidefoption1 epidefoption1',
		r'epidefoption1 epidefoption2',
		r'epidefoption1 globalscope',
		r'epidefoption1 caller',

		r'epidefoption2 autofillinvokation',
		r'epidefoption2 containeraccess',
		r'epidefoption2 standardinvokation',
		r'epidefoption2 sequence',
		r'epidefoption2 this',
		r'epidefoption2 epidefoption1',
		r'epidefoption2 epidefoption2',
		r'epidefoption2 globalscope',
		r'epidefoption2 caller',

		r'globalscope autofillinvokation',
		r'globalscope containeraccess',
		r'globalscope standardinvokation',
		r'globalscope sequence',
		r'globalscope this',
		r'globalscope epidefoption1',
		r'globalscope epidefoption2',
		r'globalscope globalscope',
		r'globalscope caller',

		r'caller autofillinvokation',
		r'caller containeraccess',
		r'caller standardinvokation',
		r'caller sequence',
		r'caller this',
		r'caller epidefoption1',
		r'caller epidefoption2',
		r'caller globalscope',
		r'caller caller',

		r'name sequence',
		r'name autofillinvokation',
		r'name containeraccess',
		r'name standardinvokation',
		r'name this',
		r'name epidefoption1',
		r'name epidefoption2',
		r'name globalscope',
		r'name caller',

		r'simpletype name',
		r'containeraccess name',
		r'standardinvokation name',
		r'sequence name',
		r'this name',
		r'epidefoption1 name',
		r'epidefoption2 name',
		r'globalscope name',
		r'caller name',
		r'name name',
		r'number name',
		r'string name',
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
def This(
	match = r'\./NAME'
):
	return f"this.{this.p[0][2:]}"

@eons.kind(ExactSyntax)
def EpidefOption1(
	match = r'\.\.NAME'
):
	return f"this.epi.{this.p[0][2:]}"

@eons.kind(ExactSyntax)
def EpidefOption2(
	match = r'\.\./NAME'
):
	return f"this.epi.{this.p[0][3:]}"

@eons.kind(ExactSyntax)
def GlobalScope(
	match = r'~/NAME'
):
	return f"Global.{this.p[0][1:]}"

@eons.kind(ExactSyntax)
def Caller(
	match = r'@NAME',
):
	return f"this.caller.{this.p[0][1:]}"
