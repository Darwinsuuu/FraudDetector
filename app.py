from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import mysql.connector
from mysql.connector import Error
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import os
from flask_cors import CORS
from io import BytesIO
import xlsxwriter
from email.mime.base import MIMEBase
from email import encoders

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Secret key for sessions (important for security)
app.secret_key = os.urandom(24)

# Load and train the model
dataset = pd.read_csv('datasets/emails.csv')  # Make sure the 'emails.csv' is present in your project folder
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(dataset['text'])
X_train, X_test, y_train, y_test = train_test_split(X, dataset['spam'], test_size=0.2, random_state=42)
model = MultinomialNB()
model.fit(X_train, y_train)

# Predict the test set labels
y_pred = model.predict(X_test)

# Calculate Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(cm)

# Classification Report
report = classification_report(y_test, y_pred)
print("Classification Report:")
print(report)

# Email sending configuration
SMTP_SERVER = 'smtp.gmail.com'  # Example: Gmail SMTP server
SMTP_PORT = 587
EMAIL_ADDRESS = 'emailphishing12@gmail.com'  # Replace with your email
EMAIL_PASSWORD = 'xoot xlqk kcgm bbof'  # Replace with your email password

# Function to predict message
def predict_message(message):
    message_vector = vectorizer.transform([message])
    prediction = model.predict(message_vector)
    return 'Spam' if prediction[0] == 1 else 'Ham'

# Function to connect db
def open_db_connection():
    """Open a connection to the MySQL database."""
    try:
        # Establish connection to the database
        db_connection = mysql.connector.connect(
            host="localhost",        # Change to your MySQL host (e.g., 'localhost' or IP address)
            user="root",    # Your MySQL username
            password="",  # Your MySQL password
            database="fraud_detector_db" # The name of the database to connect to
        )
        if db_connection.is_connected():
            print("Successfully connected to the database")
        return db_connection

    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

# Function to close the DB connection
def close_db_connection(db_connection):
    if db_connection.is_connected():
        db_connection.close()
        print("Database connection closed.")

# Function to send email
def send_email(to_email, subject, body):
    try:
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        # Connect to the SMTP server and send the email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure connection
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        server.quit()

        print("Email sent successfully.")

    except Exception as e:
        print("Failed to send email:", e)

# Define the API endpoint
@app.route('/api/spam_detector', methods=['POST'])
def classify_email():
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Debug: Print received data
        print("Received data:", data)

        # Check if 'email_content' is present in the request data
        if 'email_content' not in data:
            return jsonify({'error': 'Missing "email_content" field in the request'}), 400

        email_address = data.get('email_address', '')
        message = data['email_content']

        # Get prediction result
        result = predict_message(message)
        is_spam = 1 if result == 'Spam' else 0

        # Prepare the response
        response = {
            'result': result,
            'email_address': email_address
        }

        # Insert into database
        db_connection = open_db_connection()
        if db_connection:
            cursor = db_connection.cursor()
            insert_query = """INSERT INTO emails (email_address, email_content, isSpam)
                              VALUES (%s, %s, %s)"""
            cursor.execute(insert_query, (email_address, message, is_spam))
            db_connection.commit()
            close_db_connection(db_connection)

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/get_otp', methods=['GET'])
def get_otp():
    try:
        OTP = str(random.randint(100000, 999999))

        # Checks if OTP is present in the db
        db_connection = open_db_connection()
        if db_connection:
            cursor = db_connection.cursor()

            # Query to check for an active (non-expired) OTP
            select_query = """
                SELECT *
                FROM login
                WHERE date_created = (SELECT MAX(date_created) FROM login)
                AND date_expiry > NOW();
            """
            cursor.execute(select_query)
            result = cursor.fetchone()

            if result:
                OTP = result[1]  # Assuming OTP is at index 1 in the result
                print('Active OTP:', OTP)
            else:
                insert_query = """
                    INSERT INTO login (login_code, date_expiry)
                    VALUES (%s, DATE_ADD(NOW(), INTERVAL 5 MINUTE))
                """
                cursor.execute(insert_query, (OTP,))
                print('New OTP inserted:', OTP)

            db_connection.commit()

        # Prepare email content
        recipient = EMAIL_ADDRESS
        subject = f'FraudDetector OTP Code [{OTP}]'
        body = f"""
                    <div style="font-family: Arial, sans-serif; color: #333; margin: 0; padding: 0;">
                        <div style="max-width: 500px; margin: 20px auto; background: #fff; border-radius: 8px; border: 1px solid #ddd;">
                            <div style="background-color: #007bff; color: #fff; padding: 20px; text-align: center;">
                                <h1 style="margin: 0;">Fraud Detector</h1>
                            </div>
                            <div style="padding: 20px; text-align: left;">
                                <strong>Hello Administrator!</strong>
                                <br>
                                <p>Your OTP is:</p>
                                <p style="width: 100%; max-width: 400px; margin: 20px auto; background: #DEDEDE; border-radius: 5px; text-align: center; padding: 20px 0; font-size: 36px; letter-spacing: 18px;">
                                    {OTP}
                                </p>
                                <br>
                                <p style="line-height: 1.5;">
                                    <strong>Do not share your OTP code with anyone.</strong> If someone else obtains your OTP, they could potentially access your account, compromising your personal or sensitive information.
                                </p>
                                <br>
                                <p><strong>NOTE:</strong> The OTP is valid only for <strong>5 minutes</strong>.</p>
                            </div>
                            <div style="background-color: #f4f4f4; text-align: center; padding: 10px; font-size: 12px; color: #888;">
                                <p style="margin: 0;">If you did not request this OTP, please ignore this email.</p>
                            </div>
                        </div>
                    </div>
                """

        # Send email
        send_email(recipient, subject, body)

        return jsonify({'status': 'success', 'message': 'OTP sent successfully'})

    except Exception as e:
        print("Error occurred:", e)
        return jsonify({'status': 'error', 'message': 'Something went wrong. Error: ' + str(e)}), 500



