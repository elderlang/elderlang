import eons
from .Structure import *

@eons.kind(Structure)
def Block(
	openings = [],
	closings = [],
	content = "",
):
	# Return only the content, not the open nor close.
	return this.p[1]

# SymmetricBlocks use the same symbols for both openings and closings.
@eons.kind(Block)
def SymmetricBlock(
	openings = [],
	content = "",
):
	return this.p[1]

# OpenEndedBlocks only specify openings.
# They are closed by the beginning of another block.
# To make this possible, we just reinterpret closings as a list of blocks, not regexes.
# NOTE: All OpenEndedBlocks are terminated by the end of the line (r'$')
# NOTE: OpenEndedBlocks are not allowed to be nested: they are also automatically closed by all listed openings.
@eons.kind(Block)
def OpenEndedBlock(
	closings = [
		# Example only
		# 'BlockComment',
		# 'LineComment'
	],
	doesSpaceClose = False,
):
	return this.p[1]

# There should only ever be one CatchAllBlock. We call it 'Name'.
# This Block matches anything that is not explicitly matched by another Block.
# specialStarts allows characters which normally cannot be inside a CatchAllBlock to start a CatchAllBlock.
# For example, '/=' is valid, while '=/' is not.
@eons.kind(Block)
def CatchAllBlock(
	specialStarts = [
		# Example only
		# '/',
	],
):
	return this.p[0]

# DefaultBlocks build the contents of all other Blocks beside the CatchAllBlock.
@eons.kind(OpenEndedBlock)
def DefaultBlock(
	nest = [], # List of blocks that can be nested inside this block.
	exclusions = [
		'EOL',
	]
):
	return this.parent.Function(this).returned

# DefaultBlockSet is constructed from a series of DefaultBlocks.
# Each nest in a DefaultBlock is realized through a DefaultBlockSet.
@eons.kind(Block)
def DefaultBlockSet():

	# reduce expression -> set
	if (isinstance(this.p[0], str)):
		return [this.p[0]]
	
	if (isinstance(this.p[0], list)):
		try:
			# reduce set set -> set
			if (isinstance(this.p[1], list)):
				return this.p[0] + this.p[1]
			
			# reduce set expression -> set
			else:
				return this.p[0].append(this.p[1])
			
		except:
			# reduce (reduced) expression -> set
			return this.p[0]
		