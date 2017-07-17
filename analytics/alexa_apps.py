import json, requests

url = 'https://api.github.com/search/repositories?q=alexa+language:js'

resp = requests.get(url=url)
data = json.loads(resp.text)
result = json.dumps(data, indent=4)

print(result)
