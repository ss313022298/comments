
from enum import Enum


class Reviewtatus(Enum):
    Commit = 1
    Success = 2
    Faile = 3


class VerifyStatus(Enum):
    Commit = 1
    Success = 2
    Faile = 3


class CompanyRole(Enum):
    System = 1
    Property = 2
    SystemProperty = 3


class SystemStatus(Enum):
    OnLine = 1
    OffLine = 2



class EnumBase(Enum):
    @classmethod
    def get_chioces(cls):

        members = dir(cls)
        chioces = []
        for member in members:
            if isinstance(member, str) and member not in ['__class__', '__doc__', '__members__', '__module__']:
                chioces.append((cls[member].value, cls[member].name))
        return tuple(chioces)
    