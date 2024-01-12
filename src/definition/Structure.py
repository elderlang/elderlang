import eons
import re

class Structure (eons.Functor):
	def __init__(this, name="Structure"):
		super().__init__(name)

		# Used when parsing. Terrible name per Sly.
		this.optionalKWArgs['p'] = None

		this.optionalKWArgs['exclusions'] = []
		this.optionalKWArgs['inclusions'] = []

	def Function(this):
		pass

	def Engulf(this, substrate, escape=False):
		if (
			substrate is None
			or isinstance(substrate, bool)
			or isinstance(substrate, int)
			or isinstance(substrate, float)
			or isinstance(substrate, list)
			or isinstance(substrate, dict)
		):
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

		if (escape):
			# ret = ret.replace(r"'", r"\'")
			# # First, replace all occurrences of \' with \\\'
			ret = re.sub(r"'", r"\'", ret)
			# # Then, replace any remaining unescaped single quotes with \\'
			# ret = re.sub(r"\\'", r"\\\'", ret)
		
		return ret
