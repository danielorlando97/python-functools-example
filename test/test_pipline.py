from unittest import TestCase
from src.command_lines.command_lines import Student, Presence
from src.persistence.persistence import MemoryPersistenceLayer
from src.command_lines.command_line_handlers import CommandLineHandlers

example = """Student Marco
Student David
Student Fran
Presence Marco 1 09:02 10:17 R100
Presence Marco 3 10:58 12:05 R205
Presence David 5 14:02 15:46 F505"""

class PipelineTest(TestCase):
    def test_main_pipeline_persistence_integration(self):

        commands = [Student, Presence]
        db = MemoryPersistenceLayer()
        handlers = CommandLineHandlers(db)

        for line in example.split('\n'):
            for cmd in commands:
                if (cmd := cmd.match(line)):
                    handlers.exec_cmd(cmd)
                    break

        student = list(db.student_names())
        assert len(student) == 3

        group = db.student_presence_group_by_day("Marco")
        assert len(group) == 2
    
        group = db.student_presence_group_by_day("David")
        assert len(group) == 1