from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential

import os
from dotenv import load_dotenv
load_dotenv()

credential = AzureKeyCredential(os.getenv('TRANSLATOR_API_KEY'))
endpoint = os.getenv('TRANSLATOR_ENDPOINT')
translation_client = TextTranslationClient(endpoint=endpoint, credential=credential)

text = ['Wow, it is such a nice day outside']
translated_text = translation_client.translate(text, to_language=['de'])

print(translated_text)