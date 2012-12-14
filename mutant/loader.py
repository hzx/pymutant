from mutant.common import Module, Source
from mutant import errors
import os.path
import re
import glob

class Loader(object):
  """
  Take input mutant file.
  Create source table, mark comments line

  Take input module name. Search *.mut files in module (folder).
  Into main.mut search module imports.
  """

  def __init__(self):
    # import regex
    self.import_re = re.compile('^import\s+([a-zA-Z0-9\.]+)(?:\s+as\s+([a-zA-Z0-9]+))?$')

    # module maps by import name, need for cache
    self.modules = {}

  def setPaths(self, paths):
    """
    paths - paths where to find modules, paths divided by ,
    """
    abspaths = []
    # check folder paths exists and make it absolute
    for path in re.split('\s*,\s*', paths):
      if not os.path.exists(path):
        raise errors.PathNotFound(path)
      abspaths.append(os.path.abspath(path))

    self.paths = abspaths


  def convertNameToPath(self, name):
    # replace . to /
    return re.sub('\.', '/', name)

  def getModulePath(self, name, referer):
    modulepath = self.convertNameToPath(name)
    for path in self.paths:
      abspath = os.path.join(path, modulepath)
      if os.path.exists(abspath):
        return abspath
    raise errors.ModuleNotFound(name, referer)

  def loadModule(self, name, referer=None):
    # check cache for loaded module
    if self.modules.has_key(name): return self.modules[name]

    # load module source
    modulepath = self.getModulePath(name, referer)
    sources = self.loadSources(modulepath)
    imports = self.searchImports(sources)

    # create module
    module = Module(name, sources)

    # add module to cache
    self.modules[name] = module

    # load module imports
    for moduleName, alias in imports:
      linked = self.loadModule(moduleName, name)
      linkedName = None
      if len(alias) > 0: linkedName = alias
      else: linkedName = moduleName
      module.modules[linkedName] = linked

    return module

  def loadSources(self, folder):
    sources = []
    # search and read files in folder
    for filename in glob.glob(folder + '/*.mut'):
      with open(filename, 'r') as f: lines = f.read().splitlines()
      skiplines = self.searchComments(lines)
      sources.append(Source(filename, lines, skiplines))

    return sources

  def searchComments(self, lines):
    skiplines = []
    multiComment = False

    for num, line in enumerate(lines):
      # search multiline begin
      result = re.findall('^\s*/\*', line)
      if len(result) > 0:
        multiComment = True
        skiplines.append(num)
        continue
      if multiComment:
        skiplines.append(num)
        # search multiline end
        result = re.findall('^\s*\*/', line)
        if len(result) > 0: multiComment = False
        continue
      # search oneline comment
      result = re.findall('^\s*#.*', line)
      if len(result) > 0:
        skiplines.append(num)
        continue

    return skiplines

  def searchImports(self, sources):
    imports = []
    for source in sources:
      filename = os.path.basename(source.filename)
      # search imports only in main.mut file
      if filename == 'main.mut':
        for num, line in enumerate(source.lines):
          matches = self.import_re.findall(line)
          if len(matches) > 0:
            imports.append(matches[0])
            source.skiplines.append(num)
    return imports
