from pycaption import *
#test string
# caps = '''1
# 00:00:09,209 --> 00:00:12,312
# This is an example SRT file,
# which, while extremely short,
# is still a valid SRT file.
# '''

caps = '''1
00:00:01,500 --> 00:00:12,345
Small caption'''

# converter = CaptionConverter()
# converter.read(srt_caps, SRTReader())
# print (converter.write(SAMIWriter()))
# print (converter.write(DFXPWriter()))
# print (converter.write(pycaption.transcript.TranscriptWriter()))


# #This will take the input json parse it and find the Format key.  
# #Takes the value and depending on format uses pycaption to convert
def format_check(text):



	reader = detect_format(text)
	if reader:
		if SRTReader().detect(text):
			return "SRT"
		elif DFXPReader().detect(text):
			return "DFXP"
		elif SCCReader().detect(text):
			return "SCC"


if __name__ == '__main__':
	print(format_check(caps))