import streamlit as st

import json
from pprint import pprint
from time import sleep

from function_caller import *

def render_message(message:str = "", 
                   chunk_size : int = 10,
                   time_delay:float = 0.04,
                   smooth : bool = True):
    
    curr_len = chunk_size

    if not smooth:
        st.markdown(message)
        return

    text_container = st.markdown("")

    while curr_len < len(message):
        text_container.markdown(message[:curr_len] + "▌")
        curr_len += chunk_size
        sleep(time_delay)
    
    text_container.markdown(message)

    
def process_command(command:str):
    
    finish_reason, gpt_response = make_gpt_call(query=command)

    if finish_reason == "stop":
        print('No function called by GPT')
        return gpt_response['content']

    elif finish_reason == "function_call":
        # extract the name of the function to be called
        func_name = gpt_response['function_call']['name']

        # extract function arguments
        args = json.loads(gpt_response.to_dict()['function_call']['arguments'])
        
        print(func_name)
        pprint(args)
        response_message = make_function_call(func_name, args)
        return response_message
