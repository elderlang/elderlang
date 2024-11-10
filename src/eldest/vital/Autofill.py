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
				for name, object in this.executor.stack:
					if (name == 'Autofill'):
						continue
					if (name == 'eval'):
						continue
					elif (name == 'exec'):
						logging.debug(f"Will attempt to autotype {this.source}.")
						shouldAutoType = True
					break
			source.object, unwrapped = EVAL(this.source, shouldAutoType=shouldAutoType)

		if (isinstance(source.object, types.FunctionType) or isinstance(source.object, types.MethodType)):
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
				try:
					search = re.search(r'\(name=(.*?),', this.target)
					target.name = search.group(1)
					target.type = 2
				except Exception as e:
					if (this.target.startswith('Invoke')):
						argRetrieval = this.target.replace('Invoke', 'GetKWArgs')
						args = eval(argRetrieval)
						target.name = this.target
						toReplace = args['source']
						toReplace = re.sub(r'\\', r'\\\\', toReplace)
						toReplace = re.sub(r'\'', '\\\'', toReplace)
						toReplace = f"'{toReplace}'"
						newTarget = this.target.replace(toReplace, 'E____OBJECT.NEXTSOURCE')
						nextSource = EVAL([args['source']], unwrapReturn=True, shouldAutoType=False)[0]
						target.object = EVAL([newTarget], unwrapReturn=True, shouldAutoType=False, NEXTSOURCE=nextSource)[0]
						target.type = 5
					else:
						raise e
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
			target.name = this.target
			target.type = 4

		logging.debug(f"Target name: {target.name}; target type: {target.type}; source: {source.object} ({type(source.object)}) source type: {source.type}")

		if (target.type == 5):
			return source.object(target.object)

		attemptedAccess = False
		ret = None
		unwrapped = False
		try:
			# If member access works, use that.
			usableSource = eval(f"source.object.{target.name}")
			logging.debug(f"Found {target.name} on {source.object}")
			attemptedAccess = True
			if (target.type == 1):
				ret =  usableSource
			elif (target.type == 2):
				newTarget = re.sub(rf"name=(\\*['\"]?){target.name}(\\*['\"]?)", rf"source=E____OBJECT.NEXTSOURCE", this.target)
				ret, unwrapped =  EVAL(newTarget, shouldAutoType=False, NEXTSOURCE=usableSource)
			elif (target.type == 3):
				newTarget = re.sub(rf"(\\*['\"]?){target.name}(\\*['\"]?),", rf"E____OBJECT.NEXTSOURCE,", this.target)
				ret, unwrapped = EVAL(newTarget, shouldAutoType=False, NEXTSOURCE=usableSource)

		except Exception as e:
			if (not attemptedAccess):
				logging.debug(f"Could not find {target.name} on {source.object}")

				# Ensure non-functor types can be used with builtin symbols
				# e.g. greeting = 'hello'
				if (source.type == 1):
					if (target.type == 3 and this.target.startswith("Call")):
						source.object = source.object()
						return this.EvaluateCallAfterBasicType(source, target)
					elif (target.type == 4):
						return source.object(this.target)

				elif (source.type == 2):
					if (target.type == 1):
						toEval = f"source.object.{this.target}"
						for match, replace in this.executor.sanitize.operatorMap.items():
							toEval = toEval.replace(match, replace)
						logging.debug(f"Attempting to eval: {toEval}")
						return eval(toEval)

					elif (target.type == 2):
						if (this.target.startswith("Invoke") and target.name in this.executor.sanitize.operatorMap.keys()):
							try:
								usableSource = source.object.__getattribute__(this.executor.sanitize.operatorMap[target.name])
								newTarget = re.sub(rf"name=(\\*['\"]?){target.name}(\\*['\"]?)", rf"source=E____OBJECT.NEXTSOURCE", this.target)
								return EVAL(newTarget, shouldAutoType=False, NEXTSOURCE=usableSource)[0]
							except:
								pass

					elif (target.type == 3 and this.target.startswith("Call")):
						return this.EvaluateCallAfterBasicType(source, target)

				# Otherwise, treat the source.object as a function.
				logging.debug(f"Using it as an arg for: {source.object}({this.target})")

				target.object = EVAL(this.target, shouldAutoType=False)[0]

				if (target.type == 1 and '.EQ of ' not in str(source.object)):
					if (isinstance(target.object, eons.Functor)
						or isinstance(target.object, types.FunctionType)
						or isinstance(target.object, types.MethodType)
					):
						target.object = target.object()

				ret = source.object(target.object)

			else:
				logging.error(f"Error while attempting to autofill {source.object} with {target.name}: {e}")

		name, object = this.executor.stack[1]
		if ((
				isinstance(ret, eons.Functor)
				or isinstance(ret, types.MethodType)
				or isinstance(ret, types.FunctionType)
			)
			and (
				isinstance(object, EXEC.__class__)
				or isinstance(object, RETURN.__class__) # This may be a bug; it happens when a functor returns without any further action being taken, e.g. if(returns_false()){nop}THIS_AUTOFILL;
			)
		):
			logging.debug(f"It looks like I'm the last statement in this expression. I'll execute {ret}...")
			ret = ret()

		return ret
	
	def EvaluateCallAfterBasicType(this, source, target):
		argRetrieval = this.target.replace('Call', 'GetArgs')
		args = eval(argRetrieval)
		arg0 = this.executor.sanitize.Soil(args[0])
		arg1 = args[1]
		if (type(source.object) in [str, list]):
			arg1 = f"'{args[1]}'"
		toEval = f"source.object {arg0} {arg1}"
		logging.debug(f"Attempting to eval: {toEval}")
		return eval(toEval)
