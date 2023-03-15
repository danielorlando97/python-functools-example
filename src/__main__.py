import sys
from .command_line_handlers import CommandLineHandlers
from .command_lines import Student, Presence
from .persistence import PersistenceManager
from .queries import scholar_time_by_students

if __name__ == '__main__':

    args = sys.argv[1]
    print(args)
    with open(args, 'r') as f:
        commands = [Student, Presence]
        db = PersistenceManager()
        handlers = CommandLineHandlers(db)

        for line in f.readlines():
            print(line)
            try:
                cmd = next(filter(lambda x: x.match(line), commands))
            except StopIteration:
                raise Exception("Command Structure Error")

            handlers.exec_cmd(cmd)

        scholar_time_by_students(db['Student'], db['Presence'])
