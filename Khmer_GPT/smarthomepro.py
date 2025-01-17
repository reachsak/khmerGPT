import streamlit as st
import azure.cognitiveservices.speech as speechsdk
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
from azure.core.exceptions import HttpResponseError
from llama_cpp import Llama
from typing import Union
from web3 import Web3
from llama_cpp_agent.llm_agent import LlamaCppAgent
from llama_cpp_agent.providers.llama_cpp_endpoint_provider import LlamaCppEndpointSettings
from llama_cpp_agent.messages_formatter import MessagesFormatterType
from llama_cpp_agent.function_calling import LlamaCppFunctionTool
from llama_cpp_agent.gbnf_grammar_generator.gbnf_grammar_from_pydantic_models import create_dynamic_model_from_function
from yeelight import Bulb

# Function to record voice in Khmer
def from_mic() -> str:
    speech_config = speechsdk.SpeechConfig(subscription="5630d19384fc422f88c86b91e2354aee", region="eastus")
    speech_config.speech_recognition_language = "km-KH"
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    st.write("Speak into your microphone.")
    result = speech_recognizer.recognize_once_async().get()
    return result.text

# Function to translate text
def translate_text(text: str, source_language: str, target_language: str) -> str:
    key = "6e3b1be1232b4d76ae414452a6da63f0"
    endpoint = "https://api.cognitive.microsofttranslator.com/"
    region = "eastus"
    credential = TranslatorCredential(key, region)
    text_translator = TextTranslationClient(endpoint=endpoint, credential=credential)
    
    try:
        input_text_elements = [InputTextItem(text=text)]
        response = text_translator.translate(content=input_text_elements, to=[target_language], from_parameter=source_language)
        translation = response[0] if response else None

        if translation:
            for translated_text in translation.translations:
                return translated_text.text
    except HttpResponseError as exception:
        st.error(f"Error Code: {exception.error.code}")
        st.error(f"Message: {exception.error.message}")
    return ""

# Function to synthesize speech in Khmer
def text_to_speech_khmer(text: str):
    speech_config = speechsdk.SpeechConfig(subscription="5630d19384fc422f88c86b91e2354aee", region="eastus")
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_config.speech_synthesis_voice_name='km-KH-PisethNeural'
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        st.write("Speech synthesized successfully.")
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        st.error("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error and cancellation_details.error_details:
            st.error("Error details: {}".format(cancellation_details.error_details))
            st.error("Did you set the speech resource key and region values?")

# Functions to control the Yeelight bulb
def set_brightness_to_10(inner_thoughts: str, command: str) -> str:
    bulb_ip = "192.168.31.171"
    bulb = Bulb(bulb_ip)
    bulb.set_brightness(10)
    return f"{inner_thoughts} Brightness set to 10%."

def set_brightness_to_20(inner_thoughts: str, command: str) -> str:
    bulb_ip = "192.168.31.171"
    bulb = Bulb(bulb_ip)
    bulb.set_brightness(20)
    return f"{inner_thoughts} Brightness set to 20%."

def set_brightness_to_30(inner_thoughts: str, command: str) -> str:
    bulb_ip = "192.168.31.171"
    bulb = Bulb(bulb_ip)
    bulb.set_brightness(30)
    return f"{inner_thoughts} Brightness set to 30%."

def set_brightness_to_40(inner_thoughts: str, command: str) -> str:
    bulb_ip = "192.168.31.171"
    bulb = Bulb(bulb_ip)
    bulb.set_brightness(40)
    return f"{inner_thoughts} Brightness set to 40%."

def turn_on_light(inner_thoughts: str, command: str) -> str:
    """
    Control the Yeelight bulb.

    Parameters:
        inner_thoughts (str): Inner thoughts to return alongside the action.
        command (str): The command to execute "turn on" .
        
    Returns:
        str: A message indicating the action taken.
    """
    bulb_ip = "192.168.31.171"  # IP address of the Yeelight bulb
    bulb = Bulb(bulb_ip)
    bulb.turn_on()
    return f"{inner_thoughts} Light turned on."
    
  

def turn_off_light(inner_thoughts: str, command: str) -> str:
    """
    Control the Yeelight bulb.

    Parameters:
        inner_thoughts (str): Inner thoughts to return alongside the action.
        command (str): The command to execute,  "turn off".
        
    Returns:
        str: A message indicating the action taken.
    """
    bulb_ip = "192.168.31.171"  # IP address of the Yeelight bulb
    bulb = Bulb(bulb_ip)

    bulb.turn_off()
    return f"{inner_thoughts} Light turned off."

DynamicSampleModel3 = create_dynamic_model_from_function(turn_off_light, "turn off")
DynamicSampleModel4 = create_dynamic_model_from_function(turn_on_light, "turn on")
function_tools = [LlamaCppFunctionTool(DynamicSampleModel3), LlamaCppFunctionTool(DynamicSampleModel4)]

function_tool_registry = LlamaCppAgent.get_function_tool_registry(function_tools)

main_model = LlamaCppEndpointSettings(
    completions_endpoint_url="http://127.0.0.1:8080/completion"
)

system_prompt = "Welcome to the smart home assistant. You can ask to turn on or turn off the light.\n"

llama_cpp_agent = LlamaCppAgent(main_model, debug_output=True,
                                system_prompt=system_prompt + function_tool_registry.get_documentation(),
                                predefined_messages_formatter_type=MessagesFormatterType.CHATML)

def main():
    st.title("Smart Home Assistant")
    
    if st.button("Record Voice in Khmer"):
        khmer_text = from_mic()
        st.write(f"Recognized Khmer text: {khmer_text}")
        english_text = translate_text(khmer_text, "km", "en")
        st.write(f"Translated to English: {english_text}")

        if english_text:
            user_input = english_text
            response = llama_cpp_agent.get_chat_response(user_input, temperature=0.45, function_tool_registry=function_tool_registry)
            st.write(f"AI Response: {response}")

            # Extract inner_thoughts and translate back to Khmer
            if isinstance(response, list):
                for res in response:
                    inner_thoughts = res.get("arguments", {}).get("inner_thoughts", "")
                    if inner_thoughts:
                        khmer_thoughts = translate_text(inner_thoughts, "en", "km")
                        st.write(f"Translated inner thoughts to Khmer: {khmer_thoughts}")
                        # Synthesize the translated text to speech in Khmer
                        text_to_speech_khmer(khmer_thoughts)
            else:
                inner_thoughts = response.get("arguments", {}).get("inner_thoughts", "")
                if inner_thoughts:
                    khmer_thoughts = translate_text(inner_thoughts, "en", "km")
                    st.write(f"Translated inner thoughts to Khmer: {khmer_thoughts}")
                    # Synthesize the translated text to speech in Khmer
                    text_to_speech_khmer(khmer_thoughts)

if __name__ == "__main__":
    main()
