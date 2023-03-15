from typing import Protocol, Iterator


class StudentRepositoryProtocol(Protocol):

    def __iter__(self) -> Iterator[str]:
        """"""


class PresenceRepositoryProtocol(Protocol):

    def compute_student_time(self, name) -> tuple[int, int]:
        """It should check when the segments intercept between them"""


def scholar_time_by_students(
    student_repo: StudentRepositoryProtocol,
    presence_repo: PresenceRepositoryProtocol
):
    for student in student_repo:
        days, delta = presence_repo.compute_student_time(student)

        if days == 0:
            print(f'{student}: 0 minutes')
        else:
            print(
                f'{student}: {delta} minutes in {days} day{"" if days == 1 else "s"}')
