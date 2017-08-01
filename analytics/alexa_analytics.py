#!/usr/bin/python

import subprocess, os, glob, string

def check_alexa_app(path):
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

def find_intents(path):
    file = path + "/index.js"
    
    alexa = "require(\'alexa-app\')"
    app = ""
    flag = 0

    lines = list(skip_comments(file))

    for line in lines:
        if (flag < 1 and alexa in line.replace(" ","")):
            lineSplit = line.split(" ")
            alexaApp = lineSplit[1] + ".app"
            flag = 1
        
        if (flag > 0 and alexaApp in line.replace(" ","")):
            lineSplit = line.split(" ")
            app = lineSplit[1]

    count=0
    term = app + ".intent"

    for line in lines:
        if term in line:
            count = count + 1
    print(count)
    return count 

#def find_destinations(path):

#def find_slots(path):

def find_module_sinks(path):
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

def skip_comments(filename):
    blockStart = "/*"
    blockEnd = "*/"
    flag = 0
    with open(filename) as f:
        for line in f:
            if flag < 1 and blockStart in line:
                flag = 1

            if flag < 1:
                removeComment = line.split("//")
                yield removeComment[0]

            if flag > 0 and blockEnd in line:
                flag = 0

