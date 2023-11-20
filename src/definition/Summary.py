import eons

# These don't actually do anything, they just help in ordering the files appropriately.
from .Blocks import *
from .Syntaxes import *


################################################################################
#                                 ORDER MATTERS
################################################################################

# The Summary contains a list of all the blocks and syntaxs that are defined in the Elder language.
# This is used by the parser to determine what to parse.
# Unfortunately, this is not automated (yet), so if you add a new block or syntax, you must add it to the Summary below.

summary = eons.util.DotDict()

summary.builtins = [
    'AUTOFILL',
	'SEQUENCE',
]

summary.blocks = [
	"BlockComment",
	"LineComment",
	"UnformattedString",
	"FormattedString",
	"Namespace",
	"Container",
	"Execution",
	"Parameter",    
	"Type",
	"Expression",
	"Name",
]

summary.catchAllBlock = "Name"

summary.syntax = eons.util.DotDict()

summary.syntax.abstract = [
	"Kind",
	"Invokation",
]

summary.syntax.strict = [
	"EOL",
	"Autofill",
	"Sequence",
	# "SpaceAutofillAutofillAndName",
	"IfElse",
	"If",
	"For",
	"While",
	# "Sigil",
	# "Not",
	# "And",
	# "DoubleAnd",
	# "Or",
	# "DoubleOr",
	# "Return",
]