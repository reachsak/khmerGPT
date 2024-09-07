import azure.cognitiveservices.speech as speechsdk

def from_mic():
    speech_config = speechsdk.SpeechConfig(subscription="5630d19384fc422f88c86b91e2354aee", region="eastus")
    speech_config.speech_recognition_language="km-KH"
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    

    print("Speak into your microphone.")
    result = speech_recognizer.recognize_once_async().get()
    print(result.text)

from_mic()