"""De mensajes a prompt: apply_chat_template."""
import os

from dotenv import load_dotenv
from transformers import AutoTokenizer

load_dotenv()

MODEL = os.getenv("CHAT_TEMPLATE_MODEL", "HuggingFaceTB/SmolLM2-1.7B-Instruct")

messages = [
    {"role": "system", "content": "You are an AI assistant with access to various tools."},
    {"role": "user", "content": "Hi !"},
    {"role": "assistant", "content": "Hi human, what can help you with ?"},
    {"role": "user", "content": "What is a chat template?"},
]

if __name__ == "__main__":
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    prompt = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    print(prompt)