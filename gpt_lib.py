import json
from openai import OpenAI

class Chatbot:
    def __init__(self, api_key, model):
        """Initialize with API key and model."""
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def chat_completion(self, messages):
        """Centralized chat completion logic."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )

            # Get the message content from the first choice
            message = response.choices[0].message.content
            return message

        except Exception as e:
            print(f"Error interacting with OpenAI API: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

class Conversation:
    def __init__(self):
        self.messages = []  # No default starting message

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

    def get_conversation_format(self):
        return [{"role": message["role"], "content": message["content"]} for message in self.messages]

    def save_to_file(self, file_path):
        """Save the conversation to a JSON file."""
        with open(file_path, 'w') as file:
            json.dump(self.messages, file, indent=4)

    def load_from_file(self, file_path):
        """Load the conversation from a JSON file."""
        with open(file_path, 'r') as file:
            self.messages = json.load(file)



if __name__ == "__main__":
    # Example usage
    api_key = "your_api_key_here"
    model = "gpt-4o-mini"  # Replace with the model you are using

    # Create a Chatbot instance
    chatbot = Chatbot(api_key, model)

    # Create a Conversation instance
    conversation = Conversation()

    # Add system and user messages
    system_message = """
    You are an AI assistant designed to help users with a variety of tasks, such as answering questions, providing information, and offering recommendations. 
    Your goal is to assist the user in the most helpful and efficient manner possible. 
    Ensure that your responses are accurate, relevant, and clear.

    Examples:
    - User: "What's the weather like today?"
      AI: "The weather today is sunny with a high of 75°F."
    - User: "Can you recommend a good book?"
      AI: "I recommend 'To Kill a Mockingbird' by Harper Lee."
    - User: "How do I bake a cake?"
      AI: "To bake a cake, you will need flour, sugar, eggs, and butter. Start by preheating your oven to 350°F..."
    """
    user_input = "How are you doing today?"

    # Load the conversation from a file
    conversation.load_from_file('conversation.json')

    conversation.add_message("system", system_message)
    conversation.add_message("user", user_input)

    # Get the conversation format
    messages = conversation.get_conversation_format()

    # Save the conversation to a file
    conversation.save_to_file('conversation.json')


    # Get the GPT response
    response = chatbot.chat_completion(messages)

    # Print the response
    print(response)
