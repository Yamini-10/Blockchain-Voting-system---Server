from pydantic import BaseModel

class CandidateCreate(BaseModel):
    name: str
    party: str

class CandidateResponse(BaseModel):
    id: int
    name: str
    party: str

    class Config:
        from_attributes  = True

