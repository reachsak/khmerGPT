import streamlit as st
import azure.cognitiveservices.speech as speechsdk
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
from azure.core.exceptions import HttpResponseError
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Azure Speech configuration
speech_key = os.getenv("SPEECH_KEY")
speech_region = os.getenv("SPEECH_REGION")
translation_key = os.getenv("TRANSLATION_KEY")
translation_endpoint = os.getenv("TRANSLATION_ENDPOINT")
translation_region = os.getenv("TRANSLATION_REGION")
llm_api_key = os.getenv("LLM_API_KEY")

# Step 1: Record voice in Khmer
def record_voice():
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    speech_config.speech_recognition_language = "km-KH"
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print("Speak into your microphone.")
    result = speech_recognizer.recognize_once_async().get()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"Recognized: {result.text}")
        return result.text
    else:
        print("Speech not recognized. Try again.")
        return None

# Step 2: Translate Khmer text to English
def translate_to_english(khmer_text):
    credential = TranslatorCredential(translation_key, translation_region)
    text_translator = TextTranslationClient(endpoint=translation_endpoint, credential=credential)

    try:
        source_language = "km"
        target_languages = ["en"]
        input_text_elements = [InputTextItem(text=khmer_text)]

        response = text_translator.translate(content=input_text_elements, to=target_languages, from_parameter=source_language)
        translation = response[0] if response else None

        if translation:
            translated_text = translation.translations[0].text
            print(f"Translated to English: '{translated_text}'")
            return translated_text

    except HttpResponseError as exception:
        print(f"Error Code: {exception.error.code}")
        print(f"Message: {exception.error.message}")

    return None

# Step 3: Query the LLM
def query_llm(english_text):
    client = Groq(api_key=llm_api_key)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": english_text,
            }
        ],
        model="llama3-70b-8192", #llama3-8b-8192
    )
    response_text = chat_completion.choices[0].message.content
    print(f"LLM Response: {response_text}")
    return response_text

# Step 4: Translate English text to Khmer
def translate_to_khmer(english_text):
    credential = TranslatorCredential(translation_key, translation_region)
    text_translator = TextTranslationClient(endpoint=translation_endpoint, credential=credential)

    try:
        source_language = "en"
        target_languages = ["km"]
        input_text_elements = [InputTextItem(text=english_text)]

        response = text_translator.translate(content=input_text_elements, to=target_languages, from_parameter=source_language)
        translation = response[0] if response else None

        if translation:
            translated_text = translation.translations[0].text
            print(f"Translated to Khmer: '{translated_text}'")
            return translated_text

    except HttpResponseError as exception:
        print(f"Error Code: {exception.error.code}")
        print(f"Message: {exception.error.message}")

    return None

# Step 5: Convert Khmer text to speech
def text_to_speech(khmer_text):
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_config.speech_synthesis_voice_name = 'km-KH-PisethNeural'

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    speech_synthesis_result = speech_synthesizer.speak_text_async(khmer_text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized successfully.")
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print(f"Error details: {cancellation_details.error_details}")
                print("Did you set the speech resource key and region values?")

# Streamlit app
st.title("Khmer-GPT")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

input_method = st.selectbox("Input Method", ["Text", "Voice"])

if input_method == "Text":
    user_input = st.text_area("Enter your message in Khmer:")
    if st.button("Submit"):
        if user_input:
            st.session_state["messages"].append({"role": "user", "content": user_input})
else:
    if st.button("Record"):
        st.session_state["messages"].append({"role": "user", "content": record_voice()})

if st.session_state["messages"]:
    for msg in st.session_state["messages"]:
        st.write(f"{msg['role'].capitalize()}: {msg['content']}")

    if st.session_state["messages"][-1]["role"] == "user":
        last_message = st.session_state["messages"][-1]["content"]
        english_text = translate_to_english(last_message)
        if english_text:
            llm_response = query_llm(english_text)
            if llm_response:
                khmer_response = translate_to_khmer(llm_response)
                if khmer_response:
                    st.session_state["messages"].append({"role": "assistant", "content": khmer_response})
                    text_to_speech(khmer_response)
                    st.write(f"Assistant: {khmer_response}")

if st.button("Clear Chat"):
    st.session_state["messages"] = []
#streamlit run app.py