@app.route('/api/email_data', methods=['GET'])
def fetch_email_data():
    try:
        # Open a connection to the database
        db_connection = open_db_connection()
        if db_connection:
            cursor = db_connection.cursor(dictionary=True)

            # SQL query to fetch data from the `emails` table
            query = """
                SELECT 
                    email_address AS email, 
                    email_content AS content, 
                    isSpam AS spam, 
                    date_created 
                FROM 
                    emails
            """
            cursor.execute(query)
            emails = cursor.fetchall()

            # Close the database connection
            close_db_connection(db_connection)

            # Return the data as JSON
            return jsonify(emails), 200

    except Exception as e:
        print("Error occurred while fetching email data:", e)
        return jsonify({'error': 'Failed to fetch email data', 'message': str(e)}), 500


# Sample route for login
@app.route('/api/login_creds', methods=['POST'])
def login():
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Check if required fields are present in the request data
        if 'username' not in data or 'otp' not in data:
            return jsonify({'error': 'Missing "username" or "otp" field in the request'}), 400

        username = data['username']
        otp = data['otp']

        # Check if the username is correct
        if username != 'fraudadmin':
            return jsonify({'error': 'Invalid username'}), 200

        # Open a connection to the database
        db_connection = open_db_connection()
        if db_connection:
            cursor = db_connection.cursor()

            # Query to check if the OTP is correct and not expired
            select_query = """
                SELECT * FROM login
                WHERE login_code = %s
                AND date_expiry > NOW();
            """
            cursor.execute(select_query, (otp,))
            result = cursor.fetchone()

            if result:
                # Set session to indicate user is logged in
                session['logged_in'] = True
                return jsonify({'status': 'success', 'message': 'Login successful'}), 200
            else:
                return jsonify({'error': 'Invalid or expired OTP'}), 200

        # Close the DB connection
        close_db_connection(db_connection)

    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/api/send_report', methods=['POST'])
def send_report():
    try:
        # Fetch email data from the database
        db_connection = open_db_connection()
        if db_connection:
            query = """
                SELECT 
                    email_address AS Email, 
                    email_content AS Content, 
                    IF(isSpam = 1, 'Spam', 'Not Spam') AS Spam, 
                    date_created AS DateCreated
                FROM 
                    emails
            """
            df = pd.read_sql(query, db_connection)
            close_db_connection(db_connection)

            # Convert the dataframe to an Excel file in memory
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Email Report')

            output.seek(0)  # Reset pointer to the start of the file

            # Email Configuration
            recipient = EMAIL_ADDRESS
            subject = "Fraud Detector Report"
            body = """
                <p>Hello,</p>
                <p>Please find the attached report generated by the Fraud Detector system.</p>
                <p>Best Regards,<br>Fraud Detector Team</p>
            """

            # Create the email message
            msg = MIMEMultipart()
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html'))

            # Attach the Excel file
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(output.read())
            encoders.encode_base64(attachment)
            attachment.add_header(
                'Content-Disposition', 
                'attachment', 
                filename='Fraud_Detector_Report.xlsx'
            )
            msg.attach(attachment)

            # Send the email
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()

            return jsonify({'status': 'success', 'message': 'Report sent successfully to the authorities.'}), 200

        return jsonify({'status': 'error', 'message': 'Failed to connect to the database.'}), 500

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'status': 'error', 'message': f"Failed to send report. Error: {e}"}), 500



@app.route('/dashboard')
def dashboardPage():
    # Check if user is logged in
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('loginPage'))  # Redirect to login page if not logged in
    
    # If logged in, render the dashboard page
    return render_template('admin.html')


@app.route('/login')
def loginPage():
    return render_template('login.html')


@app.route('/api/logout')
def logout():
    # Clear the session and log out the user
    session.clear()
    return jsonify({'status': 'success', 'message': 'Logged out successfully'}), 200


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
    # app.run(debug=True)
