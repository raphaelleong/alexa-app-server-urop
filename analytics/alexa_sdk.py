#!/usr/bin/python
import sys, time

sys.path.insert(0, './alexa_analytics.py')

import json, requests, subprocess, alexa_analytics
import datetime as dt
import calendar as cs

num = 100
term = "alexa"
app_urls=[]
count = 0
dateCurrent = dt.date.today()

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = int(sourcedate.year + month / 12 )
    month = month % 12 + 1
    day = min(sourcedate.day, cs.monthrange(year,month)[1])
    return dt.date(year,month,day)

def extractor(data):
    for x in data:
        yield x['html_url']

def check_rate_limit():
    rate_url = "https://api.github.com/rate_limit"
    resp = requests.get(url=rate_url)
    data = json.loads(resp.text)

    rate_limit = data['resources']['search']['remaining']

    #print("Rate_limit: " + str(rate_limit) + "\n", end='', flush=True)
    if (rate_limit <= 0):
        print("Resetting X-RateLimit...\n", end='', flush=True)
        time.sleep(120)

endSearch = dt.date(2015, 1, 1)
while (dateCurrent > endSearch):
    datePrev = add_months(dateCurrent, -1)
    dateRange = datePrev.strftime("%Y-%m-%d") + ".." + dateCurrent.strftime("%Y-%m-%d")
    print("Extracting from dates: " + dateRange + "\n", end='', flush=True)

    #1000 results max, rerun search w (10, 20), (20, 30), etc.
    for page in range(0, 10):
        check_rate_limit()
        
        urlSearch = 'https://api.github.com/search/repositories?q=' + term + '+language:js+created:' + dateRange + '&per_page=' + str(num) + '&page=' + str(page)
        # can add &sort=updated for more recent results

        resp = requests.get(url=urlSearch)
        data = json.loads(resp.text)
        
        #result = json.dumps(data, indent=2)
        #print(result+ "\n", end='', flush=True)

        if 'items' in data:
            extracted = list(extractor(data['items']))
            length = len(extracted)
            if length <= 0:
                break
            app_urls = app_urls + extracted
            print("page " + str(page) + " extracted " + str(length) + ".\n", end='', flush=True)
        else:
            break
    

    dateCurrent = datePrev

length = len(app_urls)
print("Collected " + str(length) + " URLs.\n", end='', flush=True)
comp = 0

for name in app_urls:
    comp = comp + 1

    dirname = "demo-sdk/" + name[19:]

    subprocess.call(['mkdir', '-p', dirname]);
    subprocess.call(['git', 'clone', name, dirname]);

    flag = alexa_analytics.check_alexa_sdk(dirname)
    if (flag[1] > 0):
        #print(flag[0])
        count=count+1

    if (flag[1] < 1):
        subprocess.call(['rm', '-rf', dirname])

    print("Collected " + str(count) + " repos.\n", end='', flush=True)
    print("Completed: " + str(comp) + " out of " + str(length) + "\n", end='', flush=True)

print("Collected " + str(count) + " repos.\n", end='', flush=True)
print("Done.\n", end='', flush=True)
