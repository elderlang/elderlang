from .Syntax import *
import eons
import re


@eons.kind(BlockSyntax)
def SimpleType(
	blocks = [
		'Name',
		'KindBlock',
	],
):
	return f"Type(name={this.GetProduct(0)},kind={this.Engulf(this.GetProduct(1))})"

@eons.kind(Invokation)
def StandardInvokation(
	blocks = [
		'Name',
		'ParameterBlock',
	]
):
	return f"Invoke(name={this.GetProduct(0)},parameter={this.Engulf(this.GetProduct(1))})"

@eons.kind(Invokation)
def AccessInvokation(
	blocks = [
		'ExplicitAccess',
		'ParameterBlock',
	]
):
	return f"Invoke(source='{this.Engulf(this.GetProduct(0), escape=True)}',parameter={this.Engulf(this.GetProduct(1))})"

@eons.kind(Invokation)
def InvokationWithExecution(
	blocks = [
		'Name',
		'ExecutionBlock',
	]
):
	return f"Invoke(name={this.GetProduct(0)},execution={this.Engulf(this.GetProduct(1))})"

@eons.kind(BlockSyntax)
def StructType(
	blocks = [
		'Name',
		'KindBlock',
		'ParameterBlock',
	],
):
	if (this.GetProduct(0).startswith('Type')):
		return f"{this.GetProduct(0)[:-1]},parameter={this.Engulf(this.GetProduct(1))})"
	return f"Type(name={this.GetProduct(0)},kind={this.Engulf(this.GetProduct(1))},parameter={this.Engulf(this.GetProduct(2))})"

# Executive type is terminal. No other types build on it.
@eons.kind(BlockSyntax)
def ExecutiveType(
	blocks = [
		'Name',
		'KindBlock',
		'ExecutionBlock',
	],
):
	if (this.GetProduct(0).startswith('Type')):
		return f"{this.GetProduct(0)[:-1]},execution={this.Engulf(this.GetProduct(1))})"
	return f"Type(name={this.GetProduct(0)},kind={this.Engulf(this.GetProduct(1))},execution={this.Engulf(this.GetProduct(2))})"

@eons.kind(Invokation)
def InvokationWithParametersAndExecution(
	blocks = [
		'Name',
		'ParameterBlock',
		'ExecutionBlock',
	]
):
	if (this.GetProduct(0).startswith('Invoke')):
		return f"{this.GetProduct(0)[:-1]},execution={this.Engulf(this.GetProduct(1))})"
	return f"Invoke(name={this.GetProduct(0)},parameter={this.Engulf(this.GetProduct(1))},execution={this.Engulf(this.GetProduct(2))})"

@eons.kind(Invokation)
def ContainerInvokation(
	blocks = [
		'Name',
		'ContainerBlock',
		'ExecutionBlock',
	],
):
	if (this.GetProduct(0).startswith('Within')):
		return f"{this.GetProduct(0)[:-1]},execution={this.Engulf(this.GetProduct(1))})"
	return f"Within(name={this.GetProduct(0)},container={this.Engulf(this.GetProduct(1))},execution={this.Engulf(this.GetProduct(2))})"

@eons.kind(Invokation)
def ContainerInvokationWithParameters(
	blocks = [
		'Name',
		'ParameterBlock',
		'ContainerBlock',
		'ExecutionBlock',
	],
):
	if (this.GetProduct(0).startswith('Invoke')):
		ret = f"{this.GetProduct(0)[:-1]},container={this.Engulf(this.GetProduct(1))},execution={this.Engulf(this.GetProduct(2))})"
	else:	
		ret = f"Invoke(name={this.GetProduct(0)},parameter={this.Engulf(this.GetProduct(1))},container={this.Engulf(this.GetProduct(2))},execution={this.Engulf(this.GetProduct(3))})"
	
	# We don't want to evaluate or auto-type entries in the container.
	# Instead, we want to treat them as strings.
	# This makes FOR and other such syntaxes possible.
	ret = re.sub(r'container=CreateContainer\(\[(.*?)\]\)', r'container=CreateContainer([\1],stringify=True)', ret)
	return ret

