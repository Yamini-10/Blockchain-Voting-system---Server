import hashlib
import time

class Block:
    def __init__(self, index, user_id, candidate_id, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.user_id = user_id
        self.candidate_id = candidate_id
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        raw = f"{self.index}{self.timestamp}{self.user_id}{self.candidate_id}{self.previous_hash}"
        return hashlib.sha256(raw.encode()).hexdigest()