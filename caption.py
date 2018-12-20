from flask import Flask,request,jsonify

from pycaption import detect_format, SRTReader, DFXPReader, SCCReader,SAMIWriter


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

caps = '''1
00:00:01,500 --> 00:00:12,345
Small caption'''

list_of_formats = ["srt","dfxp","scc"]

#Detects format
def format_check(text):
    reader = detect_format(text)
    if reader:
        if SRTReader().detect(text):
            return "srt"
        elif DFXPReader().detect(text):
            return "dfxp"
        elif SCCReader().detect(text):
            return "scc"

#Convert file type to the format specified file type
def converter(text_string,outgoing_format):
	
	return {
		'srt': SAMIWriter().write(SRTReader().read(text_string)),
		'dfxp': SAMIWriter().write(DFXPReader().read(text_string)),
		'scc':SAMIWriter().write(SCCReader().read(text_string))
	}.get(outgoing_format)()

	

@app.route("/", methods=["POST"])
def user_input():

	try:
		if request.method == "POST":

			data = request.get_json()
			print("\n\nThis is the post request coming from {}: {}\n\n".format(request.environ['REMOTE_ADDR'],data))
	
			try:
				assetid = data['AssetID']
				incoming_format = data['InFormat'].lower()
				outgoing_format = data['OutFormat'].lower()
				text_string = data['TextString']
			except (ValueError,KeyError):
				return jsonify({"response":"Missing data"}) 



			if assetid and incoming_format and outgoing_format and text_string:
				print("{} asset id".format(assetid))
				# make sure that the format is the same
				if len(str(assetid)) == 10 and "." in assetid[6]:

					format_type = format_check(text_string)
					print("format_type: {}".format(format_type))
					#do checks to make sure incoming_format and outgoing format is of three types srt,dfxp or scc
					if format_type == incoming_format:
						if outgoing_format in list_of_formats:
							converted = converter(text_string,outgoing_format)
							print("Converted: {} in {}".format(converted,outgoing_format))
							return jsonify({"AssetID": assetid,'Format': outgoing_format,'TextString':text_string})
							
						else:
							return jsonify({"response":"Outgoing format is not supported or does not exist"})

				
				#Need to nest this in 4th if statement
				return jsonify({"AssetID": assetid,'Format': outgoing_format,'TextString':text_string})

		
		
				# except Exception:
				# 	return "\nError with text string format type it doesnt exist\n"
		
	except:
		return jsonify({"response":"Failed Request"})
 





if __name__ == '__main__':
	
	
	print("\n\n\n")
	app.run(debug=True)