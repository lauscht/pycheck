import os
import re
import logging
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
    parser.add_argument('-minimum', default=9, nargs='?')
    parser.add_argument('--warn', action='store_true')
    parser.add_argument('-v', action='store_true')
    parser.add_argument('--disable_summary', action='store_true')

    args = parser.parse_args()
    least_expected_rating = args.minimum

    git = Git()
    files = git.get_staged_modules()
    linter = Linter()

    ratings = []
    for file in files:
        if not os.path.exists(file):
            logging.warning("Missing file {file}".format(file=file))
            continue

        report = linter.create_report(file)
        rating = linter.extract_rating(report)
        ratings.append((rating))
        if rating < least_expected_rating:
            if args.warn or args.v:
                print("{file}: {rating}".format(file=file, rating=rating))
            if args.v:
                print(report)

    if not args.disable_summary:
        print("Your code was rated in average {avg:.2f}/10 with at least {min:.2f}/10".format(
            avg=(sum(ratings) / len(ratings)), min=min(ratings)
        ))

    if any(r < least_expected_rating for r in ratings):
        return -1
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
