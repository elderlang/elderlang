import eons
from .Structure import *

@eons.kind(Structure)
def Block(
	p = None, # Used when parsing. Terrible name per Sly.
	openings = [],
	closings = [],
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
	doesSpaceClose = False,
):
	pass

# There should only ever be one CatchAllBlock. We call it 'Name'.
# This Block matches anything that is not explicitly matched by another Block.
# specialStarts allows characters which normally cannot be inside a CatchAllBlock to start a CatchAllBlock.
# For example, '/=' is valid, while '=/' is not.
@eons.kind(Block)
def CatchAllBlock(
	specialStarts = [
		# Example only
		'/',
	],
):
	pass

# DefaultBlocks build the contents of all other Blocks beside the CatchAllBlock.
@eons.kind(OpenEndedBlock)
def DefaultBlock(
	nest = [], # List of blocks that can be nested inside this block.
):
	pass

# DefaultBlockSet is constructed from a series of DefaultBlocks.
# Each nest in a DefaultBlock is realized through a DefaultBlockSet.
@eons.kind(Block)
def DefaultBlockSet():
	pass