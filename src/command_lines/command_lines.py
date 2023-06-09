from typing import Union
from abc import ABC, abstractclassmethod
from dataclasses import dataclass
import re


class CommandLine(ABC):
    @staticmethod
    @abstractclassmethod
    def match(line: str) -> Union['CommandLine', None]:
        """
        All command line has a fixed structure, 
        So this function should return an instance of that command line 
        If the line complies with that structure
        Else it should return None
        """


class Space:
    @staticmethod
    def match(line: str):
        regex = r'\s*\n*'

        if (re.fullmatch(regex, line)):
            return Space()

        return None
    
@dataclass
class Student:
    name: str

    @staticmethod
    def match(line: str) -> 'Student':
        regex = r'Student\s+(?P<name>\w+)\s*\n*'

        if (match := re.fullmatch(regex, line)):
            return Student(name=match.group('name'))

        return None


@dataclass
class Presence:
    student_name: str
    day: int
    start_time: str
    end_time: str
    room: str

    @staticmethod
    def match(line: str) -> 'Presence':
        # This regular expression matches with the following tags
        # 1- name: An identifier (\w+)
        # 2- day: one integer between 1-7
        # 3- start_time: an hour in the format HH:MM (\d\d:\d\d)
        # 4- end_time: an hour in the format HH:MM (\d\d:\d\d)
        # 5- room: An identifier (\w+)
        regex = r'Presence\s+(?P<name>\w+)\s+(?P<day>[1234567])\s+(?P<start_time>\d\d:\d\d)\s+(?P<end_time>\d\d:\d\d)\s+(?P<room>\w+)\s*\n*'

        if (match := re.fullmatch(regex, line)):
            return Presence(
                student_name=match.group('name'),
                day=match.group('day'),
                start_time=match.group('start_time'),
                end_time=match.group('end_time'),
                room=match.group('room'),
            )

        return None


@dataclass
class Classroom:
    room_code: str
    building: str
    x: float
    y: float

    @staticmethod
    def match(line: str) -> 'Classroom':
        # This regular expression matches with the following tags
        # 1- room_code: room code (\w+)
        # 2- building: name building
        # 3- x: coordinated (\d+.\d+)
        # 4- y: coordinated (\d+.\d+)

        regex = r'Classroom\s+(?P<room_code>\w+)\s+(?P<building>\w+)\s+(?P<x>\d+(\.\d+){0,1})\s+(?P<y>\d+(\.\d+){0,1})\s*\n*'

        if (match := re.fullmatch(regex, line)):
            return Classroom(
                room_code= match.group('room_code'),
                building=match.group('building'),
                x=match.group('x'),
                y=match.group('y')
            )

        return None