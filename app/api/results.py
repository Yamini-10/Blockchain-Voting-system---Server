from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.dependencies import get_db
from app.models.vote import Vote
from app.models.candidate import Candidate

router = APIRouter(prefix="/results", tags=["Results"])

@router.get("/")
def get_results(db: Session = Depends(get_db)):

    results = (
        db.query(
            Candidate.id,
            Candidate.name,
            Candidate.party,
            func.count(Vote.id).label("vote_count")
        )
        .outerjoin(Vote, Candidate.id == Vote.candidate_id)
        .group_by(Candidate.id)
        .all()
    )


    return [{"candidate": r[1], "votes": r[3], "party": r[2], "id": r[0]} for r in results]