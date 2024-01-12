import eons
import re

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
		'BOOL',
		'FLOAT',
		'INT',
		'STRING',
		'FUNCTOR',
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
			input = re.sub(rf"(\\*['\"])\b{re.escape(keyword)}\b(\\*['\"])", rf"\1{keyword.upper()}\2", input)

		for type in this.types:
			input = re.sub(rf"(\\*)(['\"]*)(\(*)\b{re.escape(type)}\b(\\*)(['\"]*)(\)*)([^=])", rf"\3{type.upper()}\6\7", input)
			# input = re.sub(rf"(\\*)(['\"]*)(\(*)\b{re.escape(type)}\b(\\*)(['\"]*)(\)*)([^=])", rf"\1\2\3{type.upper()}\4\5\6\7", input)

		symbolBorder = rf"[a-zA-Z0-9{''.join([re.escape(sym) for sym in this.symbols.keys()])}]"
		for symbol,replacement in this.symbols.items():
			preBorder = symbolBorder.replace(re.escape(symbol), '')
			def ReplaceSymbol(match):
				prefix, expr, suffix = match.groups()
				ret = f"{prefix}{expr.replace(symbol, replacement.upper())}{suffix}"
				# logging.debug(ret)
				return ret
			toMatch = rf"(\\*['\"])({preBorder}*?{re.escape(symbol)}{symbolBorder}*)(\\*['\"])"
			# logging.debug(toMatch)
			input = re.sub(toMatch, ReplaceSymbol, input)

		for keyword in this.keywordInvokations:
			input = re.sub(rf"(\\*['\"]){keyword.upper()}(\\*['\"])", rf"\1{keyword.upper()}()\2", input)

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