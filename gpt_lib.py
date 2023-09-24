import os
import openai
import json
import time
import inspect
from loguru import logger
import sys
import logging
import traceback
import builtins
from io import StringIO
from contextlib import redirect_stdout
import trace
import datetime

# Setup for logger
logger.remove()
logger.add("variables.log", level="INFO", enqueue=True)
logger.add("variables.log", level="ERROR", enqueue=True)

def log_variable_info(variable, name=None):
    """
    Logs information about a given variable including its name, type, value, 
    the function it was called from, filename, and traceback.
    """
    # Get the frame and details of the caller
    calling_frame = inspect.currentframe().f_back
    calling_function_name = calling_frame.f_code.co_name
    calling_line_number = calling_frame.f_lineno
    calling_file_name = calling_frame.f_code.co_filename
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    
    # Formulate the traceback excluding the current function call
    tb_list = traceback.format_stack()
    tb_list.pop(-1)
    tb_list = [tb.strip() for tb in tb_list]
    
    # Attempt to get the variable's attributes if it's an object
    if isinstance(variable, object):
        try:
            variable_value = str(vars(variable))
        except:
            variable_value = str(variable)
    else:
        variable_value = str(variable)
    
    # Construct the log message
    log_dict = {
        "Name": name,
        "line_number": calling_line_number,
        "timestamp": timestamp,
        "function_name": calling_function_name,
        "file_name": calling_file_name,
        "variable_type": str(type(variable)),
        "variable_value": variable_value,
        "traceback": tb_list
    }
    log_json = json.dumps(log_dict, indent=2)
    logger.info(log_json)

def log_uncaught_exceptions(exc_type, exc_value, exc_traceback):
    """
    Logs uncaught exceptions to a file.
    """
    # Construct the log message
    log_dict = {
        "exception_type": str(exc_type),
        "exception_value": str(exc_value),
        "exception_traceback": traceback.format_tb(exc_traceback)
    }
    log_json = json.dumps(log_dict, indent=2)

    # Write the log message to a file and also log using logger
    with open('variables.log', 'a') as f:
        f.write(log_json)
        f.write('\n')
    logger.error(log_json, exc_info=(exc_type, exc_value, exc_traceback))

# Setup for code tracing using the standard logging module
logging.basicConfig(filename='app.log', level=logging.INFO)

def log_trace(frame, event, arg):
    """
    Function to trace and log each executed line of code.
    """
    if event != 'line':
        return

    co = frame.f_code
    func_name = co.co_name
    filename = co.co_filename
    line_no = frame.f_lineno
    line = linecache.getline(filename, line_no).strip()

    logging.debug(f"{func_name}({arg}) {filename}:{line_no} {line}")

    return log_trace

def start_logging():
    """
    Starts the code execution logging.
    """
    sys.settrace(log_trace)

def stop_logging():
    """
    Stops the code execution logging.
    """
    sys.settrace(None)

# Chatbot functionalities
class Chatbot:
    def __init__(self, api_key, model, starting_message=None): 
        """
        Initializes the Chatbot with given API key, model, and an optional starting message.
        """
        self.api_key = api_key
        self.model = model
        self.conversation = Conversation(starting_message)

    def chat_completion_api(self, conversation_format):
        """
        Interacts with OpenAI's ChatCompletion API for a response based on the current conversation.
        """
        # Set the OpenAI API key
        openai.api_key = self.api_key

        # Construct the messages for the chat completion API
        messages = [{"role": message["role"], "content": message["content"].lower()} for message in conversation_format]
        
        # Make the API call and extract the content from the response
        response = openai.ChatCompletion.create(model=self.model, messages=messages)
        content = response['choices'][0]['message']['content']
        
        return {"response": content}

class Conversation:
    def __init__(self, starting_message=None):  
        """
        Initializes the Conversation with an optional starting message.
        """
        self.messages = [{"role": "system", "content": "Starting message" if starting_message is None else starting_message}]

    def add_message(self, role, content):
        """
        Adds a message to the conversation.
        """
        self.messages.append({"role": role, "content": content})

    def read_from_json(self, filename):
        """
        Reads the conversation history from a JSON file.
        """
        try:
            with open(filename, "r") as f:
                conversation_json = json.load(f)
            self.messages = conversation_json["messages"]
        except:
            pass

    def write_to_json(self, filename):
        """
        Writes the conversation history to a JSON file.
        """
        conversation_json = {"messages": self.messages}
        with open(filename, "w") as f:
            json.dump(conversation_json, f, indent=2)

    def get_conversation_format(self):
        """
        Returns the conversation in a formatted structure suitable for OpenAI's API.
        """
        return [{"role": message["role"], "content": message["content"]} for message in self.messages]
