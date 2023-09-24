import json
import openai

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
        # Commented out print statement can be used for debugging purposes
        # print(self.messages)

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

class Chatbot:
    def __init__(self, api_key, model, starting_message=None):
        """
        Initializes the Chatbot with given API key, model, and an optional starting message.
        """
        self.api_key = api_key
        self.model = model
        if starting_message:
            self.conversation = Conversation(starting_message)
        else:
            self.conversation = Conversation()

    def chat_completion_api(self, conversation, user_input):
        """
        Interacts with OpenAI's ChatCompletion API for a response based on the current conversation 
        and user input. Also makes a function call to generate an HTML email.
        """
        openai.api_key = self.api_key

        # Construct the messages for the chat completion API
        messages = [{"role": message["role"], "content": message["content"]} for message in conversation.messages]

        # Add user input to the messages
        messages.append({"role": "user", "content": user_input})

        # Make the API call with an additional function to generate an HTML email
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            functions=[
                {
                    "name": "generate_html_email",
                    "description": "Generate an HTML email",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "Content for the email",
                            }
                        },
                        "required": ["content"],
                    },
                }
            ],
            function_call={"name": "generate_html_email"},
        )

        # Extract the function call result from the response
        function_call = response['choices'][0].get('function_call', {})
        
        try:
            email_content = json.loads(response['choices'][0]['message']['function_call']['arguments'])['content']
            return {"email_content": email_content}
        except:
            print("Failed to get HTML email content from the model's response.")
            email_content = ""

        return {"email_content": email_content}


# # Example usage
# api_key = "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"
# model = "gpt-3.5-turbo-0613"  # Use appropriate GPT-4 model name
# chatbot = Chatbot(api_key, model)

# conversation = Conversation()  # Assuming you have Conversation class as defined in your original post

# user_input = """
# You are the AI assistant tasked with crafting an impactful email in HTML format to advertise CryptoFuse.net. Your goal is to compel and intrigue the recipient to visit and utilize the platform. 

# Guidelines:
# - The email should be in HTML format.
# - Subject Line: Should be gripping, evoking curiosity. It's their first touchpoint.
# - Email Body: 
#     - Address the recipient personally.
#     - Introduce with a magnetic opener.
#     - Enumerate the standout features of CryptoFuse.net without overwhelming them.
#     - Use emotive language, but avoid being pushy.
#     - A clear and compelling call to action is crucial.
#     - Ensure the tone remains professional yet approachable.
#     - Capitalize the first letter of new lines.
# - Personalization is the key. Each email should feel like it's specially crafted for the recipient website.
# - Make the text visually engaging. Usage of emojis or other visual elements can be impactful, but don't overdo it.
# - Maintain a clear structure for easy readability.
# - Your output should contain the email subject and body in HTML format. No added remarks or notes.
# - You should direct them to CryptoFuse.net.
# - The only link in the email must be to CryptoFuse.net.

# Use this image "https://www.cryptofuse.net/static/images/logo-min.e146a3a94796.png

# Make the html email actually look nice."
# """
# result = chatbot.chat_completion_api(conversation, user_input)

# with open('email_contentss.html', 'w') as file:
#     file.write(result['email_content'])

# print("HTML content has been saved to 'email_content.html'")