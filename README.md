# Dynamic AI Chatbot with Personas

A command line chatbot built in Python that can take on distinct personas, track conversation history for contextually aware responses, and manage token usage against a fixed budget. Built as part of the Dataquest AI Engineering path, extended and structured for standalone use.

## Features

- **Switchable personas** defined through system messages, such as an exasperated assistant, an all caps responder, or a curious assistant that asks follow up questions
- **Conversation memory** so the model can reference earlier turns and stay coherent across a session
- **Token budget tracking** using `tiktoken` to count tokens per exchange and stop cleanly before exceeding a set limit
- **Configurable LLM backend** via the OpenAI Python SDK, pointed at Together.ai's API (works with OpenAI's API as well)

## How it works

Each conversation starts with a system message that sets the persona. User messages and model responses are appended to a running message list, which is sent in full on every API call so the model has context. Before each call, the total token count of the history is measured with `tiktoken`, and the session ends gracefully if the next exchange would exceed the token budget.

## Setup

1. Clone the repo and create a virtual environment:

```bash
git clone https://github.com/mdhritireddy7/dynamic_ai_chatbot.git
cd dynamic_ai_chatbot
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Get an API key from [Together.ai](https://api.together.ai/) (free credits on signup) or Anthropic.

3. Create a `.env` file in the project root:

```
TOGETHER_API_KEY=your_key_here
```

4. Run the chatbot:

```bash
python chatbot.py
```

## Example session

```
Persona: Exasperated Assistant

You: What's the capital of France?
Bot: Paris. Obviously. It's been Paris for quite a while now.

You: What about Germany?
Bot: Berlin. Is there a theme here, or are we just going through Europe one country at a time?
```

## Tech stack

- Python 3
- Anthropic Python SDK
- tiktoken for token counting
- python-dotenv for environment variable management

## What I learned

- Structuring multi turn conversations as message lists and why full history must be resent on each call
- Using system messages to control model behavior and tone
- Estimating and enforcing token budgets before making API calls rather than reacting to errors after

## Possible extensions

- Persist conversation history to disk so sessions can resume
- Add a summarization step to compress old history instead of hard stopping at the token limit
- Wrap the chatbot in a simple web UI
