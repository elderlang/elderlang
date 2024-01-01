from .EXEC import EXEC
from .EVAL import EVAL
from .vital.Autofill import Autofill
from .vital.Call import Call
from .vital.Get import Get
from .vital.Invoke import Invoke
from .vital.Kind import Kind
from .vital.Sequence import Sequence
from .vital.String import String
from .vital.Type import Type
from .vital.Within import Within
from .keyword.BREAK import BREAK
from .keyword.CASE import CASE
from .keyword.CATCH import CATCH
from .keyword.CONTINUE import CONTINUE
from .keyword.DEFAULT import DEFAULT
from .keyword.ELSE import ELSE
from .keyword.FOR import FOR
from .keyword.IF import IF
from .keyword.NOT import NOT
from .keyword.RETURN import RETURN
from .keyword.SWITCH import SWITCH
from .keyword.TRY import TRY
from .keyword.WHILE import WHILE

EXEC = EXEC()
EVAL = EVAL()
Autofill = Autofill()
Call = Call()
Get = Get()
Invoke = Invoke()
Kind = Kind()
Sequence = Sequence()
String = String()
Type = Type()
Within = Within()

BREAK = BREAK()
CASE = CASE()
CATCH = CATCH()
CONTINUE = CONTINUE()
DEFAULT = DEFAULT()
ELSE = ELSE()
FOR = FOR()
IF = IF()
NOT = NOT()
RETURN = RETURN()
SWITCH = SWITCH()
TRY = TRY()
WHILE = WHILE()
