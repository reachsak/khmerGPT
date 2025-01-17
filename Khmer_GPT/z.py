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
    speech_config = speechsdk.SpeechConfig(subscription="8daf8bda21e54a438ceb9be7f055577a", region="eastus")
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
    """
    Set the brightness of the Yeelight bulb to 10%.

    Parameters:
        inner_thoughts (str): Inner thoughts to return alongside the action.
        command (str): The command to execute, "set brightness to 10".

    Returns:
        str: A message indicating the action taken.
    """
    bulb_ip = "192.168.31.171"  # IP address of the Yeelight bulb
    bulb = Bulb(bulb_ip)
    bulb.set_brightness(10)
    return f"{inner_thoughts} Brightness set to 10%."

def set_brightness_to_50(inner_thoughts: str, command: str) -> str:
    """
    Set the brightness of the Yeelight bulb to 50%.

    Parameters:
        inner_thoughts (str): Inner thoughts to return alongside the action.
        command (str): The command to execute, "set brightness to 50".

    Returns:
        str: A message indicating the action taken.
    """
    bulb_ip = "192.168.31.171"  # IP address of the Yeelight bulb
    bulb = Bulb(bulb_ip)
    bulb.set_brightness(50)
    return f"{inner_thoughts} Brightness set to 50%."

def set_brightness_to_90(inner_thoughts: str, command: str) -> str:
    """
    Set the brightness of the Yeelight bulb to 90%.

    Parameters:
        inner_thoughts (str): Inner thoughts to return alongside the action.
        command (str): The command to execute, "set brightness to 90".

    Returns:
        str: A message indicating the action taken.
    """
    bulb_ip = "192.168.31.171"  # IP address of the Yeelight bulb
    bulb = Bulb(bulb_ip)
    bulb.set_brightness(90)
    return f"{inner_thoughts} Brightness set to 90%."

def set_brightness_to_percentage(inner_thoughts: str, command: str) -> str:
    """
    Set the brightness of the Yeelight bulb to 90%.

    Parameters:
        inner_thoughts (str): Inner thoughts to return alongside the action.
        command (str): The command to execute, "set brightness to 90".

    Returns:
        str: A message indicating the action taken.
    """
    bulb_ip = "192.168.31.171"  # IP address of the Yeelight bulb
    bulb = Bulb(bulb_ip)
    bulb.set_brightness(90)
    return f"{inner_thoughts} Brightness set to 90%."


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
def introduce_yourself(inner_thoughts: str, command: str) -> str:
    """
    Introduce the AI assistant.

    Parameters:
        inner_thoughts (str): Inner thoughts to return alongside the introduction.
        command (str): The command to execute, "introduce yourself".

    Returns:
        str: A message introducing the AI assistant.
    """
 
    return f"{inner_thoughts} "
DynamicSampleModel0 = create_dynamic_model_from_function(introduce_yourself, "introduce yourself")
DynamicSampleModel3 = create_dynamic_model_from_function(turn_off_light, "turn off")
DynamicSampleModel4 = create_dynamic_model_from_function(turn_on_light, "turn on")
DynamicSampleModel1 = create_dynamic_model_from_function(set_brightness_to_10, "lower down the brightness to 10%")
DynamicSampleModel5 = create_dynamic_model_from_function(set_brightness_to_50, "set the brightness to 50%")
DynamicSampleModel9 = create_dynamic_model_from_function(set_brightness_to_90, "increase the brightness to 90%")

function_tools = [LlamaCppFunctionTool(DynamicSampleModel3), LlamaCppFunctionTool(DynamicSampleModel4), LlamaCppFunctionTool(DynamicSampleModel1), LlamaCppFunctionTool(DynamicSampleModel5), LlamaCppFunctionTool(DynamicSampleModel9), LlamaCppFunctionTool(DynamicSampleModel0)]

function_tool_registry = LlamaCppAgent.get_function_tool_registry(function_tools)

main_model = LlamaCppEndpointSettings(
    completions_endpoint_url="http://127.0.0.1:8080/completion"
)

system_prompt = "You are a helpful, smart, kind, and efficient smart home AI assistant. You always fulfill the user's requests to the best of your ability.If you don't get any specific command, You will also try to understand what they are feeling and see what you could do to control the house system to fit their need.\n"

llama_cpp_agent = LlamaCppAgent(main_model, debug_output=True,
                                system_prompt=system_prompt + function_tool_registry.get_documentation(),
                                predefined_messages_formatter_type=MessagesFormatterType.CHATML)

def main():
    st.title("🇰🇭Smart Home Assistant")
    
    if st.button("Record Voice in Khmer"):
        khmer_text = from_mic()
        st.write(f"Recognized Khmer text: {khmer_text}")
        english_text = translate_text(khmer_text, "km", "en")
        st.write(f"Translated to English: {english_text}")

        if english_text:
            user_input = english_text
            response = llama_cpp_agent.get_chat_response(user_input, temperature=0.45, function_tool_registry=function_tool_registry)
            st.write(f"AI Response: {response}")

            # Extract return_value and translate back to Khmer
            return_value = ""
            if isinstance(response, list):
                for res in response:
                    return_value = res.get("return_value", "")
                    if return_value:
                        break
            else:
                return_value = response.get("return_value", "")

            st.write(f"Extracted return value: {return_value}")
            if return_value:
                khmer_return_value = translate_text(return_value, "en", "km")
                st.write(f"Translated return value to Khmer: {khmer_return_value}")
                # Synthesize the translated text to speech in Khmer
                text_to_speech_khmer(khmer_return_value)
            else:
                st.write("No return value found in the AI response.")

if __name__ == "__main__":
    main()

#streamlit run z.py