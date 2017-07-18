#!/usr/bin/python

import subprocess, os.path

def check_alexa_app(path):
    indexFile = path + "/index.js"
    if (os.path.isfile(indexFile)):
        if 'require(\'alexa-app\')' in open(indexFile).read():
            return (path + ": is an alexa-app", 1)

    indexFile = path + "/src/index.js"
    if (os.path.isfile(indexFile)):
        if 'require(\'alexa-app\')' in open(indexFile).read():
            return (path + ": is an alexa-app", 1)
    return (path + ": not an alexa-app", 0)
   

def intent_analytics(repo):
    subprocess.call(['./analyse.sh'])

