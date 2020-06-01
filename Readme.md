# Githooks

## Linter
In order to evaluate your python style consider a least pylint rating.
To do so, e.g add the following lines to your repositories or globel git pre-commit hooks.
You find them in `.git/hook/pre-commit`

    #!/bin/sh
    python -m githooks.linter --warn -minimum 10
    if [ $? -ne 0 ]
    then
      echo "The pylint rating did not meet expected values."
      exit 1
    fi


## Requirements

Please refer to the `requirements.txt` or simply install them

    >>> pip install -r requirements.txt
