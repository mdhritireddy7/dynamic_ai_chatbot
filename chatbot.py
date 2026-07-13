import os
from anthropic import Anthropic
from dotenv import load_dotenv
import tiktoken
from datetime import datetime
import json

load_dotenv()

DEFAULT_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
DEFAULT_MODEL = "claude-haiku-4-5"
DEFAULT_SYSTEM_MESSAGE = "You are a sassy assistant who is fed up with answering questions."
DEFAULT_MAX_TOKENS = 1024
DEFAULT_TEMPERATURE = 0.2
DEFAULT_TOKEN_BUDGET = 4096

now = datetime.now()
timestamp = now.strftime("%Y%m%d_%H%M%S")
filename = f"file_{timestamp}.txt"
DEFAULT_HISTORY_FILE = filename

class ConversationManager():
    def __init__(self, api_key=None, base_url=None, system_message=None, model=None, max_tokens=None, temperature=None, token_budget=None, history_file=None):
        self.api_key = api_key if api_key is not None else DEFAULT_API_KEY
        self.system_message = system_message if system_message is not None else DEFAULT_SYSTEM_MESSAGE
        self.system_messages = {"sassy_assistant": "A sassy assistant who is fed up with answering questions.", 
                                "angry_assistant": "An angry assistant that likes yelling in all caps.", 
                                "thoughtful_assistant": "A thoughtful assistant, always ready to dig deeper. This assistant asks clarifying questions to ensure understanding and approaches problems with a step-by-step methodology.",
                                "custom": "A placeholder for your custom system message."}
        self.model = model if model is not None else DEFAULT_MODEL
        self.max_tokens = max_tokens if max_tokens is not None else DEFAULT_MAX_TOKENS
        self.token_budget = token_budget if token_budget is not None else DEFAULT_TOKEN_BUDGET
        self.temperature = temperature if temperature is not None else DEFAULT_TEMPERATURE
        self.client = Anthropic(api_key=self.api_key)
        self.history_file = history_file if history_file is not None else DEFAULT_HISTORY_FILE

        self.load_conversation_history()

    def chat_completion(self, prompt):
        self.messages = [
            {"role": "user", "content": prompt}
            ]
        
        self.conversation_history.append(self.messages[0])

        self.enforce_token_management()
        
        self.response = self.client.messages.create(model=self.model,
                                                    max_tokens=self.max_tokens,
                                                    system=self.system_message,
                                                    messages=self.messages,
                                                    temperature=self.temperature)
        
        ai_response = self.response.content[0].text

        self.conversation_history.append({"role": "ai_assistant", "content": ai_response})
        print(f"Total tokens used: {self.total_tokens_used()}")

        self.save_conversation_history()

        return ai_response
    
    def count_tokens(self, text):
        try: 
            encoding = tiktoken.encoding_for_model(self.model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")

        tokens = encoding.encode(text)

        return len(tokens)
    
    def total_tokens_used(self):
        return sum(self.count_tokens(message['content'] for message in self.conversation_history))
    

    def enforce_token_management(self):
        while self.total_tokens_used() > self.token_budget:
            self.conversation_history.pop(1)

    def set_persona(self, persona):
        if persona in self.system_messages:
            self.system_message = self.system_messages[persona]
            self.update_system_message_in_history()
        else:
            raise ValueError("Persona not found")
        
    def set_custom_system_message(self, custom_message):
        if not custom_message:
            raise ValueError("Custom message cannot be empty.")
        self.system_messages["custom"] = custom_message
        self.set_persona("custom")

    
    def update_system_message_in_history(self):
        if self.conversation_history and self.conversation_history[0]["role"] == "system":
            self.conversation_history[0]["content"] = self.system_message
        else:
            self.conversation_history.insert(0, {"role": "system", "content": self.system_message})

    def load_conversation_history(self):
        try:
            with open(self.history_file, "r") as file:
                self.conversation_history = json.load(file)
        except FileNotFoundError:
            self.conversation_history = [{"role": "system", "content": self.system_message}]
        except json.JSONDecodeError:
            print("Error reading the conversation history file. Starting with an empty history.")
            self.conversation_history = [{"role": "system", "content": self.system_message}]

    def save_conversation_history(self):
        with open(self.history_file, "w") as file:
            json.dump(self.conversation_history, file, indent=4)

    
conv_manager = ConversationManager()
print(conv_manager.chat_completion("Tell me a joke"))