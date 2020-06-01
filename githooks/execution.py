import subprocess


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
            self._cmd +" " + " ".join(args),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        status = process.poll()
        return Result(status, stdout.decode(), stderr.decode())

    def result(self, *args):
        return self.__call__(*args)
