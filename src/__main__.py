import sys
from .command_lines.command_line_handlers import CommandLineHandlers
from .command_lines.command_lines import Student, Presence, Space, Classroom
from .persistence.persistence import MemoryPersistenceLayer
from .use_cases import scholar_time_by_students
from .use_cases import scholar_time_by_students_and_classroom
from .errors import FormatError

def presence_students(lines):
    commands = [Student, Presence, Space]
    db = MemoryPersistenceLayer()
    handlers = CommandLineHandlers(db)
    
    for line in lines:
        try:
            cmd = next(filter(
                lambda x:x, map(lambda x: x.match(line), commands) 
            ))
        except StopIteration:
            print(line)
            raise FormatError("Bad Command")
        
        handlers.exec_cmd(cmd)
    
    return scholar_time_by_students.run(db)

def presence_building(lines, building):
    commands = [Student, Presence, Space, Classroom]
    db = MemoryPersistenceLayer()
    handlers = CommandLineHandlers(db)
    
    for line in lines:
        try:
            cmd = next(filter(
                lambda x:x, map(lambda x: x.match(line), commands) 
            ))
        except StopIteration:
            print(line)
            raise FormatError("Bad Command")
        
        handlers.exec_cmd(cmd)
    
    return scholar_time_by_students_and_classroom.run(db, building)


if __name__ == '__main__':

    try:
        report = sys.argv[1]
    except IndexError:
        raise FormatError("The program expect a report name")
    
    if report == 'classroom':
        #python -m src classroom file GIMNASIO 
        if len(sys.argv) != 4:
            raise FormatError("The program expect a file to read and a building name")

        with open(sys.argv[2], 'r') as f:
            for answer in presence_students(f.readlines(), sys.argv[3]):
                print(answer)

    if report == 'presence':
        #python -m src presence file 
        try:
            args = sys.argv[1]
        except IndexError:
            raise FormatError("The program expect a file to read")

        # args = '../example.txt'
        with open(args, 'r') as f:
            for answer in presence_students(f.readlines()):
                print(answer)
