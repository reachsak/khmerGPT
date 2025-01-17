from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
from azure.core.exceptions import HttpResponseError


key = "6e3b1be1232b4d76ae414452a6da63f0"
endpoint = "https://api.cognitive.microsofttranslator.com/"
region = "eastus"

credential = TranslatorCredential(key, region)
text_translator = TextTranslationClient(endpoint=endpoint, credential=credential)

try:
    source_language = "en"
    target_languages = ["km"]
    input_text_elements = [ InputTextItem(text = "There are two main countries called America:  1. **North America**: This continent is home to the United States of America (USA), Canada, Mexico, and several other countries. 2. **South America**: This continent is home to countries such as Brazil, Argentina, Chile, and many others.  So, it depends on which America you are referring to:  * If you mean the landmass in the western hemisphere that is commonly known as the Americas, then it is located in the **North American** continent. * If you mean the landmass in the southern hemisphere that is often referred to as South America, then it is also located in the **South American** continent.") ]

    response = text_translator.translate(content = input_text_elements, to = target_languages, from_parameter = source_language)
    translation = response[0] if response else None

    if translation:
        for translated_text in translation.translations:
            print(f"Text was translated to: '{translated_text.to}' and the result is: '{translated_text.text}'.")

except HttpResponseError as exception:
    print(f"Error Code: {exception.error.code}")
    print(f"Message: {exception.error.message}")