from fastapi import APIRouter, Depends, Request
from dependencies.check import get_user
from fastapi.responses import JSONResponse

router=APIRouter()

@router.get("/main")
def main(user=Depends(get_user)):
    return {"uid":user["username"]}

@router.post("/logout")
def logout(request:Request):
    response=JSONResponse({
        "message":"loged out"
    })
    response.delete_cookie("uid")
    return response