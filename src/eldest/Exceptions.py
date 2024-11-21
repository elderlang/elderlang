import eons

class ElderException(Exception, metaclass=eons.ActualType): pass

class HaltExecution(ElderException, metaclass=eons.ActualType): pass

class DefinitionException(ElderException, metaclass=eons.ActualType): pass