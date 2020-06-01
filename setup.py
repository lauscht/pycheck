""" githooks setup. """
from setuptools import setup, find_packages

setup(
    name="githook",
    version="0.1",
    packages=find_packages(),

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=["pylint>=2.5"],

    # metadata to display on PyPI
    author="Tobias Lausch",
    author_email="mail@lauscht.com",
    description="Convenience Git hooks for good code quality.",
    url="http://github.com/lauscht/githooks",   # project home page, if any
    classifiers=[
        "License :: OSI Approved :: Python Software Foundation License"
    ]

)
