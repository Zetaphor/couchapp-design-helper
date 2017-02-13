#!/usr/bin/env python
import os
import couchlib

couchlib.cloneAllDocs(couchlib.getAllDocs())

currentDir = os.path.abspath(couchlib.root_dir)
for root, dirs, files in os.walk(currentDir):
    for fileName in files:
        if fileName.endswith('.json'):
            if (root.endswith('/fulltext')):
                couchlib.fullTextJsonToJs(os.path.abspath(root), fileName)
        elif fileName.endswith('.js'):
            couchlib.beautifyJsFile(os.path.abspath(root), fileName)
