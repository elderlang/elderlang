import eons

class Structure (eons.Functor):
	def __init__(this, name="Structure"):
		super().__init__(name)

		# Used when parsing. Terrible name per Sly.
		this.optionalKWArgs['p'] = None

		this.optionalKWArgs['exclusions'] = []
		this.optionalKWArgs['inclusions'] = []

	def Function(this):
		pass

	# Engulfing a string prevents runaway escape characters (e.g. \\\\\\\\\\...)
	def Engulf(this, substrate):
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
		
		# while ('\\' in ret):
		# 	ret = ret.replace('\\', '')

		if (ret[0] == ret[-1] 
			and (
				ret[0] == '"'
				or ret[0] == "'"
			)
		):
			ret = ret[1:-1]
		
		return ret
