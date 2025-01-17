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
# Initialize Web3 instance

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

DynamicSampleModel0 = create_dynamic_model_from_function(introduce_yourself, "introduce yourself")

DynamicSampleModel3 = create_dynamic_model_from_function(turn_off_light,"turn off")
DynamicSampleModel4 = create_dynamic_model_from_function(turn_on_light,"turn on")
DynamicSampleModel1 = create_dynamic_model_from_function(set_brightness_to_10, "lower down the brightness to 10%")
DynamicSampleModel5 = create_dynamic_model_from_function(set_brightness_to_50, "set the brightness to 50%")
DynamicSampleModel9 = create_dynamic_model_from_function(set_brightness_to_90, "increase the brightness to 90%")

function_tools = [LlamaCppFunctionTool(DynamicSampleModel3), LlamaCppFunctionTool(DynamicSampleModel4), LlamaCppFunctionTool(DynamicSampleModel1), LlamaCppFunctionTool(DynamicSampleModel5), LlamaCppFunctionTool(DynamicSampleModel9), LlamaCppFunctionTool(DynamicSampleModel0)]

function_tool_registry = LlamaCppAgent.get_function_tool_registry(function_tools)

main_model = LlamaCppEndpointSettings(
    completions_endpoint_url="http://127.0.0.1:8080/completion"
)

system_prompt = "You are a helpful, smart, kind, and efficient smart home AI assistant. You always fulfill the user's requests to the best of your ability.If you don't get any specific command, You will also try to understand what they are feeling and see what you could do to control the house system to fit their need .\n"

llama_cpp_agent = LlamaCppAgent(main_model, debug_output=True,
                                system_prompt=system_prompt + function_tool_registry.get_documentation(),
                                predefined_messages_formatter_type=MessagesFormatterType.CHATML)

user_input = "Hi, can you introduce yourself"


print(llama_cpp_agent.get_chat_response(user_input, temperature=0.45, function_tool_registry=function_tool_registry))
