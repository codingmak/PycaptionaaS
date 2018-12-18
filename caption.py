from flask import Flask,request,jsonify

from pycaption import *

import json


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
			return "srt"
		elif DFXPReader().detect(text):
			return "dfxp"
		elif SCCReader().detect(text):
			return "scc"

#Convert file type to outgoing file type
def converter(text_string,outgoing_format):
	
	return {
		'srt': SAMIWriter().write(SRTReader().read(text_string)),
		'dfxp': SAMIWriter().write(DFXPReader().read(caps)),
		'scc':SAMIWriter().write(SCCReader().read(caps))
	}.get(outgoing_format)()

	pass

@app.route("/test", methods=["POST"])
def user_input():

	try:
		if request.method == "POST":

			data = request.get_json()
			print("\n\nThis is the post request from user: {}\n\n".format(data))
	
			
			assetid = data['AssetID']
			incoming_format = data['InFormat'].lower()
			outgoing_format = data['OutFormat'].lower()
			text_string = data['TextString']


			if assetid and incoming_format and outgoing_format and text_string:
				# try:
				format_type = format_check(text_string)
				if format_type == incoming_format:
					print("Matched")
					converted = converter(text_string,outgoing_format)

				
				print("format_type: {}".format(format_type))
				#return jsonify({"AssetID": assetid,'InFormat': incoming_format,'TextString':text_string,'OutFormat': outgoing_format})
				#return "<h1> AssetID: {} Format: {} TextString: {}".format(assetid,outgoing_format,text_string)
				return jsonify({"AssetID": assetid,'Format': outgoing_format,'TextString':text_string})

			 
		
				# except Exception:
				# 	return "\nError with text string format type it doesnt exist\n"
		
	except (ValueError,KeyError, TypeError) as e:
		print("Failed: ", e)
 





if __name__ == '__main__':
	#print(format_check(caps))
	
	print("\n\n\n")
	app.run(debug=True)
    