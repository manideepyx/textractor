import requests
import time
# If you are using a Jupyter notebook, uncomment the following line.
#%matplotlib inline
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from PIL import Image
from io import BytesIO

# Replace <Subscription Key> with your valid subscription key.
subscription_key = "72b3f37662064fb1afe2f008e12e5200"
assert subscription_key

# You must use the same region in your REST call as you used to get your
# subscription keys. For example, if you got your subscription keys from
# westus, replace "westcentralus" in the URI below with "westus".
#
# Free trial subscription keys are generated in the "westus" region.
# If you use a free trial subscription key, you shouldn't need to change
# this region.
vision_base_url = "https://centralindia.api.cognitive.microsoft.com/vision/v2.0/"

text_recognition_url = vision_base_url + "recognizeText"

# # uncomment this if you want it to be Handwritten always
# mode = 'Handwritten'

# # Set image_url to the URL of an image that you want to analyze.
# image_url = "https://i.ytimg.com/vi/Mh9-NlRGA7g/maxresdefault.jpg"

def textrecog(image_url, mode):
	"""
		Recognises the text by passing through Azure Computer Vision
	"""

	headers = {'Ocp-Apim-Subscription-Key': subscription_key}
	# Note: The request parameter changed for APIv2.
	# For APIv1, it is 'handwriting': 'true'.
	params  = {'mode': mode}
	data    = {'url': image_url}
	response = requests.post(
	    text_recognition_url, headers=headers, params=params, json=data)
	response.raise_for_status()

	# Extracting handwritten text requires two API calls: One call to submit the
	# image for processing, the other to retrieve the text found in the image.

	# Holds the URI used to retrieve the recognized text.
	operation_url = response.headers["Operation-Location"]

	# The recognized text isn't immediately available, so poll to wait for completion.
	analysis = {}
	poll = True
	while (poll):
	    response_final = requests.get(
	        operation_url, headers=headers)
	    analysis = response_final.json()
	    time.sleep(1)
	    if ("recognitionResult" in analysis):
	        poll= False 
	    if ("status" in analysis and analysis['status'] == 'Failed'):
	        poll= False

	polygons=[]
	if ("recognitionResult" in analysis):
	    # Extract the recognized text, with bounding boxes.
	    polygons = [(line["boundingBox"], line["text"])
	        for line in analysis["recognitionResult"]["lines"]]

	# generate the text
	text_string = ""
	for polygon in polygons:
	    text = polygon[1]
	    text_string += text + '\n'

	return text_string 