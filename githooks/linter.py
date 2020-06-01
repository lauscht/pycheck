#!/usr/bin/python
"""
Linter -  a small pylint wrapper

It may analyze staged changes of your git repository to check on code style.

    >>> python -m githooks.linter  --warn -minimum 10
    Your code was rated in average 9.5/10 with at least 8.49/10

For help run:
    >>> python -m githooks.linter --help

"""
import os
import re
import logging
import argparse
from githooks.execution import Exec
from githooks.gitwrap import Git


class Linter:
    """ Wrapper for pylints report module. """
    def __init__(self):
        self._re_rating = re.compile(r"at ([\d\.]+)/10")

    @staticmethod
    def create_report(file):
        """ Get Stdout from pylint report of a file """
        result = Exec("python -m pylint")(file)
        return result.stdout

    def extract_rating(self, lint_report):
        """ Exctract rating from a pylint report """
        ratings = self._re_rating.findall(lint_report)
        try:
            return float(ratings[0])
        except IndexError:
            return 0

    def rating(self, file):
        """ Get the pylint rating of a file. """
        lint_report = self.create_report(file)
        return self.extract_rating(lint_report)


def main():
    """ run this method to extract pylint report from your code. """
    parser = argparse.ArgumentParser()
    parser.add_argument('-minimum', default=10, type=float, nargs='?')
    parser.add_argument('--warn', action='store_true')
    parser.add_argument('-v', action='store_true')
    parser.add_argument('--disable_summary', action='store_true')

    args = parser.parse_args()
    least_expected_rating = args.minimum

    git = Git()
    files = git.get_staged_modules()
    if not files:
        return 0  # No Python module to get lint.

    ratings = []
    linter = Linter()

    for file in files:
        if not os.path.exists(file):
            logging.warning("Missing file %s", file)
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
