from fastapi import APIRouter
from bson import ObjectId
from config.db import quiz_collection,embeddings_collection
from config.groq import groq
import random
import json
from pydantic import BaseModel

router=APIRouter()

@router.get("/{note_id}/test")
def test(note_id: str):

    object_id = ObjectId(note_id)

    quiz=quiz_collection.find_one({
        "note_id":object_id
    })

    if quiz:
        questions = []

        for question in quiz["questions"]:
            questions.append({
                "id": question["id"],
                "question": question["question"],
                "options": question["options"]
            })

        return {
            "questions": questions
        }

    document= list(
        embeddings_collection.find({
            "note_id":object_id
        })
    )

    selected_chunks = random.sample(
        document,
        min(10,len(document))
    )

    content ="\n\n".join(
        doc["chunk"] for doc in selected_chunks
    )

    prompt = f"""
From the given text, create 5 simple questions.

Rules:
- provide MCQ-type questions
- Questions must be based only on the given text.
- Keep the questions simple.
- Return exactly 5 questions.
- Provide 4 options for each question.
- Provide the correct answer for each question.
- The correct answer must be exactly one of the four options.
- Return only valid JSON.
- Do not include markdown or extra text.

Format:

[
{{
"id": 1,
"question": "Question 1",
"options": [
"Option 1",
"Option 2",
"Option 3",
"Option 4"
],
"correct_answer": "Option 2"
}},
{{
"id": 2,
"question": "Question 2",
"options": [
"Option 1",
"Option 2",
"Option 3",
"Option 4"
],
"correct_answer": "Option 1"
}},
{{
"id": 3,
"question": "Question 3",
"options": [
"Option 1",
"Option 2",
"Option 3",
"Option 4"
],
"correct_answer": "Option 4"
}},
{{
"id": 4,
"question": "Question 4",
"options": [
"Option 1",
"Option 2",
"Option 3",
"Option 4"
],
"correct_answer": "Option 3"
}},
{{
"id": 5,
"question": "Question 5",
"options": [
"Option 1",
"Option 2",
"Option 3",
"Option 4"
],
"correct_answer": "Option 1"
}}
]

Text:
{content}
"""

    result = groq(prompt)
    questions=json.loads(result)
    quiz = {
        "note_id": object_id,
        "questions": questions
    }
    quiz_collection.insert_one(quiz)

    questions_for_frontend = []

    for question in questions:
        questions_for_frontend.append({
            "id": question["id"],
            "question": question["question"],
            "options": question["options"]
        })

    return {
        "questions": questions_for_frontend
    }

class quizanswers(BaseModel):
    answers:dict

@router.post("/{note_id}/test/submit")
def quizsubmission(
    note_id: str,
    submission: quizanswers
):
    objectid = ObjectId(note_id)

    quiz = quiz_collection.find_one({
        "note_id": objectid
    })

    if not quiz:
        return {
            "message": "Quiz not found"
        }

    score = 0

    for question in quiz["questions"]:
        q_id = str(question["id"])

        correctanswer = question["correct_answer"]

        answer = submission.answers.get(q_id)

        if answer == correctanswer:
            score += 1

    return {
        "score": score,
        "total": len(quiz["questions"])
    }