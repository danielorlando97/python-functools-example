import sys
from .command_lines.command_line_handlers import CommandLineHandlers
from .command_lines.command_lines import Student, Presence, Space
from .persistence.persistence import MemoryPersistenceLayer
from .use_cases import scholar_time_by_students
from .errors import FormatError

def main(lines):
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

if __name__ == '__main__':

    try:
        args = sys.argv[1]
    except IndexError:
        raise FormatError("The program expect a file to read")
    # args = '../example.txt'
    with open(args, 'r') as f:
        for answer in main(f.readlines()):
            print(answer)
