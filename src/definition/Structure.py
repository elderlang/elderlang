import eons
import re

class Structure (eons.Functor):

	# Sometimes SLY adds weird things like '$end' to the start of the product list.
	# To make everything work, we have to skip these values.
	# NOTE: This is not necessary, since SLY seems to work okay if you just stop it from adding $end...
	# productOffset = 0

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
		
		# ret = this.p[index + this.productOffset]
		# if (ret is None):
		# 	this.productOffset += 1
		# 	return this.GetProduct(index)
		# #TODO: does the offset ever go down?
		# return ret

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
			ret = re.sub(r"\\", r"\\\\", ret)
			ret = re.sub(r"'", r"\'", ret)
		return ret
