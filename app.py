# app.py
from flask import Flask, render_template, request
import openai
import sqlite3
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    # Connect to SQLite database
    conn = sqlite3.connect('teenEdge.db')
    cursor = conn.cursor()

    # Select top 6 questions based on counter
    cursor.execute('''
        SELECT * FROM user_question_bank
        ORDER BY counter DESC
        LIMIT 6
    ''')

    # Fetch and print the result
    rows = cursor.fetchall()

    return render_template('index.html', questions=rows)

@app.route('/app')
def appindex():
    # Connect to SQLite database
    conn = sqlite3.connect('teenEdge.db')
    cursor = conn.cursor()

    # Select top 6 questions based on counter
    cursor.execute('''
        SELECT * FROM user_question_bank
        ORDER BY counter DESC
        LIMIT 6
    ''')

    # Fetch and print the result
    rows = cursor.fetchall()

    return render_template('app.index.html', questions=rows)


def insert_data_to_db(gender, age, category, response_content, user_message):
    conn = sqlite3.connect('teenEdge.db') 
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO user_question_bank ( user_question, response, counter, gender, age, category)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_message, response_content, 1, gender, age, category))

    conn.commit()
    conn.close()

def check_user_message_in_db(user_message):
    conn = sqlite3.connect('teenEdge.db') 
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, counter, response
        FROM user_question_bank
        WHERE user_question = ?;
    ''', (user_message,))

    result = cursor.fetchone()

    if result:
        # If user_message exists, update the counter and get the response
        record_id, counter, response = result
        print(record_id)
        # Ensure that counter is not None before performing the addition
        counter = int(counter) + 1 
        print(counter)
        cursor.execute('''
            UPDATE user_question_bank
            SET counter = ?
            WHERE id = ?;
        ''', (counter, record_id))
    conn.commit()
    conn.close()

    return response if result else None


@app.route('/chat', methods=['POST'])
def chat():
    

    openai.api_key = os.environ.get("OPENAI_API_KEY")
    openai.api_key = "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"
    # Initialize messages with system context
    messages = [{"role": "system", "content": "Eres un asistente muy útil."}]

    # Retrieve user's message from the form
    user_message = request.form['user_message']

    gender = request.form['gender']
    age = request.form['age']
    category = request.form['category']

    # Append user's message to the messages list
    messages.append({"role": "user", "content": user_message})

    try:
        # Check if the user_message already exists in the database
        response_content = check_user_message_in_db(user_message)

        if not response_content:
            # If the response is not found in the database, call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-1106",
                messages=messages
            )

            # Extract the response content from the API response
            response_content = response.choices[0].message.content

            # Insert data into the database
                            
            insert_data_to_db(gender, age, category, response_content, user_message)

            # Return the assistant's response
        return response_content

    except openai.error.OpenAIError as e:
        # Handle OpenAI API errors
        return f"Error al llamar a la API de OpenAI: {e}"

if __name__ == '__main__':
    app.run(debug=True)
