from mutant.common import Source
import os.path
import re
from exceptions import Exception

class Preprocessor(object):
  """
  Take input mutant file.
  Create file table, line table, mark comments line
  array of maps
  { 'filename': '', 'lines': ['', ..], 'skiplines': [num, ..] }
  """

  def initialize(self, paths):
    """
    paths - language paths where to find sources
    """
    self.paths = paths

  def parse(self, filename):
    """
    filename - absolute file path
      or relative to compiler directory
    """
    self.filetable = []

    # if filename is abspath - use their dirname
    if not os.path.isabs(filename):
      filename = os.path.abspath(os.path.normpath(
        os.path.join(os.path.dirname(__file__), filename)))
    rootpath, filename = os.path.split(filename)

    self.parseFile(rootpath, filename)

    return self.filetable

  def pkgToFilename(self, pkg):
    names = pkg.split('.')
    return '/'.join(names) + '.mut'

  def parseFile(self, parentdir, filename):
    """
    Load files, process import and comments,
    create lines table, mark lines
    """
    # make filename path absolute
    filename = os.path.normpath(os.path.join(parentdir, filename))
    filedir = os.path.dirname(filename)
    if not os.path.exists(filename):
      raise Exception('Preprocessor: file not exists "%s"' % filename)

    for item in self.filetable:
      if filename == item.filename: return

    # lines num for skip - import and comments
    skiplines = []
    # multiline comment parse flag
    multiComment = False
    # read lines from filename
    with open(filename, 'r') as f: lines = f.readlines()
    # iterate over each line and search import file
    for linenum, line in enumerate(lines):
      # search import
      files = re.findall('^import\s+(.+)$', line)
      if len(files) > 0:
        skiplines.append(linenum)
        self.parseFile(filedir, self.pkgToFilename(files[0]))
        continue
      # search multiline comment begin
      result = re.findall('^\s*/\*', line)
      if len(result) > 0:
        multiComment = True
        skiplines.append(linenum)
        continue
      # search multiline comment end
      result = re.findall('^\s*\*/', line)
      if multiComment:
        if len(result) > 0: multiComment = False
        skiplines.append(linenum)
        continue
      # search comments
      result = re.findall('^\s*#.*', line)
      if len(result) > 0:
        skiplines.append(linenum)
        continue

    # add filename to table
    self.filetable.append(Source(filename, lines, skiplines))

#if __name__ == "__main__":
#  preprocessor = Preprocessor()
#  preprocessor.parse('../test/main.mut')
#  print "PARSED SOURCES"
#  for item in preprocessor.filetable: print item.filename
