"""
Original file from: https://github.com/Sven-Bo/streamlit-sales-dashboard-with-userauthentication/tree/master

This script is to generate hashed password from the list of passwords below. For security purposes, the strings
in the list is replaced by 'XXX' when this was pushed to repo.
"""

import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ["John Smith", "Satoshi Nakamoto"]
usernames = ["jsmith", "snakamoto"]
passwords = ["XXX", "XXX"]

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)