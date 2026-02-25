from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.services.vote_service import cast_vote
from app.schemas.vote import VoteRequest
from app.models.user import User
from app.models.vote import Vote

router = APIRouter(prefix="/vote", tags=["Vote"])

@router.post("/")
def vote(
    request: VoteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        vote = cast_vote(
            db=db,
            user=current_user,
            candidate_id=request.candidate_id
        )
        return {"message": "Vote recorded securely"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/status")
def vote_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_vote = db.query(Vote).filter(
        Vote.user_id == current_user.id
    ).first()

    return {"has_voted": bool(existing_vote)}