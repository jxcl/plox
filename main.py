import sys

from scanner import Scanner

class Lox():

    def __init__(self):
        self.has_errors = False

    def run(self, source):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        for t in tokens:
            print(t)

        return

    def run_file(self, filename):
        with open(filename, 'r') as fp:
            source = fp.read()
            self.run(source)


        if self.has_errors:
            return 65
        else:
            return 0

    def run_prompt(self):
        while True:
            print("> ", end="")
            self.run(input())

            self.has_errors = False
        return

if __name__ == '__main__':
    if len(sys.argv[1:]) > 1:
        print("Usage: plox [script]")

    elif len(sys.argv[1:]) == 1:
        l = Lox()
        l.run_file(sys.argv[1])

    else:
        l = Lox()
        l.run_prompt()
