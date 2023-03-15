from src.command_line_handlers import PersistenceLayerProtocol, PersistenceRepositoryProtocol
from src.tools import Singleton
from typing import Protocol, Dict, List
from collections import defaultdict
from bisect import bisect_left


class RepositoryProtocol(PersistenceRepositoryProtocol, Protocol):
    """"""


class PersistenceManager(metaclass=Singleton):
    def __init__(self) -> None:
        self.db: Dict[str, RepositoryProtocol] = {}

    def __getitem__(self, collection) -> RepositoryProtocol:
        return self.db[collection]

    @staticmethod
    def register(name):
        def f(cls):
            manager = PersistenceManager()
            manager.db[name] = cls()
            return cls

        return f


@PersistenceManager.register('Student')
class StudentRepository(RepositoryProtocol):
    def __init__(self) -> None:
        self.db: List[str] = []

    def create(self, name: str):
        self.db.append(name)

    def __iter__(self):
        return self.db.__iter__()

    def __contains__(self, value):
        return value in self.db


class MaskList:
    def __init__(self) -> None:
        self.inner_list = []

    def __getindex__(self, index):
        return self.inner_list[index]['start_min']

    def __len__(self):
        return len(self.inner_list)

    def insert(self, index, value):
        self.inner_list.insert(index, value)


@PersistenceManager.register('Presence')
class PresenceRepository(RepositoryProtocol):
    def __init__(self) -> None:
        self.db: Dict[str, Dict[int, MaskList]] = defaultdict(
            lambda: defaultdict(MaskList)
        )

    def create(
        self, name, day,
        start_time, start_min,
        end_time, end_min,
        delta_time, room
    ):

        if not name in PersistenceManager()['Student']:
            raise Exception("Unknown Student")

        body = {
            'start_time': start_time,
            'end_time': end_time,
            'start_min': start_min,
            'end_min': end_min,
            'delta_time': delta_time,
            'room': room
        }

        db_by_name = self.db[name]
        list_by_day = db_by_name[day]

        index = bisect_left(list_by_day, start_min)
        list_by_day.insert(index, body)

    def compute_student_time(self, name):
        """It should check when the segments intercept between them"""

        days, delta = 0, 0
        for item in self.db[name].values():
            days += 1
            delta += sum([x['delta_time'] for x in item.inner_list])

        return days, delta
