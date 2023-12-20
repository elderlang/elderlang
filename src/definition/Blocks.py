from .Block import *
import eons

@eons.kind(SymmetricBlock)
def UnformattedString(
	openings = [r"\'"],
	representation = "\\'UNFORMATTED_STRING\\'", #NOT a raw string
	content = None
):
	# UnformattedStrings are lexed wholesale.
	return this.p[0]

@eons.kind(SymmetricBlock)
def FormattedString(
	lexer = None,
	parser = None,
	openings = [r'"', r'`'],
	representation = '\"FORMATTED_STRING\"', #NOT a raw string
	content = None,
	nest = [
		'Execution',
	]
):
	if (lexer is None):
		lexer = this.FetchWithout(['this'], 'lexer')
	if (parser is None):
		parser = this.Fetch(['this'], 'parser')
	
	rawString = this.p[0]
	
	# This is what we want to do, but python does not support the P<-...> module (only P<...>)
	# executionBlocks = re.findall(r'{(?:[^{}]|(?P<open>{)|(?P<-open>}))*(?(open)(?!))}', rawString)

	executionBlocks = []

	openCount = 0
	openPos = 0
	for i,char in enumerate(rawString):
		if (char == '{'):
			openCount += 1
			openPos = i
		elif (char == '}'):
			openCount -= 1
		if (not openCount and openPos):
			executionBlocks.append(rawString[openPos:i])
	
	if (openCount > 0):
		raise SyntaxError(f"Unbalanced curly braces in formatted string: {rawString}")
	
	# logging.critical(f"Execution blocks: {executionBlocks}")

	stringComponents = [rawString]
	for i, block in enumerate(executionBlocks):
		stringComponents[0].replace(block, f"{{i}}", 1)
		stringComponents.append(parser.parse(lexer.tokenize(block)))

	# logging.critical(f"String components: {stringComponents}")

	return stringComponents

@eons.kind(MetaBlock)
def String(
	compose = [
		'UnformattedString',
		'FormattedString',
	],
	representation = r'`STRING`',
	content = None,
	exclusions = ['lexer'],
):
	return this.p[0] # already parsed.

@eons.kind(Block)
def BlockComment(
	openings = [r'/\*'],
	closings = [r'\*/'],
	representation = r'/\*BLOCK_COMMENT\*/',
	content = None,
):
	return ''

@eons.kind(OpenEndedBlock)
def LineComment(
	openings = [r'#', r'//'],
	closings = [],
	representation = r'//LINE_COMMENT',
	content = None,
):
	return ''

@eons.kind(OpenEndedBlock)
def Namespace(
	openings = [r':'],
	closings = [],
	representation = r':NAMESPACE',
	content = "LimitedExpressionSet",
):
	return this.parent.Function(this)

@eons.kind(OpenEndedBlock)
def Type(
	openings = [r'~'],
	closings = [],
	representation = r'~TYPE',
	doesSpaceClose = True,
	content = "LimitedExpressionSet",
):
	return this.parent.Function(this)

@eons.kind(Block)
def Parameter(
	openings = [r'\('],
	closings = [r'\)'],
	representation = r'\(PARAMETER\)',
	content = "FullExpressionSet",
):
	return this.parent.Function(this)

@eons.kind(Block)
def Execution(
	openings = [r'{'],
	closings = [r'}'],
	representation = r'{{EXECUTION}}',
	content = "FullExpressionSet",
):
	return this.parent.Function(this)

@eons.kind(Block)
def Container(
	openings = [r'\['],
	closings = [r'\]'],
	representation = r'\[CONTAINER\]',
	content = "FullExpressionSet",
):
	return this.parent.Function(this)
