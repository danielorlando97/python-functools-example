from typing import Dict, List, Protocol, Iterable


class PersistenceScholarTimeProtocol(Protocol):
    def student_names(self) -> Iterable[str]:
        """"""

    def student_presence_group_by_day(self, student_name) -> Dict[int, List]:
        """It should check when the segments intercept between them"""

def run(
    repo: PersistenceScholarTimeProtocol
):
    for student in repo.student_names():
        group_by_day = repo.student_presence_group_by_day(student)

        days, delta = 0, 0
        for presences in group_by_day.values():
            days += 1
            delta += sum([item.delta_time for item in presences])

        if days == 0:
            print(f'{student}: 0 minutes')
        else:
            print(
                f'{student}: {delta} minutes in {days} day{"" if days == 1 else "s"}')
