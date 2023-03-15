from typing import Protocol, Union
from dataclasses import dataclass
import re


class CommandLine(Protocol):
    @staticmethod
    def match(line: str) -> Union['CommandLine', None]:
        """
        All command line has a fixed structure, 
        So this function should return an instance of that command line 
        If the line complies with that structure
        Else it should return None
        """


@dataclass
class Student(CommandLine):
    name: str

    @staticmethod
    def match(line: str) -> Union['Student', None]:
        regex = r'Student\s+(?P<name>\w+)'

        if (match := re.fullmatch(regex, line)):
            return Student(match.group('name'))

        return None


@dataclass
class Presence(CommandLine):
    student_name: str
    day: int
    start_time: str
    end_time: str
    room: str

    @staticmethod
    def match(line: str) -> Union['Presence', None]:
        # This regular expression matches with the following tags
        # 1- name: An identifier (\w+)
        # 2- day: one integer between 1-7
        # 3- start_time: an hour in the format HH:MM (\d\d:\d\d)
        # 4- end_time: an hour in the format HH:MM (\d\d:\d\d)
        # 5- room: An identifier (\w+)
        regex = r'Presence\s+(?P<name>\w+)\s+(?P<day>[1234567])\s+(?P<start_time>\d\d:\d\d)\s+(?P<end_time>\d\d:\d\d)\s+(?P<room>\w+)'

        if (match := re.fullmatch(regex, line)):
            return Presence(
                student_name=match.group('name'),
                day=match.group('day'),
                start_time=match.group('start_time'),
                end_time=match.group('end_time'),
                room=match.group('room'),
            )

        return None
