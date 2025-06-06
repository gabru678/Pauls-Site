from flask import Flask, request, render_template
import smtplib
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('contact.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('Index.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    # Save to database
    conn = sqlite3.connect('contact.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO messages (name, email, message) VALUES (?, ?, ?)', (name, email, message))
    conn.commit()
    conn.close()

    # Send email notification
    send_email(name, email, message)

    return "Thank you for your message!"

def send_email(name, email, message):
    sender_email = "your_email@example.com"
    receiver_email = "your_email@example.com"
    password = "your_password"

    subject = f"New Contact Form Submission from {name}"
    body = f"Name: {name}\nEmail: {email}\nMessage: {message}"

    email_message = f"Subject: {subject}\n\n{body}"

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, email_message)

if __name__ == '__main__':
    app.run(debug=True)