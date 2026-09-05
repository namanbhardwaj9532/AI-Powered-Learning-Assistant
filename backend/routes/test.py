from fastapi import APIRouter, Depends
from bson import ObjectId
from config.db import quiz_collection,embeddings_collection,testcontent_collection, testattempts_collection
from config.groq import groq
from dependencies.check import get_user
import random
import json
from pydantic import BaseModel
from datetime import datetime, timezone

router=APIRouter()

@router.get("/{note_id}/test")
def test(note_id: str,
         user=Depends(get_user)):

    object_id = ObjectId(note_id)

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
        "user_id":user["_id"],
        "questions": questions
    }
    inserted_content=testcontent_collection.insert_one(quiz)

    test_id=inserted_content.inserted_id

    questions_for_frontend = []

    for question in questions:
        questions_for_frontend.append({
            "id": question["id"],
            "question": question["question"],
            "options": question["options"]
        })

    return {
        "test_id":str(test_id),
        "questions": questions_for_frontend
    }

class quizanswers(BaseModel):
    test_id: str
    answers: dict

@router.post("/test/submit")
def quizsubmission(
    submission: quizanswers,
    user=Depends(get_user)
):
    test_content = testcontent_collection.find_one({
        "_id": ObjectId(submission.test_id),
        "user_id": user["_id"]
    })

    if not test_content:
        return {
            "message": "Test not found"
        }

    score = 0

    for question in test_content["questions"]:
        q_id = str(question["id"])

        if submission.answers.get(q_id) == question["correct_answer"]:
            score += 1

    attempt={
        "test_id": ObjectId(submission.test_id),
        "score":score,
        "wrong":len(test_content["questions"])-score,
        "right":score,
        "submitted_at": datetime.now(timezone.utc)
    }

    testattempts_collection.insert_one(attempt)
    return {
        "score": score,
        "total": len(test_content["questions"])
    }