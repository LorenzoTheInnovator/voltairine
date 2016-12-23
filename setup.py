#! /usr/bin/env python

from setuptools import setup
setup(name="voltairine",
      version="0.1",
      # packages=["pyborg"],
      scripts=['voltairine.py'],
      author="Goat and Gooseberry Collective",
      author_email="info@gooseberrycollective.net",
      description="Chat bot for Anarchism discord",
      license="GPL v3",
      install_requires=["discord.py", "toml"],
      url="https://github.com/gooseberrycollective/voltairine",
      classifiers=["Topic :: Communications :: Chat",
                   "Topic :: Games/Entertainment"])
