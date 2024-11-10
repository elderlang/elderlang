import eons

# These don't actually do anything, they just help in ordering the files appropriately.
from .Blocks import * 
from .Syntaxes import *
from .Expressions import *


################################################################################
#                                 ORDER MATTERS
# The order provided is the priority each section is given when parsing.
################################################################################

# The Summary contains a list of all the blocks and syntaxes that are defined in the Elder language.
# This is used by the parser to determine what to parse.
# Unfortunately, this is not automated (yet), so if you add a new block or syntax, you must add it to the Summary below.

summary = eons.util.DotDict()

summary.builtins = [
	"NUMBER",
]

summary.token = eons.util.DotDict()
summary.token.priority = [
	"UNFORMATTEDSTRINGBLOCK",
	"FORMATTEDSTRINGBLOCK",
	"DIVISIONASSIGNMENT",
	"NUMBER",
	"SHORTTYPE",
	"OPEN_KINDBLOCK",
	"OPEN_EXECUTIONBLOCK",
	"OPEN_PARAMETERBLOCK",
	"OPEN_CONTAINERBLOCK",
	"CLOSE_EXECUTIONBLOCK",
	"CLOSE_PARAMETERBLOCK",
	"CLOSE_CONTAINERBLOCK",
	"CLOSE_EXPRESSION",
	"THIS",
	"EPIDEFOPTION2",
	"EPIDEFOPTION1",
	"GLOBALSCOPE",
	"EXPLICITACCESS",
	"SEQUENCE",
	"CALLER",
	"EOL",
	"NAME",
]

summary.blocks = [
	"FullExpressionSet",
	"FullExpression",
	"ExecutionBlock",
	"ParameterBlock",
	"ContainerBlock",
	"KindBlock",
	"LimitedExpressionSet",
	"LimitedExpression",
	"ProtoExpressionSet",
	"ProtoExpression",
	"BlockComment",
	"LineComment",
	"UnformattedStringBlock",
	"FormattedStringBlock",
	"StringBlock",
	"Name",
]

summary.catchAllBlock = "Name"
summary.startingBlock = "FullExpressionSet"
summary.expression = "Expression" # The DefaultBlock
summary.eol = "EOL"

summary.syntax = eons.util.DotDict()

summary.syntax.block = [
	"SimpleType",
	"ContainerAccess",
	"StandardInvokation",
	"AccessInvokation",
	"ComplexAccessInvokation",
	"InvokationWithExecution",
	"StructType",
	"ExecutiveType",
	"InvokationWithParametersAndExecution",
	"ContainerInvokation",
	"ContainerInvokationWithParameters",
	"FunctorType",
]

summary.syntax.exact = [
	"DivisionAssignment",
	"ComplexDivisionAssignment",
	"This",
	"EpidefOption2",
	"EpidefOption1",
	"ComplexEpidef",
	"GlobalScope",
	"DivisionOverload",
	"DivisionAssignmentOverload",
	"ExplicitAccess",
	"ComplexExplicitAccess",
	"Sequence",
	"ComplexSequence",
	"AutofillAccessOrInvokation",
	"AutofillInvokation",
	"EOL",
	"ShortType",
	"SimpleTypeWithShortTypeAssignment",
	"Caller",
]