@eons.kind(BlockSyntax)
def FunctorType(
	blocks = [
		'Name',
		'KindBlock',
		'ParameterBlock',
		'ExecutionBlock',
	],
):
	if (this.GetProduct(0).startswith('Type')):
		return f"{this.GetProduct(0)[:-1]},execution={this.Engulf(this.GetProduct(1))})"
	return f"Type(name={this.GetProduct(0)},kind={this.Engulf(this.GetProduct(1))},parameter={this.Engulf(this.GetProduct(2))},execution={this.Engulf(this.GetProduct(3))})"

@eons.kind(ExactSyntax)
def EOL(
	match = r'[\\n\\r\\s]+',
	exclusions = [
		'parser',
	],
):
	return ''

@eons.kind(FlexibleTokenSyntax)
def ContainerAccess(
	match = [
		{
			'first': [
				r'name',
				r'this',
			],
			'second': [
				r'containerblock',
			]
		}
	]
):
	name = this.GetProduct(0)

	# Distinguishing between container *access* and *assignment* is non-trivial.
	# For example `x = [1]` should be assignment, but we don't treat `=` as something special: it's a name just like any other. So, how do we distingquish `=[1]` from `x[1]`?
	# For now, we'll say that anything in the operatorMap get's transmuted from access to assignment.
	if (name in this.executor.sanitize.operatorMap.keys()):
		return f"Invoke(name='{name}',parameter={this.Engulf(this.GetProduct(1))})"

	return f"Within(name={name},container={this.Engulf(this.GetProduct(1))})"

@eons.kind(FlexibleTokenSyntax)
def ComplexInvokation(
	match = [
		{
			'first': [
				r'complexexplicitaccess',
				r'complexinvokation',
				r'this',
				# TODO: We probably need more here, but adding may introduce reduce / reduce conflicts.
			],
			'second': [
				r'parameterblock',
			],
		},
	]
):
	return f"Invoke(source='{this.Engulf(this.GetProduct(0), escape=True)}',parameter={this.Engulf(this.GetProduct(1))})"


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
				r'complexinvokation',
				r'containeraccess',
				r'this',
				r'epidefoption1',
				r'epidefoption2',
				r'complexepidef',
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
				r'complexinvokation',
				r'containeraccess',
				r'this',
				r'epidefoption1',
				r'epidefoption2',
				r'complexepidef',
				r'globalscope',
				r'caller',
			],
		},
		{
			'first': [
				r'number',
				r'stringblock',
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
	return f"Autofill('{this.Engulf(this.GetProduct(0), escape=True)}','{this.Engulf(this.GetProduct(1), escape=True)}')"

@eons.kind(FlexibleTokenSyntax)
def AutofillInvokation(
	match = [
		{
			'first': [
				r'name',
				r'containeraccess',
				r'standardinvokation',
				r'accessinvokation',
				r'complexinvokation',
				r'explicitaccess',
				r'complexexplicitaccess',
				r'sequence',
				r'complexsequence',
				r'this',
				r'epidefoption1',
				r'epidefoption2',
				r'complexepidef',
				r'globalscope',
				r'caller',
				r'autofillaccessorinvokation',
			],
			'second': [
				r'number',
				r'stringblock',
			],
		},
		{
			'first': [
				r'shorttype',
			],
			'second': [
				r'name',
				r'number',
				r'stringblock',
				r'sequence',
				r'containerblock',
				r'containeraccess',
				r'standardinvokation',
				r'accessinvokation',
				r'complexinvokation',
				r'explicitaccess',
				r'complexexplicitaccess',
				r'this',
				r'epidefoption1',
				r'epidefoption2',
				r'complexepidef',
				r'globalscope',
				r'caller',
				r'autofillaccessorinvokation',
				r'simpletype',
				r'structtype',
				r'executivetype',
				r'functortype',
			],
		}
	],
	overrides = [
		'deprioritize'
	]
):
	return f"Invoke(source='{this.Engulf(this.GetProduct(0), escape=True)}',parameter=['{this.Engulf(this.GetProduct(1), escape=True)}'])"

@eons.kind(ExactSyntax)
def Sequence(
	match = r'NAME/NAME',
	# recurseOn = "name" # Now handled by ComplexSequence
):
	return f"FormSequence({this.GetProduct(0)},{this.GetProduct(2)})"

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
				r'complexepidef',
				r'globalscope',
				r'caller',
				r'complexsequence',
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
				r'complexepidef',
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
				r'complexepidef',
				r'globalscope',
				r'caller',
			],
		}
	]
):
	return f"FormSequence('{this.Engulf(this.GetProduct(0), escape=True)}','{this.Engulf(this.GetProduct(2), escape=True)}')"

