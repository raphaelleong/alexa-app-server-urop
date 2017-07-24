#!/usr/bin/python
import sys, time

sys.path.insert(0, './alexa_analytics.py')

import json, requests, subprocess, alexa_analytics

num = 100
term = "alexa"
app_urls=[]
count = 0

def extractor(data):
    for x in data:
        yield x['html_url']

def check_rate_limit():
    rate_url = "https://api.github.com/rate_limit"
    resp = requests.get(url=rate_url)
    data = json.loads(resp.text)

    rate_limit = data['resources']['search']['remaining']

    if (rate_limit <= 0):
        print("Resetting X-RateLimit...\n", end=' ', flush=True)
        time.sleep(300)

for page in range(0, 50):
    check_rate_limit()
    urlSearch = 'https://api.github.com/search/repositories?q=' + term + '+language:js&per_page=' + str(num) + '&page=' + str(page)
    # can add &sort=updated for more recent results

    resp = requests.get(url=urlSearch)
    data = json.loads(resp.text)
    
    if 'items' in data:
        extracted = list(extractor(data['items']))
        length = len(extracted)
        if length <= 0:
            break
        app_urls = app_urls + extracted
        print("Page " + str(page) + " Extracted " + str(length) + ".\n", end=' ', flush=True)
    else:
        break

length = len(app_urls)
print("Collected " + str(length) + " URLs.\n", end=' ', flush=True)

for name in app_urls:
    dirname = "demo/" + name[19:]

    subprocess.call(['mkdir', '-p', dirname]);
    subprocess.call(['git', 'clone', name, dirname]);

    flag = alexa_analytics.check_alexa_app(dirname)
    if (flag[1] > 0):
        #print(flag[0])
        count=count+1

    if (flag[1] < 1):
        subprocess.call(['rm', '-rf', dirname])

subprocess.call(['./clean_dir.sh'])
print("Collected " + str(count) + " repos.\n", end=' ', flush=True)
print("Done.\n", end=' ', flush=True)
