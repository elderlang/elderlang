import eons
import re
from .Sanitize import Sanitize

class Structure (eons.Functor):

	sanitize = Sanitize()

	def __init__(this, name="Structure"):
		super().__init__(name)

		# Used when parsing. Terrible name per Sly.
		this.optionalKWArgs['p'] = None

		this.optionalKWArgs['exclusions'] = []
		this.optionalKWArgs['inclusions'] = []
		this.optionalKWArgs['overrides'] = []

		this.fetch.use = [
			'args',
			'this',
		]
		this.fetch.attr.use = []

	def Function(this):
		pass

	def GetProduct(this, index):
		# No mangling necessary.. yet..
		return this.p[index]

	def Engulf(this, substrate, escape=False, buildContainer=False):
		if (
			substrate is None
			or isinstance(substrate, bool)
			or isinstance(substrate, int)
			or isinstance(substrate, float)
		):
			return substrate
		
		if (isinstance(substrate, list)
			or isinstance(substrate, dict)
		):
			if (buildContainer):
				ret = f"CreateContainer({substrate})"
			else:
				return substrate

		ret = str(substrate)
		
		if (not len(ret)):
			return ret

		if (ret[0] == ret[-1] 
			and (
				ret[0] == '"'
				or ret[0] == "'"
			)
		):
			ret = ret[1:-1]

		if (buildContainer and ret.startswith('[')):
			ret = f"CreateContainer({ret})"

		if (escape):
			ret = re.sub(r"\\", r"\\\\", ret)
			ret = re.sub(r"'", r"\'", ret)
		return ret
