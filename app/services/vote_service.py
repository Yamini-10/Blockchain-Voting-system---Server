from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.vote import Vote
from app.models.user import User
from app.models.election import Election
from app.blockchain.blockchain import Block

def cast_vote(db: Session, user: User, candidate_id: int):

    # Check election status
    election = db.query(Election).first()
    if not election or not election.is_active:
        raise HTTPException(status_code=400, detail="Election is closed")

    # Double vote prevention
    existing_vote = db.query(Vote).filter(Vote.user_id == user.id).first()
    if existing_vote:
        raise HTTPException(status_code=400, detail="You have already voted")

    last_vote = db.query(Vote).order_by(Vote.id.desc()).first()
    previous_hash = last_vote.hash if last_vote else "0"

    block = Block(
        index=(last_vote.id + 1) if last_vote else 1,
        user_id=user.id,
        candidate_id=candidate_id,
        previous_hash=previous_hash
    )

    new_vote = Vote(
        user_id=user.id,
        candidate_id=candidate_id,
        hash=block.hash,
        previous_hash=previous_hash
    )

    db.add(new_vote)
    db.commit()

    return new_vote