# GPT Autocomplete

## Description

This repository contains a Python module that uses OpenAI's GPT model to autocomplete text. The module provides functions to interact with the GPT model and generate text continuations based on user input. It also supports saving and loading conversations to and from JSON files.

## Features

- Uses OpenAI's GPT model to generate an autocomplete continuation of the provided text.
- Provides a simple API for interacting with the GPT model.
- Supports saving and loading conversations to and from JSON files.

## Requirements

- Python 3.x
- OpenAI API key

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/Silenttttttt/gpt-autocomplete.git
   cd gpt-autocomplete
   ```

2. Install the required libraries:
   ```sh
   pip install openai
   ```

## Usage

1. Create a new script, `main.py`, and use the `gpt_lib` module:

   ```python
   import gpt_lib

   if __name__ == "__main__":
       # Define your API key and model
       api_key = "your_openai_api_key"
       model = "gpt-4o-mini"  # Replace with the model you are using

       # Create a Chatbot instance
       chatbot = gpt_lib.create_chatbot(api_key, model)

       # Create a Conversation instance
       conversation = gpt_lib.create_conversation()

       # Add system and user messages
       system_message = """
       You are an AI designed to assist users by continuing their sentences based on the context provided. 
       Your goal is to continue the text without repeating any letters or words already present in the input. 
       Ensure that your completions are coherent and contextually relevant.

       Examples:
       - User: "Tell me about the wea"
         AI: "ther today."
       - User: "The quick brown"
         AI: "fox jumps over the lazy dog."
       - User: "I love programming in Pyt"
         AI: "hon because it's versatile."
       """
       user_input = "Tell me about the wea"

       conversation.add_message("system", system_message)
       conversation.add_message("user", user_input)

       # Save the conversation to a file
       conversation.save_to_file('conversation.json')

       # Load the conversation from a file
       conversation.load_from_file('conversation.json')

       # Get the conversation format
       messages = conversation.get_conversation_format()

       # Get the GPT response
       response = chatbot.chat_completion(messages)

       # Print the response
       print(response)
   ```

2. Run the script:
   ```sh
   python main.py
   ```

## License

This project is licensed under  under the GNU General Public License v3.0
````

This setup provides a clean and focused module for generating text continuations using OpenAI's GPT model, along with support for saving and loading conversations to and from JSON files. The example script and detailed instructions in the README demonstrate how to use these features.
`````
