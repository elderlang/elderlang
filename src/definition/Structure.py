import eons

@eons.kind(eons.Functor)
def Structure(
	allowInBlocks = [
		'Execution'
	],
):
	pass

@eons.kind(Structure)
def StrictStructure(
	match = r'',
	replace = r'',
	readDirection = '>',
):
	pass

@eons.kind(Structure)
def AbstractStructure(
	requiredBlocks = [],
	optionalBlocks = [],
):
	pass