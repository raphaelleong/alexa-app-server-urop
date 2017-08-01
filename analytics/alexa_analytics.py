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
    
def find_req_sinks(filepath):
    term = "require(\'request\')"

    varFlag = 0
    count = 0
    lines = list(skip_comments(filepath))

    for line in lines:
        temp = line.replace(" ","").replace("\"","\'").replace("\t","")
        if (varFlag < 1 and term in temp):
            var = temp.split("=")[0].replace("var","").replace("const","").replace("let","")
            varTerm  = var + "("
            varFlag = 1
            #rp(options), rp(opts), etc.

        if (varFlag > 0 and (varTerm in temp)):
            count = count + 1

    print(count)

def find_rp_sinks(filepath):
    term = "require(\'request-promise\')"

    varFlag = 0
    count = 0
    lines = list(skip_comments(filepath))

    for line in lines:
        temp = line.replace(" ","").replace("\"","\'").replace("\t","")
        if (varFlag < 1 and term in temp):
            var = temp.split("=")[0].replace("var","").replace("const","").replace("let","")
            varTerm  = var + "("
            varTerm2 = var + ".post"
            varTerm3 = var + ".get"
            varFlag = 1
            #request(options), request.post, etc.

        if (varFlag > 0 and (varTerm in temp or varTerm2 in temp or varTerm3 in temp)):
            count = count + 1

    print(count)

def find_module_file(path, module):
    term = "require(\'" + module + "\')"
    if (os.path.isdir(path)):
        os.chdir(path)
        for file in glob.glob( "*.js" ):
            try: 
                lines = list(skip_comments(file))
                for line in lines:
                    if (term in line.replace(" ","").replace("\"","\'")):
                        os.chdir("../../../")
                        res = path + " has module " + module
                        print(file)
                        return(res, file)
            except:
                continue
    os.chdir("../../../")
    res = path + " does not have module " + module
    print("-1")
    return(res, None)

#def find_destinations(path):
    # using module format of request, request-promise and http
    # find destination URI in repo
    # possibly use other module formats?

def find_slots(path):
    file = path + "/index.js"
    
    slots = "slots:{"
    res = ""
    lines = list(skip_comments(file))
    slotRes = ""
    flag = 0
    flagCustom = 0

    for line in lines:
        temp = line.replace(" ","").replace("\'","").replace("\"", "").replace("[","{").replace("]","}")
        
        if (flag > 0):
            res = res + temp
        
        if (flag < 1 and slots in temp):
            res = res + temp
            flag = 1

        if (flag > 0 and "}" in temp):
            flag = 0
            flagCustom = 1
            if ("{}" in res):
                res = ""
                continue

            resSplit = res.split("{")
            resSplit = resSplit[1].split("}")
            slotRes = slotRes + resSplit[0]
            res = ""

    slotArray = slotRes.replace("\n","").replace("\t","").split(",")
    if (flagCustom > 0):
        if (len(slotRes) == 0):
            print("0")
            return []
        print(len(slotArray))
        return slotArray

    print("-1")
    return None

    # find all occurrences of Slots : {}
    # retrieve all parts of list in { 1 , 2 , 3}

def skip_comments(filename):
    blockStart = "/*"
    blockEnd = "*/"
    flag = 0
    enc = 'utf-8'
    with open(filename, encoding=enc) as f:
        for line in f:
            if flag < 1 and blockStart in line:
                flag = 1

            if flag < 1:
                removeComment = line.split("//")
                yield removeComment[0]

            if flag > 0 and blockEnd in line:
                flag = 0

