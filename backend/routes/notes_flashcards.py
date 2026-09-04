from fastapi import APIRouter, Depends
from bson import ObjectId
from config.groq import groq
from config.db import embeddings_collection
from config.db import flashcards_collection
from dependencies.check import get_user
import json
from bson.errors import InvalidId
from fastapi import APIRouter, Depends, HTTPException
router=APIRouter()


def extract_keywords(content):
    prompt = f"""
Extract the most important keywords and key concepts from the following study material.

Rules:
- Extract only meaningful keywords or concepts.
- Focus on important technical terms, concepts, topics, names, methods, and definitions.
- Do not extract common or generic words.
- Do not include complete sentences.
- Do not include duplicate or closely repeated keywords.
- Keywords must be directly related to the given text.
- Return between 5 and 15 keywords depending on the amount of useful information.
- Return only valid JSON.
- Do not include markdown or any extra text.

Format:

{{
    "keywords": [
        "keyword 1",
        "keyword 2",
        "keyword 3"
    ]
}}

Text:
{content}
"""

    result=groq(prompt)
    return json.loads(result)["keywords"]


def produce_flashcard(keywords, content):

    prompt = f"""
Create flashcards from the following study material.

Keywords:
{keywords}

Rules:
- Generate 3 to 5 flashcards.
- Generate flashcards only for important concepts.
- Use the keywords to identify important concepts.
- The answers must come only from the provided study material.
- Do not add information that is not present in the study material.
- Keep questions clear and suitable for revision.
- Keep answers concise but informative.
- Do not create duplicate flashcards.
- Return only valid JSON.
- Do not include markdown or extra text.

Format:

{{
    "flashcards": [
        {{
            "question": "Question here",
            "answer": "Answer here"
        }},
        {{
            "question": "Question here",
            "answer": "Answer here"
        }}
    ]
}}

Study Material:
{content}
"""

    result = groq(prompt)

    try:
        data = json.loads(result)
        return data["flashcards"]

    except (json.JSONDecodeError, KeyError) as e:
        print("Invalid LLM response:")
        print(result)
        print("Error:", e)

        raise HTTPException(
            status_code=500,
            detail="Failed to generate flashcards"
        )

    
@router.get("/{note_id}/flashcards")
def flashcards(
    note_id: str,
    user=Depends(get_user)
):
    try:
        object_id = ObjectId(note_id)
    except InvalidId:
        raise HTTPException(
            status_code=400,
            detail="Invalid note ID"
        )

    # Check if flashcards already exist
    saved_flashcards = flashcards_collection.find_one({
        "user_id": user["_id"],
        "note_id": object_id
    })

    if saved_flashcards:
        return {
            "flashcards": saved_flashcards["flashcards"]
        }

    # Get document chunks
    document = list(
        embeddings_collection.find({
            "note_id": object_id
        })
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    all_flashcards = []

    # Process chunks in batches
    for i in range(0, len(document), 10):

        batch = document[i:i + 10]

        content = "\n\n".join(
            doc["chunk"] for doc in batch
        )

        keywords = extract_keywords(content)

        flashcards = produce_flashcard(
            keywords,
            content
        )

        all_flashcards.extend(flashcards)

    # Save generated flashcards
    flashcards_collection.insert_one({
        "user_id": user["_id"],
        "note_id": object_id,
        "flashcards": all_flashcards
    })

    return {
        "flashcards": all_flashcards
    }