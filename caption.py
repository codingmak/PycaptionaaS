from flask import Flask,request,jsonify

from pycaption import detect_format,SRTReader,DFXPReader, SCCReader,SAMIWriter,CaptionConverter,DFXPWriter,SCCWriter,SRTWriter

import logging

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

logger = logging.getLogger(__name__)

logging.basicConfig(filename='output.log',level=logging.INFO, format='%(asctime)s:%(name)s:%(message)s')


app = Flask(__name__)

formats = ['scc','srt','scc']

#Detects format
def format_check(text_string):

    reader = detect_format(text_string)

    if reader:
        if SRTReader().detect(text_string):
            return "srt"
        elif DFXPReader().detect(text_string):
            return "dfxp"
        elif SCCReader().detect(text_string):
            return "scc"
        else:
        	return None

def detect_reader(text_string):

	format_type = format_check(text_string)

	if format_type == 'srt':
		return SRTReader()
	elif format_type == 'dfxp':
		return DFXPReader()
	elif format_type == 'scc':
		return SCCReader()
	else:
		return None
	

#Convert file type to the format specified file type
def convert(text_string,outgoing_format):

	converter = CaptionConverter()
	formatted = detect_reader(text_string)
	converter.read(text_string, formatted)

	if outgoing_format == 'srt':
		return converter.write(SRTWriter())	
	elif outgoing_format == 'dfxp':
		return converter.write(DFXPWriter())
	elif outgoing_format == 'scc':
		return converter.write(SCCWriter())
	else:
		return None



@app.route("/", methods=["POST"])
def user_input():

	try:
		if request.method == "POST":

			data = request.get_json()
			
			logging.info("\n\nPOST request from {}: {}\n\n".format(request.remote_addr,data))
			
			pattern = "!@#$%"

			try:
				assetid = data['AssetID']
				incoming_format = data['InFormat'].lower()
				outgoing_format = data['OutFormat'].lower()
				
				text_string = data['TextString'].split(pattern)
				
				text_string = "\n".join(text_string)
				#############################################################################
			except (ValueError,KeyError):
				return jsonify({"response":"Missing data"}) 

	
		
			if len(str(assetid)) == 10 and "." in assetid[6] and incoming_format in formats:

				
				format_type = format_check(text_string)
				
				logger.info("format_type: {}".format(format_type))
			#do checks to make sure incoming_format and outgoing format is of three types srt,dfxp or scc					

				
				if format_type == incoming_format:
				
					converted = convert(text_string,outgoing_format)
				

					return jsonify({"AssetID": assetid,'Format': outgoing_format,'TextString':converted})
		
	except:
		return jsonify({"response":"Failed request"})
 





if __name__ == '__main__':
	
	
	print("\n\n\n")
	app.run(debug=True)