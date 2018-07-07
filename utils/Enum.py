from enum import Enum


class EnumBase(Enum):
    @classmethod
    def get_chioces(cls):

        members = dir(cls)
        chioces = []
        for member in members:
            if isinstance(member, str) and member not in ['__class__', '__doc__', '__members__', '__module__']:
                chioces.append((cls[member].value, cls[member].name))
        return tuple(chioces)

