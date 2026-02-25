# Blockchain Voting System – Backend

Secure voting backend built with **FastAPI**, JWT authentication, and blockchain-style vote hashing.

## Tech Stack

- FastAPI
- SQLAlchemy
- SQLite / PostgreSQL
- JWT Authentication
- Blockchain vote hashing
- Admin controls
- REST API

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
# Install dependencies
pip install -r requirements.txt
# Run server
uvicorn app.main:app --reload

# add env
DATABASE_URL=postgresql://postgres:Your_password@localhost:5432/voting_db
SECRET_KEY=supersecretproductionkey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
