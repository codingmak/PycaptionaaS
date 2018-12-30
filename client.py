import requests
import json

text = """1 
00:00:01,500 --> 00:00:12,345
Small caption
"""

pattern = "!@#$%"
try:
	with open(input("Enter file: "),'r') as f:
		content = f.read()
	content = content.split(' \n')
	if pattern not in content:
		content = pattern.join(content)
	print("Change pattern")
	#dfxp or scc
	payload = {"AssetID":"123456.123","InFormat":"srt","OutFormat":"scc","TextString":content}


	r = requests.post('http://127.0.0.1:5000/', json = payload)
	print(r.text)
except IOError as e:
	print("File name does not exist: ",e)

	