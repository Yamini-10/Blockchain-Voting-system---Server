from sqlalchemy.orm import Session
from app.models.vote import Vote

def verify_blockchain(db: Session):

    votes = db.query(Vote).order_by(Vote.id).all()

    for i in range(1, len(votes)):
        if votes[i].previous_hash != votes[i-1].hash:
            return False

    return True