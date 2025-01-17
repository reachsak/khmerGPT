import azure.cognitiveservices.speech as speechsdk
from llama_cpp import Llama
from typing import Union
import requests
from web3 import Web3
from llama_cpp_agent.llm_agent import LlamaCppAgent
from llama_cpp_agent.providers.llama_cpp_endpoint_provider import LlamaCppEndpointSettings
from llama_cpp_agent.messages_formatter import MessagesFormatterType
from llama_cpp_agent.function_calling import LlamaCppFunctionTool
from llama_cpp_agent.gbnf_grammar_generator.gbnf_grammar_from_pydantic_models import create_dynamic_model_from_function
from yeelight import Bulb
from groq import Groq

# Function to transcribe speech from the microphone
def from_mic():
    speech_config = speechsdk.SpeechConfig(subscription="8daf8bda21e54a438ceb9be7f055577a", region="eastus")
    speech_config.speech_recognition_language="km-KH"
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    
    print("Speak into your microphone.")
    result = speech_recognizer.recognize_once_async().get()
    return result.text

# Functions to control Yeelight bulb
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

def set_brightness_to_20(inner_thoughts: str, command: str) -> str:
    """
    Set the brightness of the Yeelight bulb to 20%.

    Parameters:
        inner_thoughts (str): Inner thoughts to return alongside the action.
        command (str): The command to execute, "set brightness to 20".

    Returns:
        str: A message indicating the action taken.
    """
    bulb_ip = "192.168.31.171"  # IP address of the Yeelight bulb
    bulb = Bulb(bulb_ip)
    bulb.set_brightness(20)
    return f"{inner_thoughts} Brightness set to 20%."

def set_brightness_to_30(inner_thoughts: str, command: str) -> str:
    """
    Set the brightness of the Yeelight bulb to 30%.

    Parameters:
        inner_thoughts (str): Inner thoughts to return alongside the action.
        command (str): The command to execute, "set brightness to 30".

    Returns:
        str: A message indicating the action taken.
    """
    bulb_ip = "192.168.31.171"  # IP address of the Yeelight bulb
    bulb = Bulb(bulb_ip)
    bulb.set_brightness(30)
    return f"{inner_thoughts} Brightness set to 30%."

def set_brightness_to_40(inner_thoughts: str, command: str) -> str:
    """
    Set the brightness of the Yeelight bulb to 40%.

    Parameters:
        inner_thoughts (str): Inner thoughts to return alongside the action.
        command (str): The command to execute, "set brightness to 40".

    Returns:
        str: A message indicating the action taken.
    """
    bulb_ip = "192.168.31.171"  # IP address of the Yeelight bulb
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
DynamicSampleModel1 = create_dynamic_model_from_function(set_brightness_to_10, "lower down the brightness to 10%")
DynamicSampleModel5 = create_dynamic_model_from_function(set_brightness_to_40, "set the brightness to 40%")
DynamicSampleModel9 = create_dynamic_model_from_function(set_brightness_to_30, "increase the brightness to 30%")

function_tools = [LlamaCppFunctionTool(DynamicSampleModel3), LlamaCppFunctionTool(DynamicSampleModel4), LlamaCppFunctionTool(DynamicSampleModel1), LlamaCppFunctionTool(DynamicSampleModel5), LlamaCppFunctionTool(DynamicSampleModel9)]
function_tool_registry = LlamaCppAgent.get_function_tool_registry(function_tools)

# Use the Groq LLM for processing
client = Groq(api_key="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")

def get_groq_response(user_input: str) -> str:
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": user_input}],
        model="llama3-8b-8192"
    )
    return chat_completion.choices[0].message.content

# Main script logic
if __name__ == "__main__":
    user_input = from_mic()
    print(f"Transcribed text: {user_input}")

    # Process the transcribed text with Groq LLM
    groq_response = get_groq_response(user_input)
    print(f"Groq LLM Response: {groq_response}")

    # Process the response further if needed, here we simply print it
    # If additional processing is required, such as controlling the Yeelight bulb, add that logic here
    print("Processing completed.")
