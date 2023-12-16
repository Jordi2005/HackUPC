import sqlite3
from datetime import datetime

# Connect to SQLite database
conn = sqlite3.connect('teenEdge.db')
cursor = conn.cursor()

# Sample data to insert
data_to_insert = {
    'question': 'Sample Question',
    'user_question': 'User\'s Question',
    'response': 'Sample Response',
    'counter': 1,
    'gender': 'Male',
    'age': 25,
    'category': 'General',
    'timestamp': datetime.now()
}

# Insert data into user_question_bank table
cursor.execute('''
    INSERT INTO user_question_bank (
        question, user_question, response, counter, gender, age, category, timestamp
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', (
    data_to_insert['question'],
    data_to_insert['user_question'],
    data_to_insert['response'],
    data_to_insert['counter'],
    data_to_insert['gender'],
    data_to_insert['age'],
    data_to_insert['category'],
    data_to_insert['timestamp']
))

# Commit the changes
conn.commit()

# Fetch and print data from user_question_bank table
cursor.execute('SELECT * FROM user_question_bank')
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the connection
conn.close()
