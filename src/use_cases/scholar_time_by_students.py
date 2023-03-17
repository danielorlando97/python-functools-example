from typing import Dict, List, Protocol, Iterable


class PersistenceScholarTimeProtocol(Protocol):
    def student_names(self) -> Iterable[str]:
        """It should return an iterable with the names of students in the system"""

    def student_presence_group_by_day(self, student_name) -> Dict[int, List]:
        """It should return each student's presence group by the presence days"""

def run(
    repo: PersistenceScholarTimeProtocol
):
    for student in repo.student_names():
        group_by_day = repo.student_presence_group_by_day(student)

        days, delta = 0, 0
        for presences in group_by_day.values():
            days += 1

            # In the database, there may be errors and overlapping presence instances,
            # so that the total number of minutes cannot be calculated with a simple sum. 
            presences.sort(key=lambda x:x.start_min)
            # Each key in the dict meads a day where the student went to the school
            # So, there are minimaly a presente instance 
            pivot = presences[0] 
            delta += pivot.delta_time
            for item in presences[1:]:
                if pivot.end_min <= item.start_min:
                    # The student went out and then came back in. Example by symbols ()[]
                    delta += item.delta_time
                elif pivot.end_min < item.end_min:
                    # entered twice and then exited twice more. Example by symbols ([)]
                    print("Warning: The information might be incomplete")
                    delta += item.end_min - pivot.end_min
                else:
                    # One presence is a subprocense of the other Example by symbols ([])
                    print("Warning: The information might be incomplete")
                    continue

                pivot = item
                    

        if days == 0:
            yield f'{student}: 0 minutes'
        else:
            yield f'{student}: {delta} minutes in {days} day{"" if days == 1 else "s"}'
