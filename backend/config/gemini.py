from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

key=os.getenv("gemini_key")

client =genai.Client(
    api_key=key
)
def gemini(prompt):
    interaction = client.interactions.create(
        model="gemini-3.5-flash",
        input=prompt
        )
    return interaction.output_text

def embed(chunks):

    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=chunks
    )

    return [embedding.values for embedding in result.embeddings]