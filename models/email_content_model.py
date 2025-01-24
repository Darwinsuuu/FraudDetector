import pandas as pd
import string
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report

# Step 1: Load the dataset
df = pd.read_csv('datasets/emails.csv')

# Step 2: Handle missing values and ensure correct labels
df.dropna(subset=['text', 'spam'], inplace=True)
df['spam'] = df['spam'].apply(lambda x: 'ham' if x == 0 else ('spam' if x == 1 else x))
df['spam'] = df['spam'].map({'ham': 0, 'spam': 1})

# Ensure no missing values in 'spam' column after encoding
assert df['spam'].isna().sum() == 0, "There are missing values in the 'spam' column after encoding."

# Step 3: Text Preprocessing
def preprocess_text(text):
    text = text.lower()  # Convert text to lowercase
    text = ''.join([char for char in text if char not in string.punctuation])  # Remove punctuation
    return text

# Apply preprocessing to the text column
df['text'] = df['text'].apply(preprocess_text)

# Step 4: Split data into training and testing sets
X = df['text']
y = df['spam']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Create a pipeline and train the model
model = make_pipeline(TfidfVectorizer(), LogisticRegression())

# Train the model
model.fit(X_train, y_train)

# Step 6: Evaluate the model
accuracy = model.score(X_test, y_test)
print(f'Model Accuracy: {accuracy:.4f}')

# Print classification report (Precision, Recall, F1-Score)
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Step 7: Save the model to a file
joblib.dump(model, 'email_content_model.pkl')

print("Model has been trained and saved as 'email_content_model.pkl'")