@eons.kind(OperatorOverload)
def DivisionOverload(
	match = [
		r'SEQUENCE kindblock',
		r'SEQUENCE kindblock executionblock',
		r'SEQUENCE kindblock parameterblock executionblock',
	]
):
	return this.parent.Function(this)


# We have to specify the /= operator to prevent it from getting caught in a SEQUENCE match.
# TODO: Is there a fancier way to do a negative look ahead of an already matched name, so that we can include this logic in the SEQUENCE match?
@eons.kind(ExactSyntax)
def DivisionAssignment(
	match = r'NAME/=NAME',
):
	return f"{this.Engulf(this.GetProduct(0))} /= {this.Engulf(this.GetProduct(2))}"

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
				r'complexepidef',
				r'globalscope',
				r'caller',
				r'complexdivisionassignment',
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
				r'complexepidef',
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
				r'complexepidef',
				r'globalscope',
				r'caller',
			],
		}
	]
):
	return f"{this.Engulf(str(this.GetProduct(0)))} /= {this.Engulf(str(this.GetProduct(2)))}"

@eons.kind(OperatorOverload)
def DivisionAssignmentOverload(
	match = [
		r'DIVISIONASSIGNMENT kindblock',
		r'DIVISIONASSIGNMENT kindblock executionblock',
		r'DIVISIONASSIGNMENT kindblock parameterblock executionblock',
	]
):
	return this.parent.Function(this)

@eons.kind(ExactSyntax)
def ExplicitAccess(
	match = r'NAME\\.NAME',
	# recurseOn = "name" # Now handled by ComplexExplicitAccess
):
	return f"Get({this.GetProduct(0)},{this.GetProduct(2)})"

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
				r'complexepidef',
				r'globalscope',
				r'caller',
				r'complexexplicitaccess',
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
	return f"Get('{this.Engulf(this.GetProduct(0), escape=True)}','{this.Engulf(this.GetProduct(2), escape=True)}')"

@eons.kind(ExactSyntax)
def ShortType(
	match = r'NAME\\s+:=\\s+'
):
	return f"Get(Type(name={this.GetProduct(0)}),'EQ')"

@eons.kind(FlexibleTokenSyntax)
def SimpleTypeWithShortTypeAssignment(
	match = [r'name OPEN_KINDBLOCK limitedexpression SHORTTYPE']
):
	return f"Get(Type(name={this.Engulf(this.GetProduct(0))}, kind={this.Engulf(this.GetProduct(2))}))"

@eons.kind(ExactSyntax)
def This(
	match = r'\\./NAME'
):
	toAccess = this.Engulf(this.GetProduct(1)[1:-1])
	if (toAccess.startswith('this')):
		return toAccess
	return f"this.{toAccess}"

@eons.kind(ExactSyntax)
def EpidefOption1(
	match = r'\\.\\.NAME'
):
	return f"this.epidef.{this.Engulf(this.GetProduct(1)[1:-1])}"

@eons.kind(ExactSyntax)
def EpidefOption2(
	match = r'\\.\\./NAME'
):
	return f"this.epidef.{this.Engulf(this.GetProduct(1)[1:-1])}"

@eons.kind(FlexibleTokenSyntax)
def ComplexEpidef(
	match = [
		{
			'first': [
				r'EPIDEFOPTION2'
			],
			'second': [
				r'epidefoption1',
				r'epidefoption2',
				r'complexepidef'
			]
		}
	]
):
	return f"this.epidef.{this.Engulf(this.GetProduct(1)[5:])}"

@eons.kind(ExactSyntax)
def GlobalScope(
	match = r'~/NAME'
):
	return f"HOME.Instance().{this.Engulf(this.GetProduct(1)[1:-1])}"

@eons.kind(ExactSyntax)
def Caller(
	match = r'@NAME',
):
	# Enable @@... to become this.caller.caller...
	toAccess = this.Engulf(this.GetProduct(1)[1:-1])
	if (toAccess.startswith('this.caller')):
		return f"this.caller.{toAccess[5:]}"
	return f"this.caller.{toAccess}"
