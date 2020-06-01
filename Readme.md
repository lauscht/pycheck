# Githooks

In order to evaluate your python style consider a least pylint rating.
To do so, e.g. install the following git pre-commit hook to enable clean code.

    .git/hook/pre-commint
    #!/bin/sh
    python -m githooks.linter -warn --minimum 10

