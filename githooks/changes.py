""" Compare file equality """
import os
import logging
import argparse
import difflib


def equality(source=None, target=None, verbose=False):
    """ :returns percentage of source lines in target. """

    def get_lines(file):
        if not os.path.exists(file):
            logging.warning('Missing source file %s', file)
            raise FileNotFoundError

        with open(file, 'r') as handle:
            return handle.readlines()


    sources = get_lines(args.source)
    target = get_lines(args.target)

    differ = difflib.Differ()
    result = differ.compare(sources, target)
    result = [line for line in result if not line.startswith('?')]
    removed = [line for line in result if line.startswith('-')]
    amount_origin = len(sources) - len(removed)

    percent_of_source = amount_origin/len(target)*100
    if args.v:
        added = [line for line in result if line.startswith('+')]
        print("Compared {args.source} to {args.target}".format(args=args))
        print(f"{amount_origin} source lines comprise target"
              f" {len(target)} lines ({percent_of_source:.2f} %%)")
        print(f"removed {len(removed)} / {len(sources)}")
        print(f"added {len(added)} lines")

    return percent_of_source


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=str)
    parser.add_argument('target', type=str)
    args = parser.parse_args()

    equality(source=args.source,
             target=args.target,
             verbose=True)
