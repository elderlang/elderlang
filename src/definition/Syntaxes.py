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
	return f"Type(name={this.p[0]},kind={this.Engulf(this.p[1])})"

@eons.kind(BlockSyntax)
def ContainerAccess(
	blocks = [
		'Name',
		'Container',
	]
):
	return f"Within(name={this.p[0]},container={this.Engulf(this.p[1])})"

@eons.kind(Invokation)
def StandardInvokation(
	blocks = [
		'Name',
		'Parameter',
	]
):
	return f"Invoke(name={this.p[0]},parameter={this.Engulf(this.p[1])})"

@eons.kind(Invokation)
def AccessInvokation(
	blocks = [
		'ExplicitAccess',
		'Parameter',
	]
):
	return f"Invoke(source='{this.Engulf(this.p[0], escape=True)}',parameter={this.Engulf(this.p[1])})"

@eons.kind(AccessInvokation)
def ComplexAccessInvokation(
	blocks = [
		'ComplexExplicitAccess',
		'Parameter',
	]
):
	return this.parent.Function(this)

@eons.kind(Invokation)
def InvokationWithExecution(
	blocks = [
		'Name',
		'Execution',
	]
):
	return f"Invoke(name={this.p[0]},execution={this.Engulf(this.p[1])})"

@eons.kind(BlockSyntax)
def StructType(
	blocks = [
		'Name',
		'Kind',
		'Parameter',
	],
):
	if (this.p[0].startswith('Type')):
		return f"{this.p[0][:-1]},parameter={this.Engulf(this.p[1])})"
	return f"Type(name={this.p[0]},kind={this.Engulf(this.p[1])},parameter={this.Engulf(this.p[2])})"

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
		return f"{this.p[0][:-1]},execution={this.Engulf(this.p[1])})"
	return f"Type(name={this.p[0]},kind={this.Engulf(this.p[1])},execution={this.Engulf(this.p[2])})"

@eons.kind(Invokation)
def InvokationWithParametersAndExecution(
	blocks = [
		'Name',
		'Parameter',
		'Execution',
	]
):
	if (this.p[0].startswith('Invoke')):
		return f"{this.p[0][:-1]},execution={this.Engulf(this.p[1])})"
	return f"Invoke(name={this.p[0]},parameter={this.Engulf(this.p[1])},execution={this.Engulf(this.p[2])})"

@eons.kind(Invokation)
def ContainerInvokation(
	blocks = [
		'Name',
		'Container',
		'Execution',
	],
):
	if (this.p[0].startswith('Within')):
		return f"{this.p[0][:-1]},execution={this.Engulf(this.p[1])})"
	return f"Within(name={this.p[0]},container={this.Engulf(this.p[1])},execution={this.Engulf(this.p[2])})"

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
		return f"{this.p[0][:-1]},container={this.Engulf(this.p[1])},execution={this.Engulf(this.p[2])})"
	return f"Invoke(name={this.p[0]},parameter={this.Engulf(this.p[1])},container={this.Engulf(this.p[2])},execution={this.Engulf(this.p[3])})"

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
		return f"{this.p[0][:-1]},execution={this.Engulf(this.p[1])})"
	return f"Type(name={this.p[0]},kind={this.Engulf(this.p[1])},parameter={this.Engulf(this.p[2])},execution={this.Engulf(this.p[3])})"

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
		{
			'first': [
				r'name',
				r'sequence',
				r'complexsequence',
				r'explicitaccess',
				r'complexexplicitaccess',
				r'standardinvokation',
				r'accessinvokation',
				r'complexaccessinvokation',
				r'containeraccess',
				r'this',
				r'epidefoption1',
				r'epidefoption2',
				r'globalscope',
				r'caller',
				# Explicitly NOT simpletype
			],
			'second': [
				r'name',
				r'sequence',
				r'complexsequence',
				r'explicitaccess',
				r'complexexplicitaccess',
				r'standardinvokation',
				r'accessinvokation',
				r'complexaccessinvokation',
				r'containeraccess',
				r'this',
				r'epidefoption1',
				r'epidefoption2',
				r'globalscope',
				r'caller',
			],
		},
		{
			'first': [
				r'number',
				r'string',
			],
			'second': [
				r'name'
			]
		},
		{
			'first': [
				r'simpletype',
			],
			'second': [
				r'name'
			]
		}
	],
	recurseOn = "name",
	overrides = [
		'deprioritize'
	]
):
	return f"Autofill('{this.Engulf(this.p[0], escape=True)}','{this.Engulf(this.p[1], escape=True)}')"

