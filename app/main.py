from fastapi import FastAPI
from app.api import auth, vote, admin, results, candidate
from app.db.base import Base
from app.db.session import engine
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blockchain Voting System")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(vote.router)
app.include_router(admin.router)
app.include_router(results.router)
app.include_router(candidate.router)
@app.get("/")
def root():
    return {"message": "Blockchain Voting Backend Running"}