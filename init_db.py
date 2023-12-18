import sqlite3
from datetime import datetime

# Connect to SQLite database (or create it if not exists)
conn = sqlite3.connect('teenEdge.db')
cursor = conn.cursor()

# Create user_question_bank table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_question_bank (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        user_question TEXT,
        response TEXT,
        counter INTEGER,
        gender TEXT,
        age INTEGER,
        category TEXT, 
        social_activity TEXT,
        stistd TEXt,
        timestamp DATETIME
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and table created successfully.")
