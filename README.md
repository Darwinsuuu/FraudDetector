# Fraud Detector

A machine learning-based fraud detection system designed to identify fraudulent activities in various types of transactions.

## Features

- Detects fraudulent transactions using machine learning algorithms.
- Supports various data preprocessing techniques to enhance model performance.
- Easy integration with existing systems and APIs for real-time fraud detection.
 
<br>

# How to run app locally
Follow these steps to set up and run the FraudDetector app on your local machine.


### 1. Download and Install Git
You will need Git installed on your machine to clone the repository. 

- **Download Git** from [https://git-scm.com/downloads](https://git-scm.com/downloads).
- Follow the installation instructions for your operating system.

### 2. Clone the Repository

Once Git is installed, open your terminal or command prompt and run the following command to clone the repository:

```bash
git clone https://github.com/Darwinsuuu/FraudDetector.git
```

This will download the project files to your local machine.


### 3. Go to the Project Directory
Navigate to the directory where the repository was cloned. For example:

```bash
cd C://User/Documents/FraudDetector
```
Replace this path with the correct location of the FraudDetector folder on your machine.


### 4. Create a Virtual Environment
It’s recommended to use a virtual environment for managing dependencies. Run the following command to create a virtual environment:
```bash
python -m venv myenv
```
This will create a virtual environment named myenv in your project directory.


### 5. Activate the Virtual Environment
Activate the virtual environment using the following command:
- On Windows
```bash
.\myenv\Scripts\activate
```
- On Mac/Linux
```bash
source myenv/bin/activate
```
Your terminal should now show that the virtual environment is active (typically, you will see (myenv) before the command prompt).

### 6. Install Required Packages
Once the virtual environment is activated, install the necessary Python packages listed in the requirements.txt file:
```bash
pip install -r requirements.txt
```

### 7. Once packages install you have to download XAMPP <a href="https://sourceforge.net/projects/xampp/files/XAMPP%20Windows/8.0.30/xampp-windows-x64-8.0.30-0-VS16-installer.exe">here</a>.

### 8. Import database in phpMyAdmin
Follow this <a href="https://www.youtube.com/watch?v=2ynKAAt1G4Y">youtube tutorial</a> on how to import database to phpMyAdmin<br>
<strong>Note</strong>: Make sure to name the database to fraud_detector_db to prevent issues.


### 7. Run the Application
After installing the dependencies and importing the database you can start the application by running command in terminal:
```bash
python app.py
```
The Flask app will run on http://127.0.0.1:5000/ by default, and you can access it through your web browser.



<br>

# Troubleshooting
- If you encounter any issues related to missing dependencies, ensure you have activated the virtual environment and installed all required packages.
- If you face any issues with the application, make sure you have the correct Python version installed (Python 3.x recommended).

<br>


# Technologies

### Frontend:
- **jQuery**: Simplifies HTML manipulation, event handling, and AJAX.
- **Bootstrap**: A CSS framework for building responsive, mobile-first layouts.
- **SweetAlert**: Customizable popup boxes for alerts and confirmations.
- **Ajax**: Allows asynchronous data fetching for smoother user experience.
- **Boxicons**: A library of vector icons for enhancing UI elements.

### Backend:
- **Flask**: Web framework for building the API.
- **Pandas**: Data manipulation and analysis.
- **scikit-learn**: Machine learning (CountVectorizer, Naive Bayes).
- **MySQL Connector**: MySQL database interaction.
- **smtplib**: Sending emails for notifications.
- **xlsxwriter**: Writing Excel files.
- **Flask CORS**: Handling cross-origin resource sharing.
- **email.mime**: Handling email MIME types for attachments.

### Database
- **MySQL**: Relational database management system (RDBMS) that uses structured query language (SQL) to store and manage data.
