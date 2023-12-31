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

summary.blocks = [
	"FullExpressionSet",
	"FullExpression",
	"Execution",
	"Parameter",
	"Container",
	"Kind",
	"LimitedExpressionSet",
	"LimitedExpression",
	"ProtoExpressionSet",
	"ProtoExpression",
	"BlockComment",
	"LineComment",
	"UnformattedString",
	"FormattedString",
	"String",
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
	"InvokationWithExecution",
	"StructType",
	"InvokationWithParametersAndExecution",
	"ContainerInvokation",
	"ContainerInvokationWithParameters",
	"FunctorType",
]

summary.syntax.exact = [
	"ExplicitAccess",
	"Sequence",
	"AutofillAccessOrInvokation",
	"AutofillInvokation",
	"EOL",
]