#!/usr/bin/python

import subprocess, os, glob

def check_alexa_app(path):
   # indexFile = path + "/index.js"
   # if (os.path.isfile(indexFile)):
   #     if 'require(\'alexa-app\')' in open(indexFile, encoding="utf8").read():
   #         return (path + ": is an alexa-app", 1)

   # indexFile = path + "/src/index.js"
   # if (os.path.isfile(indexFile)):
   #     if 'require(\'alexa-app\')' in open(indexFile, encoding="utf8").read():
   #         return (path + ": is an alexa-app", 1)
   # return (path + ": not an alexa-app", 0)
   #
    term = "require(\'alexa-app\')"
    if (os.path.isdir(path)):

        os.chdir(path)
        for file in glob.glob( "*.js" ):
                try: 
                    f = open(file)
                    contents = f.read()
                    if term in contents:
                        os.chdir("../../../")
                        return(path + ": is an alexa-app", 1)
                except: 
                    contents = ""
                    print("Could not print file: " + file + "\n", end=' ', flush=True)
        os.chdir("../../../")
    return(path + ": is not an alexa-app", 0)

def check_alexa_sdk(path):
   # indexFile = path + "/index.js"
   # if (os.path.isfile(indexFile)):
   #     if 'require(\'alexa-app\')' in open(indexFile, encoding="utf8").read():
   #         return (path + ": is an alexa-app", 1)

   # indexFile = path + "/src/index.js"
   # if (os.path.isfile(indexFile)):
   #     if 'require(\'alexa-app\')' in open(indexFile, encoding="utf8").read():
   #         return (path + ": is an alexa-app", 1)
   # return (path + ": not an alexa-app", 0)
   #
    term = "require(\'alexa-sdk\')"
    if (os.path.isdir(path)):

        os.chdir(path)
        for file in glob.glob( "*.js" ):
                try: 
                    f = open(file)
                    contents = f.read()
                    if term in contents:
                        os.chdir("../../../")
                        return(path + ": is an alexa-sdk", 1)
                except: 
                    contents = ""
                    print("Could not print file: " + file + "\n", end=' ', flush=True)
        os.chdir("../../../")
    return(path + ": is not an alexa-sdk", 0)

def intent_analytics(repo):
    subprocess.call(['./analyse.sh'])

