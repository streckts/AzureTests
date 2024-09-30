from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

import os
from dotenv import load_dotenv
load_dotenv()

credential = AzureKeyCredential(os.getenv('VISION_API_KEY'))
endpoint = os.getenv('VISION_ENDPOINT')

image_url = 'https://lh5.googleusercontent.com/-L9vuCkuwhsE/ToByBD601uI/AAAAAAAAFf0/3UKAHX0PXO4/s640/Bruins_StanleyCup_Engrave.jpg'

vision_client = ImageAnalysisClient(
    credential=credential,
    endpoint=endpoint
    )

result = vision_client.analyze_from_url(
    image_url=image_url,
    visual_features=[VisualFeatures.READ]
    )

print('Results:')
if result.read is not None:
    for line in result.read.blocks[0].lines:
        print(f"    Line: '{line.text}', Bounding Box {line.bounding_polygon}")
        for word in line.words:
            print(word.text)