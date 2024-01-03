import eons
import re
import inspect
import logging
from ..EldestFunctor import EldestFunctor
from ..EVAL import EVAL
from ..EXEC import EXEC
from ..TYPE import TYPE

class Autofill (EldestFunctor):
	def __init__(this, name="Autofill"):
		super().__init__(name)

		this.arg.kw.required.append('source')
		this.arg.kw.required.append('target')

		this.arg.mapping.append('source')
		this.arg.mapping.append('target')

	def Function(this):
		source = this.source
		if (type(this.source) == str):
			# Check if we should treat source as a Type & perform assignment.
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
			source = EVAL(this.source, shouldAutoType = shouldAutoType)

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
				search = re.search(r'\(name = (.*?),', this.target)
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
				raise RuntimeError(f"Invalid target for autofill on {source}: {this.target}")
			
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

		if (inspect.isclass(source)):
			source = source()

		if (target.type == 4):
			return source(this.target)
		
		logging.debug(f"Target name: {target.name}; target type: {target.type}; source: {source.name}")

		attemptedAccess = False
		try:
			# If member access works, use that.
			usableSource = source.__getattribute__(target.name)
			logging.debug(f"Found {target.name} on {source.name}")
			attemptedAccess = True
			if (target.type == 1):
				return usableSource
			elif (target.type == 2):
				EVAL._NEXTSOURCE = usableSource
				newTarget = re.sub(rf"name = (\\*['\"]?){target.name}(\\*['\"]?)", rf"source = this._NEXTSOURCE", this.target)
				return EVAL(newTarget)
			elif (target.type == 3):
				EVAL._NEXTSOURCE = usableSource
				newTarget = re.sub(rf"(\\*['\"]?){target.name}(\\*['\"]?),", rf"this._NEXTSOURCE,", this.target)
				return EVAL(newTarget)
		except Exception as e:
			if (not attemptedAccess):
				logging.debug(f"Could not find {target.name} on {source.name}; using it as an arg for: {source.name}({this.target})")
				# Otherwise, treat the source as a function.
				return source(EVAL(this.target))
			else:
				logging.error(f"Error while attempting to autofill {source.name} with {target.name}: {e}")
