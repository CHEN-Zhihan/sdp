from abc import ABC
class DuplicationException(Exception,ABC):
    pass

class UsernameDuplication(DuplicationException):
    pass

class CourseNameDuplication(DuplicationException):
    pass

class ModulenameDuplication(DuplicationException):
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