@eons.kind(FlexibleTokenSyntax)
def AutofillInvokation(
	match = [
		{
			'first': [
				r'name',
				r'containeraccess',
				r'standardinvokation',
				r'accessinvokation',
				r'complexaccessinvokation',
				r'explicitaccess',
				r'complexexplicitaccess',
				r'sequence',
				r'complexsequence',
				r'this',
				r'epidefoption1',
				r'epidefoption2',
				r'globalscope',
				r'caller',
				r'autofillaccessorinvokation',
			],
			'second': [
				r'number',
				r'string',
			],
		},
		{
			'first': [
				r'shorttype',
			],
			'second': [
				r'number',
				r'string',
				r'sequence',
				r'container',
				r'containeraccess',
				r'standardinvokation',
				r'accessinvokation',
				r'complexaccessinvokation',
				r'explicitaccess',
				r'complexexplicitaccess',
				r'this',
				r'epidefoption1',
				r'epidefoption2',
				r'globalscope',
				r'caller',
				r'autofillaccessorinvokation',
			],
		}
	],
	overrides = [
		'deprioritize'
	]
):
	return f"Call('{this.Engulf(this.p[0], escape=True)}',{this.Engulf(str(this.p[1]))})"

@eons.kind(ExactSyntax)
def Sequence(
	match = r'NAME/NAME',
	# recurseOn = "name" # Now handled by ComplexSequence
):
	return f"Sequence({this.p[0]},{this.p[2]})"

@eons.kind(FlexibleTokenSyntax)
def ComplexSequence(
	match = [
		{
			'first': [
				r'sequence',
				r'standardinvokation',
				r'containeraccess',
				r'explicitaccess',
				r'complexexplicitaccess',
				r'this',
				r'epidefoption1',
				r'epidefoption2',
				r'globalscope',
				r'caller',
			],
			'second': [
				r'SEQUENCE',
			],
			'third': [
				r'name',
				r'standardinvokation',
				r'containeraccess',
				r'explicitaccess',
				r'complexexplicitaccess',
				r'this',
				r'epidefoption1',
				r'epidefoption2',
				r'globalscope',
				r'caller',
			],
		},
		{
			'first': [
				r'name',
			],
			'second': [
				r'SEQUENCE',
			],
			'third': [
				r'standardinvokation',
				r'containeraccess',
				r'explicitaccess',
				r'complexexplicitaccess',
				r'this',
				r'epidefoption1',
				r'epidefoption2',
				r'globalscope',
				r'caller',
			],
		}
	]
):
	return f"Sequence('{this.Engulf(this.p[0], escape=True)}','{this.Engulf(this.p[2], escape=True)}')"

@eons.kind(OperatorOverload)
def DivisionOverload(
	match = [
		r'SEQUENCE kind',
		r'SEQUENCE kind execution',
		r'SEQUENCE kind parameter execution',
	]
):
	return this.parent.Function(this)


# We have to specify the /= operator to prevent it from getting caught in a SEQUENCE match.
# TODO: Is there a fancier way to do a negative look ahead of an already matched name, so that we can include this logic in the SEQUENCE match?
@eons.kind(ExactSyntax)
def DivisionAssignment(
	match = r'NAME/=NAME',
):
	return f"{this.Engulf(this.p[0])} /= {this.Engulf(this.p[2])}"

