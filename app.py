# app.py
from flask import Flask, render_template, request, redirect,url_for
import openai
import sqlite3
import os
from flask_caching import Cache
from datetime import datetime
from tf_model import predict_image

from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# Set the upload folder
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

@app.route('/sti')
def sti():
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

    return render_template('sti.html', questions=rows)

@app.route('/sa')
def sa():
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

    return render_template('sa.html', questions=rows)

@app.route('/photo-gallery')
def photogallery():
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

    return render_template('photo.html', questions=rows)

@app.route('/about-us')
def aboutus():
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

    return render_template('about.html', questions=rows)

@app.route('/contact')
def contact():
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

    return render_template('contact.html', questions=rows)


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

        # Ensure that counter is not None before performing the addition
        counter = int(counter) + 1 

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

def generate_new_filename(original_filename):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    _, extension = os.path.splitext(original_filename)
    new_filename = f"{timestamp}{extension}"
    return new_filename


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        new_filename = generate_new_filename(file.filename)
        filename = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        file.save(filename)

        return redirect(url_for('show_image', filename=new_filename))

@app.route('/show/<filename>')
def show_image(filename):
    full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    label, score = predict_image(full_path)
    return render_template('show.html', filename=filename,label=label, score=score)

if __name__ == '__main__':
    app.run(debug=True)
