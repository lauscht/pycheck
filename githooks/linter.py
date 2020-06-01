import os
import re
import argparse
from githooks.execution import Exec
from githooks.gitwrap import Git


class Linter:

    def __init__(self):
        self._re_rating = re.compile(r"at ([\d\.]+)/10")

    def create_report(self, file):
        result = Exec("python -m pylint")(file)
        return result.stdout

    def extract_rating(self, lint_report):
        ratings = self._re_rating.findall(lint_report)
        try:
            return float(ratings[0])
        except IndexError:
            return 0

    def rating(self, file):
        lint_report = self.create_report(file)
        return self.extract_rating(lint_report)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('minimum_rating', default=10, nargs='?')
    parser.add_argument('-v', action='store_true')
    args = parser.parse_args()

    git = Git()
    print(git.last_commit())
    print(git.diff_index())
    files = git.get_staged_modules()
    linter = Linter()

    for file in files:
        if not os.path.exists(file):
            continue
        report = linter.create_report(file)
        rating = linter.extract_rating(report)
        if args.minimum_rating > rating:
            print(f"{file}: {rating}")
            if args.v:
                print(report)


if __name__ == '__main__':
    import sys
    sys.exit(main())