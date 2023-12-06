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
]

summary.blocks = [
	"FullExpressionSet",
	"FullExpression",
	"BlockComment",
	"LineComment",
	"UnformattedString",
	"FormattedString",
	"Execution",
	"Parameter",
	"Container",
	"Type",
	"Namespace",
	"LimitedExpressionSet",
	"LimitedExpression",
	"ProtoExpressionSet",
	"ProtoExpression",
	"Name",
]

summary.catchAllBlock = "Name"
summary.startingBlock = "FullExpressionSet"
summary.defaultBlock = "Expression"

summary.syntax = eons.util.DotDict()

summary.syntax.abstract = [
	"Kind",
	"StructKind",
	"ContainerInvokationWithParameters",
	"InvokationWithParametersAndExecution",
	"ContainerInvokation",
	"TypedName",
	"StandardInvokation",
	"ContainerAccess",
	"InvokationWithExecution",
]

summary.syntax.strict = [
	"Sequence",
	"Autofill",
	"EOL",
]