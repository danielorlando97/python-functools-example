from unittest import TestCase
from src.persistence.models import StudentModel, PresenceModel
from src.persistence.persistence import MemoryPersistenceLayer
from src.errors import PersistenceError

class MemoryPersistence(TestCase):

    def create_default_presence(
        self,             
        name="Daniel",
        day=1,
        start_time='01:20',
        start_min=80,
        end_time='2:20',
        end_min=140,
        delta_time=60,
        room='F100'
    ):
         
        return PresenceModel(
            name,
            day,
            start_time,
            start_min,
            end_time,
            end_min,
            delta_time,
            room
        )
         

    def test_success_save_student(self):
        db = MemoryPersistenceLayer()

        db.create(StudentModel("Daniel"))

        assert len(db.db) == 1
        assert 'Daniel' in db.db

    def test_success_save_presence(self):
        db = MemoryPersistenceLayer()

        db.create(StudentModel("Daniel"))
        presence = self.create_default_presence()

        db.create(presence)


        assert len(db.db['Daniel']) == 1
        assert 1 in db.db['Daniel']
        assert len(db.db['Daniel'][1]) == 1
        assert db.db['Daniel'][1][0] == presence

    def test_success_void_student_name(self):
            db = MemoryPersistenceLayer()
            result = list(db.student_names())

            assert len(result) == 0

    def test_success_student_name(self):
            db = MemoryPersistenceLayer()
            db.create(StudentModel("Daniel"))
            result = list(db.student_names())

            assert len(result) == 1
            assert result[0] == 'Daniel'

    def test_success_group_by(self):
        db = MemoryPersistenceLayer()

        db.create(StudentModel("Daniel"))
        db.create(StudentModel("Mathias"))

        db.create(self.create_default_presence())
        db.create(self.create_default_presence(name='Mathias'))
        db.create(self.create_default_presence(name='Mathias', day=2))
        db.create(self.create_default_presence())

        result = db.student_presence_group_by_day("Daniel")
        assert len(result) == 1
        assert 1 in result
        assert len(result[1]) == 2

        result = db.student_presence_group_by_day("Mathias")
        assert len(result) == 2
        assert 1 in result and 2 in result
        assert len(result[1]) == 1
        assert len(result[2]) == 1

    def test_fail_create_presence(self):
        db = MemoryPersistenceLayer()
        try:
            db.create(self.create_default_presence())
            assert False
        except PersistenceError:
            pass

    def test_fail_create_presence(self):
        db = MemoryPersistenceLayer()
        try:
            db.student_presence_group_by_day("Daniel")
            assert False
        except PersistenceError:
            pass