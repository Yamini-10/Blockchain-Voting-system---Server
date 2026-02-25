from pydantic import BaseModel

class VoteRequest(BaseModel):
    candidate_id: int