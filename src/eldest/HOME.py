# HOME is a singleton that stores the "globals" for elder.
# HOME can be explicitly referenced using the ~/ notation.
class HOME:
	def __init__(this):
		# Singletons man...
		if "instance" not in HOME.__dict__:
			HOME.instance = this
		else:
			return None
		
		this.exec = None

	@staticmethod
	def Instance():
		if "instance" not in HOME.__dict__:
			HOME()
		return HOME.instance

	def __getattr__(this, name):
		try:
			return object.__getattribute__(this, name)
		except:
			try:
				ex = object.__getattribute__(this, 'exec')
				return getattr(ex, name)
			except:
				return None

	def __setattr__(this, name, value):
		try:
			ex = object.__getattribute__(this, 'exec')
			setattr(ex, name, value)
		except:
			object.__setattr__(this, name, value)