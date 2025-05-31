import csv
import hashlib


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_hashed_password, entered_password):
    hashed_entered = hash_password(entered_password)
    
    return hashed_entered == stored_hashed_password
