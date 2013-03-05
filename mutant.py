#!/usr/bin/env python
import sys
import os
import os.path

MUTANT_FILE = os.path.realpath(__file__)
MUTANT_PATH = os.path.dirname(MUTANT_FILE)
CURRENT_PATH = os.path.abspath('.')


HELP = """
usage:
  mutant js

  mutant py
"""

def usage():
  print HELP

def taskJs():
  print 'task js not implemented'

def taskPy():
  print 'task py not implemented'

def main():
  taskMap = {
      'js': taskJs,
      'py': taskPy,
    }
  print 'main'

if __name__ == '__main__':
  sys.exit(main())
