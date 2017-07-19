#!/usr/bin/python
import sys
sys.path.insert(0, './alexa_analytics.py')

import json, requests, subprocess, alexa_analytics

num = 100
term = "alexa-app"
urlSearch = 'https://api.github.com/search/repositories?q=' + term + '+language:js&per_page=' + str(num)
# can add &sort=updated for more recent results
urlAlexaAppFormat = 'https://api.github.com/search/repositories?q=require%28%27alexa-app%27%29+in:file+language:js+repo:'

resp = requests.get(url=urlSearch)
data = json.loads(resp.text)
result = json.dumps(data, indent=4)

length = len(data['items'])

for x in range(0,length):
    name = data['items'][x]['html_url']
    dirname = "demo/" + name[19:]

    subprocess.call(['mkdir', '-p', dirname]);
    subprocess.call(['git', 'clone', name, dirname]);
    
    flag = alexa_analytics.check_alexa_app(dirname) 
    if (flag[1] > 0):
        print(flag[0])

    if (flag[1] < 1):
        subprocess.call(['rm', '-rf', dirname])

#TODO get more repositories than 30
#     process greps to perform analytics and update table
#     grep for alexa-apps, look for app.intents?
