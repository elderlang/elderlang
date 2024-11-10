from .Block import *
import eons

# NOTE: Normally, we would not append "Block" to the following child instances (e.g. "final"(ish) classes). However, we can't have name conflicts with the classes we use in Eldest.

@eons.kind(SymmetricBlock)
def UnformattedStringBlock(
	openings = [r"\'"],
	representation = "\\'UNFORMATTED_STRING\\'", #NOT a raw string
	content = None,
	overrides = [
		'prioritize',
	],
	inclusions = [
		'newline',
	],
):
	# UnformattedStrings are lexed wholesale.
	string = str(this.Engulf(this.GetProduct(0), escape=True))

	# Escape any newline characters.
	string = string.replace('\n', '\\n')

	return f"String('{string}')"

@eons.kind(SymmetricBlock)
def FormattedStringBlock(
	lexer = None,
	parser = None,
	openings = [r'"', r'`'],
	representation = '\"FORMATTED_STRING\"', #NOT a raw string
	content = None,
	nest = [
		'Execution',
	],
	overrides = [
		'prioritize',
	],
	inclusions = [
		'newline',
	],
):
	if (lexer is None):
		lexer = this.executor.Fetch('lexer')
	if (parser is None):
		parser = this.executor.Fetch('parser')

	rawString = f"'{this.GetProduct(0)[1:-1]}'" # Standardize quotations

	# This is what we want to do, but python does not support the P<-...> module (only P<...>)
	# executionBlocks = re.findall(r'{(?:[^{}]|(?P<open>{)|(?P<-open>}))*(?(open)(?!))}', rawString)

	executionBlocks = []

	openCount = 0
	openPos = 0
	for i,char in enumerate(rawString):
		if (char == '{'):
			openCount += 1
			openPos = i+1
		elif (char == '}'):
			openCount -= 1
		if (openCount == 0 and openPos > 0):
			# logging.critical(f"Execution block: {rawString[openPos:i]}")
			executionBlocks.append(rawString[openPos:i])
			openPos = 0

	if (openCount > 0):
		raise SyntaxError(f"Unbalanced curly braces in formatted string: {rawString}")

	# logging.critical(f"Execution blocks: {executionBlocks}")

	stringComponents = [rawString]
	for i, block in enumerate(executionBlocks):
		stringComponents[0] = stringComponents[0].replace(f"{{{block}}}", r"%s", 1)
		stringComponents.append(parser.parse(lexer.tokenize(block)))
	
	# Escape any newline characters only AFTER the rawString has been processed.
	stringComponents[0] = stringComponents[0].replace('\n', '\\\\n')

	# logging.critical(f"String components: {stringComponents}")

	# Wipe result data, since our return value here can apparently be clobbered by the parser calls.
	import eons #huh?
	this.result.data = eons.util.DotDict()

	return f"String({', '.join([str(c) for c in stringComponents])})"

@eons.kind(MetaBlock)
def StringBlock(
	compose = [
		'UnformattedStringBlock',
		'FormattedStringBlock',
	],
	representation = r'`STRING`',
	content = None,
	exclusions = ['lexer'],
	overrides = [
		'prioritize',
	],
):
	return this.GetProduct(0) # already parsed.

@eons.kind(Block)
def BlockComment(
	openings = [r'/\*'],
	closings = [r'\*/'],
	representation = r'/\\*BLOCK_COMMENT\\*/',
	content = None,
	exclusions = [
		'tokens',
		'parser',
	],
	inclusions = [
		'newline',
		'space.padding',
	],
):
	return ''

@eons.kind(OpenEndedBlock)
def LineComment(
	openings = [r'#', r'//'],
	closings = [],
	representation = r'//LINE_COMMENT',
	content = None,
	exclusions = [
		'tokens',
		'parser',
	],
	inclusions = [
		'space.padding',
	],
):
	return ''

@eons.kind(OpenEndedBlock)
def KindBlock(
	openings = [r':'],
	closings = [],
	representation = r':KIND',
	content = "LimitedExpression",
):
	if (len(this.p) <= 1):
		return "Kind()"

	if (this.GetProduct(0) in openings and this.GetProduct(1) in openings):
		return "Kind()"
	if (this.GetProduct(0).startswith('Kind')):
		return this.GetProduct(0)
	kind = this.Engulf(this.GetProduct(1), escape=True)
	if (len(kind)):
		kind = f"'{kind}'"
	return f"Kind({kind})"

@eons.kind(Block)
def ParameterBlock(
	openings = [r'\('],
	closings = [r'\)'],
	representation = r'\\(PARAMETER\\)',
	content = "FullExpressionSet",
	inclusions = [
		'space.padding',
	],
):
	return this.parent.Function(this)

@eons.kind(Block)
def ExecutionBlock(
	openings = [r'{'],
	closings = [r'}'],
	representation = r'{{EXECUTION}}',
	content = "FullExpressionSet",
	inclusions = [
		'space.padding',
	],
):
	return this.parent.Function(this)

@eons.kind(Block)
def ContainerBlock(
	openings = [r'\['],
	closings = [r'\]'],
	representation = r'\\[CONTAINER\\]',
	content = "FullExpressionSet",
	inclusions = [
		'space.padding',
	],
	buildContainer = True,
):
	return this.parent.Function(this)
