import os
from anthropic import Anthropic
from dotenv import load_dotenv
import tiktoken

load_dotenv()

DEFAULT_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
DEFAULT_MODEL = "claude-haiku-4-5"
DEFAULT_SYSTEM_MESSAGE = "You are a sassy assistant who is fed up with answering questions."
DEFAULT_MAX_TOKENS = 1024
DEFAULT_TEMPERATURE = 0.2
DEFAULT_TOKEN_BUDGET = 4096

class ConversationManager():
    def __init__(self, api_key=None, base_url=None, system_message=None, model=None, max_tokens=None, temperature=None, token_budget=None):
        self.api_key = api_key if api_key is not None else DEFAULT_API_KEY
        self.system_message = system_message if system_message is not None else DEFAULT_SYSTEM_MESSAGE
        self.model = model if model is not None else DEFAULT_MODEL
        self.max_tokens = max_tokens if max_tokens is not None else DEFAULT_MAX_TOKENS
        self.token_budget = token_budget if token_budget is not None else DEFAULT_TOKEN_BUDGET
        self.temperature = temperature if temperature is not None else DEFAULT_TEMPERATURE
        self.client = Anthropic(api_key=self.api_key)
        self.conversation_history = [{"role": "system", "content": self.system_message}]

    def chat_completion(self, prompt):
        self.messages = [
            {"role": "user", "content": prompt}
            ]
        
        self.conversation_history.append(self.messages[0])
        
        self.response = self.client.messages.create(model=self.model,
                                                    max_tokens=self.max_tokens,
                                                    system=self.system_message,
                                                    messages=self.messages,
                                                    temperature=self.temperature)
        
        ai_response = self.response.content[0].text

        self.conversation_history.append({"role": "ai_assistant", "content": ai_response})
        print(f"Total tokens used: {self.total_tokens_used()}")

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
    
conv_manager = ConversationManager()
print(conv_manager.chat_completion("Tell me a joke"))