from fastapi import FastAPI
from routes.auth import router as auth_router
from routes.main import router as main_router


app=FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def server():
    return {"message":"server running"}

app.include_router(auth_router)
app.include_router(main_router)


