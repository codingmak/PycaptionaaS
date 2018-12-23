import requests
import json

text = """1 
00:00:01,500 --> 00:00:12,345
Small caption
"""

with open('file.srt','r') as f:
	content = f.read()

content = content.split(' \n')
content = "n".join(content)

print(content)

payload = {"AssetID":"123456.123","InFormat":"srt","OutFormat":"scc","TextString":content}


r = requests.post('http://127.0.0.1:5000/', json = payload)
print(r.text)