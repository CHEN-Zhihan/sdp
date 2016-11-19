from abc import ABC
class NameDuplication(Exception):
    pass


class AlreadyException(Exception,ABC):
    pass

class AlreadyEnrolled(AlreadyException):
    pass

class AlreadyOpened(AlreadyException):
    pass

class NotOwnerException(Exception):
    pass

class NotEnrolledException(Exception):
    pass

class NoModuleException(Exception):
    pass