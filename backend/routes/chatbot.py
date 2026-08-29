from fastapi import APIRouter
from config.groq import groq
from pydantic import BaseModel

router= APIRouter()

class chatreq(BaseModel):
    prompt:str

@router.post("/chatbot")
def chatbot(req:chatreq):
    result=groq(req.prompt)
    return {
        "output":result
    }