import eons

class HaltExecution(Exception, metaclass=eons.ActualType): pass