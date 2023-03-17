from unittest import TestCase
from src.__main__ import main
from src.errors import FormatError

simple_example = """Student Marco
Student David
Student Fran
Presence Marco 1 09:02 10:17 R100
Presence Marco 3 10:58 12:05 R205
Presence David 5 14:02 15:46 F505"""

without_segmentation_example = """Student Marco
Student David
Student Fran
Presence Marco 1 09:02 10:17 R100
Presence Marco 3 10:58 12:05 R205
Presence David 5 14:02 15:46 F505
Presence Fran 1 09:02 12:05 R100
Presence Fran 1 10:58 13:17 R100
"""


class PipelineTest(TestCase):
    def test_main_pipeline_persistence_integration(self):
        
        answers = [
            "Marco: 142 minutes in 2 days",
            "David: 104 minutes in 1 day",
            "Fran: 0 minutes",
        ]

        for test, answer in zip(answers, main(simple_example.split('\n'))):
            assert test == answer

    def test_main_pipeline_persistence_integration_without_segmentation(self):
        
        answers = [
            "Marco: 142 minutes in 2 days",
            "David: 104 minutes in 1 day",
            "Fran: 255 minutes in 1 day",
        ]
        
        for test, answer in zip(answers, main(without_segmentation_example.split('\n'))):
            assert test == answer

    def test_bad_command_student(self):
        try:
            main("student david")
        except FormatError:
            pass

    def test_bad_command_students(self):
        try:
            main("students david")
        except FormatError:
            pass

    def test_bad_command_studnts(self):
        try:
            main("studnts david")
        except FormatError:
            pass

    def test_bad_command_presence(self):
        try:
            main("presence Marco 1 09:02 10:17 R100")
        except FormatError:
            pass

    def test_bad_command_precense(self):
        try:
            main("Precense Marco 1 09:02 10:17 R100")
        except FormatError:
            pass

    def test_bad_command_presence_without_name(self):
        try:
            main("Presence 1 09:02 10:17 R100")
        except FormatError:
            pass

    def test_bad_command_presence_without_day(self):
        try:
            main("Presence Marco 09:02 10:17 R100")
        except FormatError:
            pass

    def test_bad_command_presence_without_start(self):
        try:
            main("Presence Marco 1 10:17 R100")
        except FormatError:
            pass

    def test_bad_command_presence_without_run(self):
        try:
            main("Presence Marco 1 09:02 10:17")
        except FormatError:
            pass

    def test_bad_command_hello_word(self):
        try:
            main("Hello World!!!")
        except FormatError:
            pass