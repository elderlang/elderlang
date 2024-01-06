import eons
import re
import inspect
import logging
import types
from ..EldestFunctor import EldestFunctor
from ..EVAL import EVAL
from ..EXEC import EXEC
from ..TYPE import TYPE
from ..Util import *

class Autofill (EldestFunctor):
	def __init__(this, name="Autofill"):
		super().__init__(name)

		this.arg.kw.required.append('source')
		this.arg.kw.required.append('target')

		this.arg.mapping.append('source')
		this.arg.mapping.append('target')

	def Function(this):
		source = eons.util.DotDict()
		source.object = this.source
		source.type = 0
		if (type(this.source) == str):
			# Check if we should treat source.object as a Type & perform assignment.
			shouldAutoType = False
			if (type(this.target) == str and this.target == 'EQ' and this.executor is not None):
				stack = this.executor.stack.copy()
				stack.reverse()
				for name, object in stack:
					if (name == 'Autofill'):
						continue
					if (name == 'eval'):
						continue
					elif (name == 'exec'):
						logging.debug(f"Will attempt to autotype {this.source}.")
						shouldAutoType = True
					break
			source.object = EVAL(this.source, shouldAutoType = shouldAutoType)

		if (isinstance(source.object, types.FunctionType)):
			source.type = 1
		elif (type(source.object) in [int, float, str, bool]):
			source.type = 2
		elif (isinstance(source.object, TYPE)):
			source.type = 3
		elif (isinstance(source.object, eons.Functor)):
			source.type = 4

		# elif (inspect.isclass(source.object)):
		# 	source.object = source.object()
		# 	source.type = 2

		target = eons.util.DotDict()
		target.name = None
		target.type = 0
		if (type(this.target) == str):
			if (not '(' in this.target):
				target.name = this.target
				target.type = 1
			elif (
				this.target.startswith('Within')
				or this.target.startswith('Invoke')
			):
				search = re.search(r'\(name=(.*?),', this.target)
				target.name = search.group(1)
				target.type = 2
			elif (
				this.target.startswith('Autofill')
				or this.target.startswith('Call')
				or this.target.startswith('Sequence')
				or this.target.startswith('Get')
			):
				search = re.search(r'\((.*?),', this.target)
				target.name = search.group(1)
				target.type = 3

			if (target.name == None or target.type == 0):
				raise RuntimeError(f"Invalid target for autofill on {source.object}: {this.target}")
			
			if (target.name[0] == target.name[-1] 
				and (
					target.name[0] == '"'
					or target.name[0] == "'"
				)
			):
				target.name = target.name[1:-1]

		else:
			target.object = this.target
			target.type = 4

		if (target.type == 4 or source.type == 1):
			return source.object(this.target)

		logging.debug(f"Target name: {target.name}; target type: {target.type}; source: {source.object} source type: {source.type}")

		attemptedAccess = False
		try:
			# If member access works, use that.
			usableSource = source.object.__getattribute__(target.name)
			logging.debug(f"Found {target.name} on {source.object}")
			attemptedAccess = True
			if (target.type == 1):
				return usableSource
			elif (target.type == 2):
				newTarget = re.sub(rf"name=(\\*['\"]?){target.name}(\\*['\"]?)", rf"source=this.NEXTSOURCE", this.target)
				return EVAL(newTarget, NEXTSOURCE = usableSource)
			elif (target.type == 3):
				newTarget = re.sub(rf"(\\*['\"]?){target.name}(\\*['\"]?),", rf"this.NEXTSOURCE,", this.target)
				return EVAL(newTarget, NEXTSOURCE = usableSource)
		except Exception as e:
			if (not attemptedAccess):
				logging.debug(f"Could not find {target.name} on {source.object}")

				# Ensure non-functor types can be used with builtin symbols
				# e.g. greeting = 'hello'
				if (source.type == 2):
					if (target.type == 1):
						toEval = f"source.object.{this.target}"
						for match, replace in {
							'PLUS': '__add__',
							'MINUS': '__sub__',
							'TIMES': '__mul__',
							'DIVIDE': '__truediv__',
							'MOD': '__mod__',
							'PLUSEQ': '__iadd__',
							'MINUSEQ': '__isub__',
							'TIMESEQ': '__imul__',
							'DIVIDEEQ': '__idiv__',
							'MODEQ': '__imod__',
							'POW': '__pow__',
							'AND': '__and__',
							'OR': '__or__',
							'ANDAND': '__and__',
							'OROR': '__or__',
							'GT': '__gt__',
							'GTEQ': '__ge__',
							'LT': '__lt__',
							'LTEQ': '__le__',
							'EQEQ': '__eq__',
						}.items():
							toEval = toEval.replace(match, replace)
						logging.debug(f"Attempting to eval: {toEval}")
						return eval(toEval)
					
					elif (target.type == 3 and this.target.startswith("Call")):
						argRetrieval = this.target.replace('Call', 'GetArgs')
						args = eval(argRetrieval)
						arg0 = this.executor.Sanitize.Soil(args[0])
						arg1 = f"'{args[1]}'"
						# TODO: support more than just strings
						toExec = f"source.object {arg0} {arg1}"
						logging.debug(f"Attempting to exec: {toExec}")
						exec(toExec)
						return source.object

				# Otherwise, treat the source.object as a function.
				logging.debug(f"Using it as an arg for: {source.object}({this.target})")
				return source.object(EVAL(this.target))
			else:
				logging.error(f"Error while attempting to autofill {source.object} with {target.name}: {e}")
