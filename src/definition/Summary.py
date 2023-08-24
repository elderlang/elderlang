import eons

# These don't actually do anything, they just help in ordering the files appropriately.
from .Blocks import *
from .Structures import *


################################################################################
#                                 ORDER MATTERS
################################################################################

# The Summary contains a list of all the blocks and structures that are defined in the Elder language.
# This is used by the parser to determine what to parse.
# Unfortunately, this is not automated (yet), so if you add a new block or structure, you must add it to the Summary below.

summary = eons.util.DotDict()

summary.builtins = [
    'AUTOFILL'
]

summary.blocks = [
	"BlockComment",
	"LineComment",
	"UnformattedString",
	"FormattedString",
	"GlobalNamespace",
	"LocalNamespace",
	"Container",
	"Execution",
	"Parameter",    
	"Type",
	"Expression",
	"Name",
]

summary.catchAllBlock = "Name"

summary.structure = eons.util.DotDict()

summary.structure.abstract = [
	"Kind",
	"Invokation",
]

summary.structure.strict = [
	"SpaceAutofillNames",
	"SpaceAutofillAutofillAndName",
	"IfElse",
	"If",
	"For",
	"While",
	# "Sigil",
	"Not",
	"And",
	"DoubleAnd",
	"Or",
	"DoubleOr",
	"Return",
]