from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.candidate import Candidate
from app.models.user import User
from app.core.dependencies import get_current_user, get_db, require_admin
from app.schemas.candidate import CandidateCreate
router = APIRouter(prefix="/candidates", tags=["Candidates"])


@router.post("/")
def create_candidate(
    candidate: CandidateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    print("Candidate create triggered !!!")

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    new_candidate = Candidate(
        name=candidate.name,
        party=candidate.party
    )

    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)

    return new_candidate


@router.get("/")
def get_candidates(db: Session = Depends(get_db)):
    return db.query(Candidate).all()

@router.delete("/{candidate_id}")
def delete_candidate(
    candidate_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403)

    candidate = db.query(Candidate).get(candidate_id)
    db.delete(candidate)
    db.commit()
    return {"message": "Deleted"}


@router.put("/{candidate_id}")
def edit_candidate(
    candidate_id: int,
    request: CandidateCreate,
    db: Session = Depends(get_db),
    admin = Depends(require_admin)
):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    candidate.name = request.name
    candidate.party = request.party

    db.commit()
    db.refresh(candidate)

    return {
        "message": "Candidate updated successfully",
        "candidate": {
            "id": candidate.id,
            "name": candidate.name,
            "party": candidate.party
        }
    }