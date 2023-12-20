import eons
import re
import logging
from .Structure import *
from .Exceptions import *

@eons.kind(Structure)
def Block(
	openings = [],
	closings = [],
	content = "",
):
	# Return only the content, not the open nor close.
	# We must also filter for EOL tokens.
	possibleContent = None
	i = 0
	failedMatches = []
	reject = [r'\s+'] + openings + closings
	while (True):
		try:
			possibleContent = this.p[i]
			logging.debug(f"{this.name} Block has possibleContent '{possibleContent}' ({i}).")

			if (isinstance(possibleContent, str)):
				if (not len(possibleContent)):
					i += 1
					continue
				
				for r in reject:
					if (re.match(r, possibleContent)):
						failedMatches.append(possibleContent)
						i += 1
						break
				else:
					continue

			elif (isinstance(possibleContent, list)):
				# Sets and friends will return lists, so this is probably what we're looking for.
				break

			else:
				i += 1

		except Exception as e:
			# Empty blocks are acceptable.
			if (not len(failedMatches)):
				logging.debug(f"Block {this.name} is empty.")
				return ""

			raise SyntaxError(f"Could not find content for {this.name} block in {failedMatches}.")
	return possibleContent

# SymmetricBlocks use the same symbols for both openings and closings.
@eons.kind(Block)
def SymmetricBlock(
	openings = [],
	content = "",
):
	# SymmetricBlocks should always have 1 opening and 1 closing.
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
	return this.parent.Function(this)

@eons.kind(Block)
def MetaBlock(
	compose = [],
):
	return this.parent.Function(this)

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

# Expressions build the contents of all other Blocks beside the CatchAllBlock.
@eons.kind(OpenEndedBlock)
def Expression(
	openings = [r';', r','],
	nest = [], # List of blocks that can be nested inside this block.
	exclusions = [
		'EOL',
	]
):
	return this.p[0]

# ExpressionSet is constructed from a series of Expressions.
# Each nest in a Expression is realized through a ExpressionSet.
@eons.kind(Block)
def ExpressionSet():

	if (isinstance(this.p[0], str)):
		return [this.p[0]]
	
	ret = this.p[0]
	
	if (isinstance(this.p[0], list)):
		try:
			if (isinstance(this.p[1], list)):
				ret = this.p[0] + this.p[1]			
			else:
				ret.append(this.p[1])
		except Exception as e:
			pass
	
	return ret