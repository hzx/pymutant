#!/usr/bin/env python
import unittest

import os.path
import sys


TEST_PATH = os.path.abspath(os.path.dirname(__file__))
SRC_PATH = os.path.normpath(os.path.join(TEST_PATH, '../..'))
sys.path.insert(0, SRC_PATH)

TEST_MODULES = [
    'mutant.test.grammarparser_test',
    'mutant.test.preprocessor_test',
    'mutant.test.lexer_test',
    'mutant.test.parser_test',
    ]

def main():
  suite = unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)
  unittest.TextTestRunner().run(suite)

if __name__ == "__main__":
  main()
