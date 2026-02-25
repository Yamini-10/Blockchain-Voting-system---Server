from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.vote import Vote
from app.models.candidate import Candidate
from app.models.user import User
from app.core.dependencies import get_db, get_current_user, require_admin
from app.models.election import Election
from app.services.blockchain_service import verify_blockchain
router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/analytics")
def get_analytics(
    db: Session = Depends(get_db),
   admin: User = Depends(require_admin)
):
    if admin.role != "admin":
        raise HTTPException(status_code=403)
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

    analytics = []
    for r in results:
        analytics.append({
            "id": r.id,
            "name": r.name,
            "party": r.party,
            "vote_count": r.vote_count
        })

    total_votes = db.query(func.count(Vote.id)).scalar()

    return {
        "total_votes": total_votes,
        "candidates": analytics
    }

# Reset election
@router.delete("/reset")
def reset_election(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403)

    db.query(Vote).delete()
    db.commit()

    return {"message": "Election Reset Successful"}

# Close Election
@router.post("/close")
def close_election(
    db: Session = Depends(get_db),
    admin = Depends(require_admin)
):
    election = db.query(Election).first()

    if not election:
        election = Election(is_active=False)
        db.add(election)
    else:
        election.is_active = False

    db.commit()
    return {"message": "Election closed"}


# Open Election
@router.post("/open")
def open_election(
    db: Session = Depends(get_db),
    admin = Depends(require_admin)
):
    election = db.query(Election).first()

    if not election:
        election = Election(is_active=True)
        db.add(election)
    else:
        election.is_active = True

    db.commit()
    return {"message": "Election opened"}


# Blockchain Integrity Check
@router.get("/verify")
def verify_chain(
    db: Session = Depends(get_db),
    admin = Depends(require_admin)
):
    is_valid = verify_blockchain(db)
    return {"blockchain_valid": is_valid}


# Winner Detection
@router.get("/winner")
def get_winner(
    db: Session = Depends(get_db),
    admin = Depends(require_admin)
):
    results = (
        db.query(
            Candidate.id,
            Candidate.name,
            func.count(Vote.id).label("vote_count")
        )
        .outerjoin(Vote, Candidate.id == Vote.candidate_id)
        .group_by(Candidate.id)
        .order_by(func.count(Vote.id).desc())
        .all()
    )

    if not results:
        return {"message": "No candidates"}

    winner = results[0]

    return {
        "winner": winner.name,
        "votes": winner.vote_count
    }

@router.get("/status")
def election_status(
    db: Session = Depends(get_db),
    admin = Depends(require_admin)
):
    election = db.query(Election).first()
    if not election:
        election = Election(is_active=False)
        db.add(election)
        db.commit()
        db.refresh(election)
    return {"is_active": election.is_active}