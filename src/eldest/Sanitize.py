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

	types = [
		'bool',
		'float',
		'int',
		'string',
		'functor',
		'surface',
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
			input = re.sub(rf"(\\*)(['\"])\b{re.escape(keyword)}\b(\\*)(['\"])", rf"\1\2{keyword.upper()}\3\4", input)
		for type in this.types:
			input = re.sub(rf"(\\*)(['\"]*)(\(*)\b{re.escape(type)}\b(\\*)(['\"]*)(\)*)", rf"\3{type.upper()}\6", input)
		for symbol,replacement in this.symbols.items():
			input = re.sub(rf"(\\*)(['\"])(\w*){re.escape(symbol)}(\w*)(\\*)(['\"])", rf"\1\2\3{replacement.upper()}\4\5\6", input)
		return input

	def Soil(this, input):
		if (isinstance(input, list)):
			return [this.Soil(item) for item in input]

		for keyword in this.keywords:
			input = re.sub(rf"\b{keyword.upper()}\b", rf"{re.escape(keyword.lower())}", input)
		for type in this.types:
			input = re.sub(rf"(\(*)\b{type.upper()}\b(\)*)", rf"\1{type.lower()}\2", input)
		for symbol,replacement in this.symbols.items():
			input = re.sub(rf"{(replacement.upper())}", rf"{re.escape(symbol)}", input)
		return input