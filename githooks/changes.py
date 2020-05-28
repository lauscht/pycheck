import re
import os
import subprocess
from pylint import epylint as lint


class Result:
    def __init__(self, status, stdout, stderr):
        self.status = status
        self.stdout = stdout
        self.stderr = stderr


class Exec:
    def __init__(self, cmd):
        self._cmd = cmd
    
    def __call__(self, *args):
        process = subprocess.Popen(
            self._cmd +" "+ " ".join(args),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        status = process.poll()
        return Result(status, stdout.decode(), stderr.decode())

    def result(self, *args):
        return self.__call__(*args)
            

class Git:

    def __init__(self):
        self._re_get_changed_files_cmd = re.compile(r"A[\s+](.*[\.py])[\n$]?")

    def last_commit(self):
        result = Exec("git rev-parse --verify HEAD").result()
        assert result.status == 0
        return result.stdout.strip()

    def diff_index(self):
        last_commit = self.last_commit()
        result = Exec("git diff-index --cached {last_commit}".format(last_commit=last_commit))()
        return result.stdout.strip()

    def get_changed_files(self):
        lines = self.diff_index()
        files = self._re_get_changed_files_cmd.findall(lines)
        return files


class Linter:

    def __init__(self):
        self._re_rating = re.compile(r"at ([\d\.]+)/10")

    def lint(self, file):
        result = Exec("python -m pylint")(file)
        return result.stdout

    def rating(self, file):
        output = self.lint(file)
        ratings = self._re_rating.findall(output)
        try:
            return float(ratings[0])
        except IndexError:
            return 0
        

if __name__ == '__main__':
    git = Git()
    print(git.last_commit())
    print(git.diff_index())
    files = git.get_changed_files()
    linter = Linter()

    for file in files:
        if not os.path.exists(file):
            continue
        print(file)
        print(linter.rating(file))
