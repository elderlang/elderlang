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
		stringComponents[0] = stringComponents[0].replace(f"{{{block}}}", f"{{{i}}}", 1)
		stringComponents.append(parser.parse(lexer.tokenize(block)))

	# logging.critical(f"String components: {stringComponents}")

	return f"String({', '.join([str(c) for c in stringComponents])})"

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
	exclusions = [
		'tokens',
		'parser',
	],
	inclusions = [
		'newline',
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
):
	return ''

@eons.kind(OpenEndedBlock)
def Namespace(
	openings = [r':'],
	closings = [],
	representation = r':NAMESPACE',
	content = "LimitedExpression",
):
	# Getting strange recursion loop here.
	# Should always be :what_we_want
	return f"SetNamespace({this.p[1]})"

@eons.kind(OpenEndedBlock)
def Type(
	openings = [r'~'],
	closings = [],
	representation = r'~TYPE',
	doesSpaceClose = True,
	content = "LimitedExpression",
):
	# Same as Namespace, above.
	# (Type is always wrapped by other syntaxes, so no need for f"..."))
	return this.p[1]

@eons.kind(Block)
def Parameter(
	openings = [r'\('],
	closings = [r'\)'],
	representation = r'\(PARAMETER\)',
	content = "FullExpressionSet",
	inclusions = [
		'space.padding',
	],
):
	return this.parent.Function(this)

@eons.kind(Block)
def Execution(
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
def Container(
	openings = [r'\['],
	closings = [r'\]'],
	representation = r'\[CONTAINER\]',
	content = "FullExpressionSet",
	inclusions = [
		'space.padding',
	],
):
	return this.parent.Function(this)
