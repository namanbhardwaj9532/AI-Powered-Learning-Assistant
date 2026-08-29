from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("groq_key")

client = OpenAI(
    api_key=key,
    base_url="https://api.groq.com/openai/v1"
)


def groq(prompt):
    response = client.responses.create(
        model="openai/gpt-oss-20b",
        input=prompt
    )

    return response.output_text