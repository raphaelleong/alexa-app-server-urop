#!/usr/bin/python

import json, requests, git, subprocess

url = 'https://api.github.com/search/repositories?q=alexa+language:js'

resp = requests.get(url=url)
data = json.loads(resp.text)
result = json.dumps(data, indent=4)

length = len(data['items']);

for x in range(0,length):
    name = data['items'][x]['html_url']
    dirname = "demo/" + name[19:]
    print(dirname)
    subprocess.call(['mkdir', '-p', dirname]);
    #subprocess.call(['git', 'clone', name, dirname]);


#TODO get more repositories than 30
#     process greps to perform analytics and update table
