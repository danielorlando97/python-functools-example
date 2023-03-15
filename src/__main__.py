import sys
from .command_lines.command_line_handlers import CommandLineHandlers
from .command_lines.command_lines import Student, Presence
from .persistence.persistence import MemoryPersistenceLayer
from .use_cases import scholar_time_by_students


if __name__ == '__main__':

    args = sys.argv[1]
    # args = '../example.txt'
    with open(args, 'r') as f:
        commands = [Student, Presence]
        db = MemoryPersistenceLayer()
        handlers = CommandLineHandlers(db)

        for line in f.readlines():

            # We have to use for syntax because
            # with list compression we will iterate all list log  
            # and with iterator (filter + next) with have to call the function match two times  
            for cmd in commands:
                if (cmd := cmd.match(line)):
                    handlers.exec_cmd(cmd)
                    break

        scholar_time_by_students.run(db)