# NOTE: Sequences and division CANNOT be combined.
@eons.kind(FlexibleTokenSyntax)
def ComplexDivisionAssignment(
	match = [
		{
			'first': [
				r'explicitaccess',
				r'complexexplicitaccess',
				r'standardinvokation',
				r'containeraccess',
				r'this',
				r'epidefoption1',
				r'epidefoption2',
				r'globalscope',
				r'caller',
			],
			'second': [
				r'DIVISIONASSIGNMENT',
			],
			'third': [
				r'name',
				r'autofillaccessorinvokation',
				r'standardinvokation',
				r'explicitaccess',
				r'containeraccess',
				r'this',
				r'epidefoption1',
				r'epidefoption2',
				r'globalscope',
				r'caller',
			],
		},
		{
			'first': [
				r'name',
			],
			'second': [
				r'DIVISIONASSIGNMENT',
			],
			'third': [
				r'autofillaccessorinvokation',
				r'standardinvokation',
				r'explicitaccess',
				r'containeraccess',
				r'this',
				r'epidefoption1',
				r'epidefoption2',
				r'globalscope',
				r'caller',
			],
		}
	]
):
	return f"{this.Engulf(str(this.p[0]))} /= {this.Engulf(str(this.p[2]))}"

@eons.kind(OperatorOverload)
def DivisionAssignmentOverload(
	match = [
		r'DIVISIONASSIGNMENT kind',
		r'DIVISIONASSIGNMENT kind execution',
		r'DIVISIONASSIGNMENT kind parameter execution',
	]
):
	return this.parent.Function(this)

@eons.kind(ExactSyntax)
def ExplicitAccess(
	match = r'NAME\.NAME',
	# recurseOn = "name" # Now handled by ComplexExplicitAccess
):
	return f"Get({this.p[0]},{this.p[2]})"

@eons.kind(FlexibleTokenSyntax)
def ComplexExplicitAccess(
	match = [
		{
			'first': [
				r'explicitaccess',
				r'standardinvokation',
				r'containeraccess',
				r'this',
				r'epidefoption1',
				r'epidefoption2',
				r'globalscope',
				r'caller',
			],
			'second': [
				r'EXPLICITACCESS',
			],
			'third': [
				r'name',
				r'standardinvokation',
				r'containeraccess',
			],
		},
		{
			'first': [
				r'name'
			],
			'second': [
				r'EXPLICITACCESS',
			],
			'third': [
				r'standardinvokation',
				r'containeraccess',
			],
		},
	]
):
	return f"Get('{this.Engulf(this.p[0], escape=True)}','{this.Engulf(this.p[2], escape=True)}')"

@eons.kind(ExactSyntax)
def ShortType(
	match = r'NAME\s+:=\s+'
):
	return f"Get(Type(name={this.p[0]}),'=')"

@eons.kind(FlexibleTokenSyntax)
def SimpleTypeWithShortTypeAssignment(
	match = [r'name OPEN_KIND limitedexpression SHORTTYPE']
):
	return f"Get(Type(name={this.Engulf(this.p[0])}, kind={this.Engulf(this.p[2])}))"

@eons.kind(ExactSyntax)
def This(
	match = r'\./NAME'
):
	toAccess = this.Engulf(this.p[1][1:-1])
	if (toAccess.startswith('this')):
		return toAccess
	return f"this.{toAccess}"

@eons.kind(ExactSyntax)
def EpidefOption1(
	match = r'\.\.NAME'
):
	return f"this.epidef.{this.Engulf(this.p[1][1:-1])}"

@eons.kind(ExactSyntax)
def EpidefOption2(
	match = r'\.\./NAME'
):
	return f"this.epidef.{this.Engulf(this.p[1][1:-1])}"

@eons.kind(ExactSyntax)
def GlobalScope(
	match = r'~/NAME'
):
	return f"HOME.Instance().{this.Engulf(this.p[1][1:-1])}"

@eons.kind(ExactSyntax)
def Caller(
	match = r'@NAME',
):
	# Enable @@... to become this.caller.caller...
	toAccess = this.Engulf(this.p[1][1:-1])
	if (toAccess.startswith('this.caller')):
		return f"this.caller.{toAccess[5:]}"
	return f"this.caller.{toAccess}"
