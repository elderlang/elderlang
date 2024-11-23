import eons
import re

# This file contains information from Eldest, which is downstream from the elderlangdefinitions, where this is located.
# All this information is hard coded and needs to be kept up to date with any downstream changes.
# The reason to do this is so that sanitization is not applied across the board. For example, "hello wolf!" should not become "hello wolfNOT".

class Sanitize (eons.Functor):

	keywords = [
		'break',
		'continue',
		'case',
		'default',
		'else',
		'for',
		'if',
		'not',
		'return',
		'switch',
		'while',
		'try',
		'catch',
		'as',
	]

	keywordInvokations = [
		'break',
		'continue',
	]

	types = [
		'bool',
		'float',
		'int',
		'string',
		'functor',
		'container',
		'pointer',
	]

	symbols = {
		'!': 'not',
		'=': 'eq',
		'&': 'and',
		'|': 'or',
		'>': 'gt',
		'<': 'lt',
		'+': 'plus',
		'-': 'minus',
		'*': 'times',
		'/': 'divide',
		'^': 'pow',
		'%': 'mod',
	}

	allBuiltins = [
		'BREAK',
		'CONTINUE',
		'CASE',
		'DEFAULT',
		'ELSE',
		'FOR',
		'IF',
		'NOT',
		'RETURN',
		'SWITCH',
		'WHILE',
		'TRY',
		'CATCH',
		'BOOL',
		'FLOAT',
		'INT',
		'STRING',
		'FUNCTOR',
		'CONTAINER',
		'POINTER',
		'NOT',
		'EQ',
		'EQEQ',
		'AND',
		'ANDAND',
		'OR',
		'OROR',
		'GT',
		'GTEQ',
		'LT',
		'LTEQ',
		'PLUS',
		'PLUSEQ',
		'MINUS',
		'MINUSEQ',
		'TIMES',
		'TIMESEQ',
		'DIVIDE',
		'DIVIDEEQ',
		'POW',
		'POWEQ'
		'MOD',
		'MODEQ',
	]

	operatorMap = {
		'EQ': '__eq__',
		'PLUS': '__add__',
		'MINUS': '__sub__',
		'TIMES': '__mul__',
		'DIVIDE': '__truediv__',
		'MOD': '__mod__',
		'PLUSEQ': '__iadd__',
		'MINUSEQ': '__isub__',
		'TIMESEQ': '__imul__',
		'DIVIDEEQ': '__idiv__',
		'MODEQ': '__imod__',
		'POW': '__pow__',
		'AND': '__and__',
		'OR': '__or__',
		'ANDAND': '__and__',
		'OROR': '__or__',
		'GT': '__gt__',
		'GTEQ': '__ge__',
		'LT': '__lt__',
		'LTEQ': '__le__',
		'EQEQ': '__eq__',
	}

	def __init__(this, name="Sanitize"):
		super().__init__(name)

		this.arg.kw.required.append('input')

		this.arg.mapping.append('input')
		
	def Function(this):
		return this.Clean(this.input)

	def Clean(this, input):
		if (isinstance(input, list)):
			return [this.Clean(item) for item in input]

		for keyword in this.keywords:
			# For whole files
			# input = re.sub(rf"(\\*['\"])\b{re.escape(keyword)}\b(\\*['\"])", rf"\1{keyword.upper()}\2", input)

			# For individual words
			input = re.sub(f"^{re.escape(keyword)}$", keyword.upper(), input)

		for type in this.types:
			# For whole files
			# input = re.sub(rf"(\\*)(['\"]*)(\(*)\b{re.escape(type)}\b(\\*)(['\"]*)(\)*)([^=])", rf"\3{type.upper()}\6\7", input)

			# For individual words
			input = re.sub(f"^{re.escape(type)}$", type.upper(), input)

		# For whole files
		# symbolBorder = rf"[a-zA-Z0-9{''.join([re.escape(sym) for sym in this.symbols.keys()])}]"
		# for symbol,replacement in this.symbols.items():
		# 	preBorder = symbolBorder.replace(re.escape(symbol), '')
		# 	def ReplaceSymbol(match):
		# 		prefix, expr, suffix = match.groups()
		# 		ret = f"{prefix}{expr.replace(symbol, replacement.upper())}{suffix}"
		# 		# logging.debug(ret)
		# 		return ret
		# 	toMatch = rf"(\\*['\"])({preBorder}*?{re.escape(symbol)}{symbolBorder}*)(\\*['\"])"
		# 	# logging.debug(toMatch)
		# 	input = re.sub(toMatch, ReplaceSymbol, input)

		# For individual words
		for symbol,replacement in this.symbols.items():
			input = re.sub(re.escape(symbol), replacement.upper(), input)

		for keyword in this.keywordInvokations:
			# For whole files
			# input = re.sub(rf"(\\*['\"]){keyword.upper()}(\\*['\"])", rf"\1{keyword.upper()}()\2", input)

			# For individual words
			input = re.sub(f"^{re.escape(keyword)}$", f"{keyword.upper()}()", input)

		return input

	def Soil(this, input):
		if (isinstance(input, list)):
			return [this.Soil(item) for item in input]

		for keyword in this.keywords:
			input = re.sub(rf"\b{keyword.upper()}\b", rf"{keyword.lower()}", input)
		for type in this.types:
			input = re.sub(rf"(\(*)\b{type.upper()}\b(\)*)", rf"\1{type.lower()}\2", input)
		for symbol,replacement in this.symbols.items():
			input = re.sub(rf"(\\*['\"]?){(replacement.upper())}(\\*['\"]?)", rf"{symbol}", input)
		return input