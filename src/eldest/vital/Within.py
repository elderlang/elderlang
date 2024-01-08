import eons
import types
from .SourceTargetFunctor import SourceTargetFunctor
from ..EVAL import EVAL
from ..EXEC import EXEC

class Within (SourceTargetFunctor):
	def __init__(this, name="Within"):
		super().__init__(name)

		this.arg.kw.optional['useInvokation'] = False

		this.arg.kw.required.append('container')

		this.needs.target = False

	def Function(this):
		if (
			this.useInvokation 
			or isinstance(this.source, types.FunctionType) 
			or isinstance(this.source, types.MethodType)
		):
			return this.source([EVAL(item, shouldAttemptInvokation=True)[0] for item in this.container])

		index = EVAL(this.container[0], shouldAttemptInvokation=True)[0]
		logging.debug(f"Indexing {this.source} ({type(this.source)}) with {index} ({type(index)}).")

		if (
			isinstance(this.source, list)
			or isinstance(this.source, tuple)
			or isinstance(this.source, CONTAINER)
		):
			if (isinstance(index, int)):
				return this.source[index]
			if (isinstance(index, NUMBER) or isinstance(index, float)):
				return this.source[int(index)]
			elif (isinstance(index, STRING) or isinstance(index, str)):
				return this.source[str(index)]
			else:
				raise RuntimeError(f"Cannot index a list with {index}.")

		elif (
			isinstance(this.source, dict)
		):
			if (isinstance(index, NUMBER)):
				return this.source[int(index)]
			elif (isinstance(index, STRING)):
				return this.source[str(index)]
			return this.source[index]
		
		elif (
			isinstance(this.source, str)
			or isinstance(this.source, STRING)
		):
			return this.source[int(index)]
		
		else:
			raise RuntimeError(f"Cannot index {this.source} with {index}.")
		
