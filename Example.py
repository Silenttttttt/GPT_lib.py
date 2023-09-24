from gpt_lib import Chatbot, Conversation

def main():
    # Initialize Chatbot and Conversation
    api_key = "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"  # Replace with your OpenAI API Key
    model = "gpt-3.5-turbo"  # or the desired model
    chatbot = Chatbot(api_key, model, "Hello!")
    conversation = Conversation("Hello!")
    
    while True:
        user_input = input("You: ")
        
        # Add user message to conversation
        conversation.add_message("user", user_input)
        
        # Get formatted conversation for OpenAI's API
        formatted_conversation = conversation.get_conversation_format()
        
        # Get response from chatbot
        response = chatbot.chat_completion_api(formatted_conversation)
        
        print(f"AI: {response['response']}")
        
        # Add AI's response to conversation
        conversation.add_message("system", response['response'])

        cont = input("Continue conversation? (yes/no): ")
        if cont.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
