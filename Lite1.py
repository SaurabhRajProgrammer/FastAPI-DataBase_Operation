import sqlite3
from fastapi import FastAPI

app=FastAPI()

conn = sqlite3.connect("store.db",check_same_thread=False)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY,
        title TEXT,
        completed TEXT
        )

""")

conn.commit()

@app.get("/")
def home():
    return {
        "message":"SQLite connected fine"
    }