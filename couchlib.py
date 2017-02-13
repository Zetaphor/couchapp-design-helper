import json
import urllib2
import base64
import os
from jsmin import jsmin
from subprocess import call
from mkdirp import mkdir_p

# Config
host = 'localhost'
port = 5984
db_name = 'app'
username = 'admin'
password = 'root'
root_dir = 'design-docs'
rc_file = '.couchapprc'

# URL to pull all docs list from
couch_all_docs_url = 'http://%s:%s/%s/_all_docs?startkey="_design/"&endkey="_design0"' % (host, port, db_name)

# URL to pass to couchapp for pull
couch_doc_url = 'http://%s:%s@%s:%s/%s/' % (username, password, host, port, db_name)

startDir = os.path.dirname(os.path.realpath(__file__))

def getAllDocs():
    "Get a list of all design documents"
    request = urllib2.Request(couch_all_docs_url)
    # Encode auth credentials
    base64string = base64.b64encode('%s:%s' % (username, password))
    # Add the auth header to the request
    request.add_header("Authorization", "Basic %s" % base64string)
    # Pull list of design documents
    return json.load(urllib2.urlopen(request))['rows']

def cloneAllDocs(documents):
    "Use couchapp to clone all design documents in list"
    mkdir_p(os.path.abspath(root_dir))
    os.chdir(os.path.abspath(root_dir))
    # Clone each design document
    for doc in documents:
        call(["couchapp", "clone", couch_doc_url + doc['id']])
    os.chdir(startDir)

def beautifyJsFile(fileDir, jsFileName):
    "Beautify a JS file with JS-Beautify"
    # Open a file handler to write the output
    beautifiedJsFile = open(fileDir + '/' + jsFileName + '_tmp', 'w')
    # Beautify the JS file, write to a tmp file
    call(["js-beautify", fileDir + '/' + jsFileName], stdout=beautifiedJsFile, cwd=fileDir + '/')
    # Close the file handle
    beautifiedJsFile.close()
    # Remove the _tmp from the beautified file
    os.rename(fileDir + '/' + jsFileName + '_tmp', fileDir + '/' + jsFileName)

def fullTextJsonToJs(fileDir, jsonFileName):
    "Convert a full text JSON to a beautified JS file"
    # Load the JSON file to a var
    with open(fileDir + '/' + jsonFileName) as data_file:
        data = json.load(data_file)
    os.remove(fileDir + '/' + jsonFileName)
    # Open a tmp .js file for writing
    newJsFile = open(fileDir + '/' + jsonFileName[:-2] + '_tmp', 'w')
    # Write the JS from the JSON file
    newJsFile.write(data['index'])
    # Close the file handler
    newJsFile.close()

    # Open a file handler for the beautified output
    beautifiedNewJsFile = open(fileDir + '/' + jsonFileName[:-2], 'w')
    # Beautify the new JS file
    call(["js-beautify", fileDir + '/' + jsonFileName[:-2] + '_tmp'], stdout=beautifiedNewJsFile, cwd=fileDir + '/')
    # Close the file handle
    beautifiedNewJsFile.close()
    os.remove(fileDir + '/' + jsonFileName[:-2] + '_tmp')

def fullTextJsToJson(fileDir, jsFileName, outputPath):
    "Convert a full text JS to a compacted JSON file"
    with open(fileDir + '/' + jsFileName) as jsFile:
        jsFileContent = jsFile.read()
        minified = jsmin(jsFileContent, quote_chars="'\"`")

    with open(outputPath + '/' + jsFileName + 'on', 'w') as jsonFile:
        jsonFile.write(json.dumps({ "index": minified }))

def minifyJs(fileDir, jsFileName, outputPath):
    with open(fileDir + '/' + jsFileName, 'r+') as jsFile:
        jsFileContent = jsFile.read()
        minified = jsmin(jsFileContent, quote_chars="'\"`")

    with open(outputPath + '/' + jsFileName, 'w') as newJsFile:
        newJsFile.write(minified)
