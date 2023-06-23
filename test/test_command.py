from unittest import TestCase
from src.command_lines.command_lines import Student, Presence, Classroom


class StudentCommandTest(TestCase):
    def test_success_match(self):

        cmd = 'Student Matthias'
        result = Student.match(cmd)

        assert result != None

    def test_success_match_with_endline(self):

        cmd = 'Student Matthias\n'
        result = Student.match(cmd)

        assert result != None

    def test_success_match_with_spaces(self):

        cmd = 'Student Matthias   '
        result = Student.match(cmd)

        assert result != None

    def test_success_match_with_spaces_and_endline(self):

        cmd = 'Student Matthias   \n'
        result = Student.match(cmd)

        assert result != None


class PresenceCommandTest(TestCase):
    def test_success_match(self):

        cmd = 'Presence Matthias 2 09:04 10:35 F100'
        result = Presence.match(cmd)

        assert result != None

    def test_success_match_with_endline(self):

        cmd = 'Presence Matthias 2 09:04 10:35 F100\n'
        result = Presence.match(cmd)

        assert result != None

    def test_success_match_with_spaces(self):

        cmd = 'Presence  Matthias   2 09:04  10:35 F100   '
        result = Presence.match(cmd)

        assert result != None

    def test_success_match_with_spaces_and_endline(self):

        cmd = 'Presence  Matthias   2 09:04  10:35 F100   \n'
        result = Presence.match(cmd)

        assert result != None


class CommandCommandTest(TestCase):
    def test_success_match(self):

        cmd = 'Classroom R100 LAB 15.4 16'
        result = Classroom.match(cmd)

        assert result != None
