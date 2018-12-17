from flask import Flask,request,jsonify

from pycaption import *

import json
from colorama import Fore

app = Flask(__name__)


'''
RESTful API
Use https://github.com/a-wakeel/flask-bp as a base
Flask (Python) for the framework
JSON payload for the POST request
AssetID = Property.Ep
TextString = .SCC file with line breaks
InFormat = what you are sending
OutFormat = what you want back


POST returns JSON
‘AssetID’ = 123456.001 (AssetID),
‘Format’ = string for what the format
‘TextString’ = converted closed captions
'''


#test string
caps = '''100:00:01,500 --> 00:00:12,345 Small caption'''


# #This will take the input json parse it and find the Format key.  
# #Takes the value and depending on format uses pycaption to convert
def format_check(text):

	reader = detect_format(text)
	if reader:
		if SRTReader().detect(text):
			return SAMIWriter().write(SRTReader().read(text))
		elif DFXPReader().detect(text):
			return SAMIWriter().write(DFXPReader().read(text))
		elif SCCReader().detect(text):
			return SAMIWriter().write(SCCReader().read(text))



@app.route("/test", methods=["POST","GET"])
def user_input():

	try:
		if request.method == "POST":

			data = request.get_json()
			print("\n\nThis is the post request from user: {}\n\n".format(data))
	
			global assetid,incoming_format,outgoing_format,text_string
			assetid = data['AssetID']
			incoming_format = data['InFormat']
			outgoing_format = data['OutFormat']
			text_string = data['TextString']

			if assetid and incoming_format and outgoing_format and text_string:

				print("This is the text_string {}".format(text_string))
				
				#return jsonify({"AssetID": assetid,'InFormat': incoming_format,'TextString':text_string,'OutFormat': outgoing_format})
				return jsonify({"AssetID": assetid,'Format': outgoing_format,'TextString':text_string})
		return "<h1> AssetID: {} Format: {} TextString: {}".format(assetid,outgoing_format,text_string)
		
	except (ValueError,KeyError, TypeError) as e:
		print("Failed ",e)
 

# # #view the file that is converted and parse the json file to output to view.	
# # @app.route("/view",methods=["GET"])
# # def view_converted():
# # 	assetid = request.form['AssetID']
# # 	formatted = request.form['Format']
# # 	text_string = request.form['TextString'] 



# 	return '<h1>AssetID: {} Formatted: {} TextString: {}</h1>'.format(assetid,formatted,text_string)





if __name__ == '__main__':
	#print(format_check(caps))
	
	print("\n\n\n")
	app.run(debug=True)
    