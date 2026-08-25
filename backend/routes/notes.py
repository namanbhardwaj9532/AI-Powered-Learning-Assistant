from fastapi import FastAPI, Depends, Form, File, UploadFile, APIRouter
from config.db import notes_collection
from config.db import embeddings_collection
from dependencies.check import get_user
import os
from uuid import uuid4
from fastapi.staticfiles import StaticFiles
from bson import ObjectId
from pypdf import PdfReader
from config.gemini import embed
from pydantic import BaseModel
from config.gemini import gemini
import numpy as np

router=APIRouter()


@router.get("/notes")
def all_notes(user=Depends(get_user)):
    notes=list(notes_collection.find({
        "user_id":user["_id"]
    }))

    for note in notes:
        note["_id"] = str(note["_id"])
        note["user_id"] = str(note["user_id"])
    return notes


def split_text(text, chunk_size=500, overlap=100):

    chunks = []

    step = chunk_size - overlap

    for i in range(0, len(text), step):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)

    return chunks

@router.post("/notes")
def add_note(
    title: str = Form(...),
    content: str = Form(None),
    file: UploadFile = File(...),
    user=Depends(get_user)
):
    new_name = None

    if file:
        os.makedirs("uploads", exist_ok=True)

        file_ext = os.path.splitext(file.filename)[1]
        new_name = f"{uuid4()}{file_ext}"

        file_path = os.path.join("uploads", new_name)

        with open(file_path, "wb") as f:
            f.write(file.file.read())


    reader=PdfReader(file_path)
    text = ""
    
    for page in reader.pages:
        text += page.extract_text() or ""

    chunks=split_text(text)
    new_note = {
        "user_id": user["_id"],
        "username": user["username"],
        "title": title,
        "content": content,
        "filename": file.filename if file else None,
        "filesavedname": new_name,
    }

    result=notes_collection.insert_one(new_note)
    note_id=result.inserted_id

    embeddings=embed(chunks)

    documents = []

    for i, chunk in enumerate(chunks):
        documents.append({
            "note_id": note_id,
            "chunk_index": i,
            "chunk": chunk,
            "embedding": embeddings[i]
        })

    embeddings_collection.insert_many(documents)

    notes = list(notes_collection.find({
        "user_id": user["_id"]
    }))

    for note in notes:
        note["_id"] = str(note["_id"])
        note["user_id"] = str(note["user_id"])

    return notes




@router.get("/file/{note_id}")
def get_note(note_id: str):

    note = notes_collection.find_one({
        "_id": ObjectId(note_id)
    })

    reader = PdfReader(f"uploads/{note['filesavedname']}")

    tolpage=len(reader.pages)

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""


    return {
        "title": note["title"],
        "filename": note["filename"],
        "text": text,
        "tolpages":tolpage
    }



class chatreq(BaseModel):
    prompt:str

@router.post("/{note_id}/chatbot")
def noteschatbot(req:chatreq,
                 note_id:str):
    prompt_embedding= np.array(
        embed(req.prompt)[0],
        dtype=np.float32
    )
    documents=list(embeddings_collection.find({
        "note_id":ObjectId(note_id)
    })
    )
    if not documents:
        return {
            "output": "No content found in this note."
        }

    embeddings= np.array(
        [doc["embedding"] for doc in documents],
        dtype=np.float32
    )
    results=[]
    prompt_embedding/=np.linalg.norm(prompt_embedding)
    embeddings /= np.linalg.norm(
        embeddings,
        axis=1,
        keepdims=True
    )
    similarities = embeddings @ prompt_embedding
    top_indices = np.argsort(similarities)[-5:][::-1]

    top_chunks = []

    for index in top_indices:
        top_chunks.append({
            "chunk": documents[index]["chunk"],
            "similarity": float(similarities[index])
        })

    context="\n\n".join(
        item["chunk"] for item in top_chunks
    )
    prompt = f"""
        You are an intelligent AI assistant helping the user understand their document.

        The document context is provided below. Use it as your primary source of
        information, but do not simply copy sentences from it.

        You should:
        - Understand the meaning of the provided context.
        - Combine information from multiple parts of the context when necessary.
        - Explain concepts in your own words.
        - Make reasonable inferences and conclusions when they logically follow
        from the information in the context.
        - Answer conceptual "why", "how", and "what does this mean" questions
        using your understanding of the context.
        - Give examples when they help explain the answer.
        - Do not invent facts that contradict the document.
        - If the document does not provide enough information to answer the
        question, clearly say what information is missing.

        Document context:
        {context}

        User question:
        {req.prompt}

        Provide a clear, useful answer to the user.
        """

    result=gemini(prompt)
    return {
        "output":result
    }