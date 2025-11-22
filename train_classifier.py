import pandas as pd
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle

# Load dataset
df = pd.read_csv("train.csv")

X = df["text"]
y = df["label"]

vectorizer = TfidfVectorizer(stop_words="english")

# Convert text into numbers
X_vec = vectorizer.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)

# Naive Bayes model
model = MultinomialNB()

# Train the model
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model + vectorizer
with open("model.pkl", "wb") as f:
    pickle.dump((model, vectorizer), f)

print("Model saved as model.pkl")

