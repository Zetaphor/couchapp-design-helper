#!/usr/bin/env python
import os
import couchlib
from shutil import copyfile, rmtree
from subprocess import call
from mkdirp import mkdir_p

startDir = os.path.dirname(os.path.realpath(__file__))
currentDir = os.path.abspath(couchlib.root_dir)
rcFile = os.path.abspath(couchlib.rc_file)
convertedFiles = []

mkdir_p('./tmp')

for root, dirs, files in os.walk(couchlib.root_dir):
    for fileName in files:
        if fileName.endswith('.js'):
            outputDir = os.path.abspath('./tmp/' + root)
            mkdir_p(outputDir)
            if root.endswith('/fulltext'):
                couchlib.fullTextJsToJson(os.path.abspath(root), fileName, outputDir)
            else:
                couchlib.minifyJs(os.path.abspath(root), fileName, outputDir)

os.chdir('./tmp/' + couchlib.root_dir)
for root, dirs, files in os.walk('.'):
    topLevel = root.count('/') is 1 and root != './tmp'
    if topLevel:
        copyfile(rcFile, os.path.abspath(root) + '/.couchapprc')
        call(["couchapp", "push"], cwd=os.path.abspath(root))
        print 'Pushed ' + root[1:]

os.chdir(startDir)
rmtree(os.path.abspath('./tmp'))
