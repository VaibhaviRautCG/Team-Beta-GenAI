from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import os
# from azure.cognitiveservices.vision.computervision.models import ComputerVisionErrorException
from io import BytesIO

subscription_key = os.environ["VISION_KEY"]
endpoint = os.environ["VISION_ENDPOINT"]

credentials = CognitiveServicesCredentials(subscription_key)
computervision_client = ComputerVisionClient(endpoint, credentials)

def extract_text_from_image(file):
    # Extract recognized text from the results
    recognized_text = ''
    try:
        image_data = file.read()
        # headers = {'Content-Type': 'application/octet-stream'}
        # results = computervision_client.read(img_data) #, headers=headers)
        result = computervision_client.read_in_stream(BytesIO(image_data), raw=True)
        for region in result.regions:
            for line in region.lines:
                for word in line.words:
                    recognized_text += word.text + ' '
        print("\nTEST: recognized_text: ", recognized_text)
        return recognized_text.strip()
    except Exception as e:
        print(f"Computer Vision API Error: {e}")
        print(f"Response Content: {e.response.content}")
        return str(e)

    