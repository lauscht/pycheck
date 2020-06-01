"""
# GitWrap

Wrapper for commonly used git methods.

"""
import re
import os
from githooks.execution import Exec


class Git:
    """ A simple wrapper to some commonly used git-methods. """

    def __init__(self):
        self._re_get_changed_modules = re.compile(r"[MA][\s+](.*\.py)[\n$]?")

    @staticmethod
    def root():
        """ get the root folder of a git repository. """
        result = Exec("git rev-parse --show-toplevel").result()
        return result.stdout.strip()

    @staticmethod
    def last_commit():
        """ Retrieves last git hash """
        result = Exec("git rev-parse --verify HEAD").result()
        assert result.status == 0
        return result.stdout.strip()

    def diff_index(self):
        """ :returns changes to the repository """
        last_commit = self.last_commit()
        result = Exec("git diff-index --cached {last_commit}".format(last_commit=last_commit))()
        return result.stdout.strip()

    def get_staged_modules(self):
        """ :returns (list) with all staged python modules. """
        lines = self.diff_index()
        files = list(self._re_get_changed_modules.findall(lines))
        if not files:
            return []

        root = self.root()
        return [os.path.join(root, f) for f in files]
