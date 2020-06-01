import re
import os
from .execution import Exec


class Git:

    def __init__(self):
        self._re_get_changed_files_cmd = re.compile(r"[MA][\s+](.*[\.py])[\n$]?")

    def root(self):
        result = Exec("git rev-parse --show-toplevel").result()
        return result.stdout.strip()

    def last_commit(self):
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
        lines = self.diff_index()
        files = list(self._re_get_changed_files_cmd.findall(lines))
        if not files:
            return []

        root = self.root()
        return [os.path.join(root, f) for f in files]

