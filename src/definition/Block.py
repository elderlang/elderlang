import eons

@eons.kind(eons.Functor)
def Block(
	openings = [],
	closings = [],
	recurse = False,
	nest = [],
	content = "",
):
	pass

# OpenEndedBlocks only specify openings.
# They are closed by the beginning of another block.
# To make this possible, we just reinterpret closings as a list of blocks, not regexes.
# NOTE: All OpenEndedBlocks are terminated by the end of the line (r'$')
# NOTE: OpenEndedBlocks are not allowed to be nested: they are also automatically closed by all listed openings.
@eons.kind(Block)
def OpenEndedBlock(
	closings = [
		# Example only
		'BlockComment',
		'LineComment'
	],
):
	pass

# There should only ever be one CatchAllBlock. We call it 'Name'.
# This Block matches anything that is not explicitly matched by another Block.
@eons.kind(Block)
def CatchAllBlock():
	pass
