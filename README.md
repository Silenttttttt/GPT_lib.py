### GPT-Lib

#### Overview:

The GPT-Lib module provides utility functions and classes to interact with the OpenAI GPT model, manage conversations, and log variable information as well as uncaught exceptions. This module leverages OpenAI's API and offers a comprehensive logging mechanism for debugging and tracking.

#### Key Features:

- Advanced Logging: Allows you to log variable information, uncaught exceptions, and code tracebacks.

- Chatbot Functionality: Provides methods to initiate and manage interactions with OpenAI's GPT model.

- Conversation Management: Allows easy storage and retrieval of conversation history in a structured format suitable for OpenAI's API.


### How To Use:

1. Ensure you have the necessary libraries installed: openai, loguru, and others as mentioned in the module.

2. Initialize the Chatbot class with your OpenAI API key and desired model.

3. Start a conversation using the Conversation class and interact with the GPT model using the Chatbot class.

4. Add, read, and write messages using the provided methods in the Conversation class.


## Example Usage:

An example is provided in the `Example.py` demonstrating a back-and-forth chat with the AI using the same conversation.

Run the example script. Interact with the AI and experience a real-time conversation. You can continue or stop the chat as you wish.

### Notes:

- `Ensure you have a valid API key from OpenAI.`

- `The logging mechanism provided in the module helps in debugging and tracking. Check the variables.log and app.log for logged details.`

- `OpenAi's documentation: https://platform.openai.com/docs/api-reference/introduction and https://openai.com/blog/function-calling-and-other-api-updates`


#### Key Classes & Methods:

- `log_variable_info: Logs information about a given variable.`

- `log_uncaught_exceptions: Logs uncaught exceptions to a file.`

- `Chatbot:__init__(self, api_key, model, starting_message=None): Initializes the chatbot.chat_completion_api(self, conversation_format): Interacts with OpenAI's API to get a response.`

- `__init__(self, api_key, model, starting_message=None): Initializes the chatbot.`

- `chat_completion_api(self, conversation_format): Interacts with OpenAI's API to get a response.`

- `Conversation:__init__(self, starting_message=None): Initializes the conversation.add_message(self, role, content): Adds a message to the conversation.read_from_json(self, filename): Reads conversation history from JSON.write_to_json(self, filename): Writes conversation history to JSON.get_conversation_format(self): Gets conversation in a structured format for OpenAI's API.`

- `__init__(self, starting_message=None): Initializes the conversation.`

- `add_message(self, role, content): Adds a message to the conversation.`

- `read_from_json(self, filename): Reads conversation history from JSON.`

- `write_to_json(self, filename): Writes conversation history to JSON.`

- `get_conversation_format(self): Gets conversation in a structured format for OpenAI's API.`
