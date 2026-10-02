# ============================================================
# PHISHING EMAIL DETECTOR
# Machine Learning model that classifies emails as phishing or safe
# Educational cybersecurity research project
# ============================================================

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
from pathlib import Path

# ------------------------------------------------------------
# Step 1: Setup paths
# ------------------------------------------------------------
project_root = Path(__file__).parent.parent
model_path = project_root / "data" / "phishing_model.pkl"

print("=" * 60)
print("  PHISHING EMAIL DETECTOR - Model Training")
print("=" * 60)

# ------------------------------------------------------------
# Step 2: Load a sample dataset
# For Phase 1, we use a small built-in sample
# (Phase 2 will load the real Kaggle dataset with 82,000 emails)
# ------------------------------------------------------------
print("\n[1/6] Loading sample dataset...")

emails = [
    # PHISHING examples (label = 1)
    "URGENT: Your account has been suspended. Click here to verify your identity immediately.",
    "Congratulations! You've won $1,000,000. Send us your bank details to claim your prize.",
    "Dear customer, your password expires in 24 hours. Reset it now at this link.",
    "Final notice: Your payment failed. Update your billing information immediately.",
    "Your package could not be delivered. Confirm your address at this link.",
    "SECURITY ALERT: Unusual login detected. Verify your account now or it will be locked.",
    "You have a pending refund. Claim it now before it expires.",
    "Confirm your identity to avoid account suspension. Click the link below.",
    "Your bank account needs verification. Login immediately to prevent closure.",
    "Exclusive offer: Update your payment info to continue your subscription.",
    
    # SAFE examples (label = 0)
    "Hey, are we still meeting for lunch tomorrow at 12?",
    "Please find the attached report for Q3. Let me know your thoughts.",
    "Reminder: Team meeting at 3 PM in the conference room.",
    "Happy birthday! Hope you have a wonderful day.",
    "Can you review the document I sent yesterday when you get a chance?",
    "The project deadline has been extended to next Friday.",
    "Thanks for your help on the presentation. It went really well.",
    "Let's catch up sometime next week for coffee.",
    "The invoice for last month has been processed successfully.",
    "I'll be out of office until Monday. Please contact Sarah for urgent matters.",
]

# Labels: 1 = phishing, 0 = safe
labels = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1,    # First 10 are phishing
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0]    # Next 10 are safe

print(f"     Loaded {len(emails)} sample emails")
print(f"     Phishing: {sum(labels)} | Safe: {len(labels) - sum(labels)}")

# ------------------------------------------------------------
# Step 3: Convert text to numbers using TF-IDF
# ML models can't read text — they need numbers
# ------------------------------------------------------------
print("\n[2/6] Converting text to numerical features (TF-IDF)...")

vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words='english',
    max_features=1000,
    ngram_range=(1, 2)  # Use single words AND two-word phrases
)

X = vectorizer.fit_transform(emails)
y = labels

print(f"     Created {X.shape[1]} features from {X.shape[0]} emails")

# ------------------------------------------------------------
# Step 4: Split into training (80%) and testing (20%)
# ------------------------------------------------------------
print("\n[3/6] Splitting data into train/test sets...")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"     Training set: {X_train.shape[0]} emails")
print(f"     Testing set:  {X_test.shape[0]} emails")

# ------------------------------------------------------------
# Step 5: Train TWO models and compare them
# ------------------------------------------------------------
print("\n[4/6] Training models...")

# Model 1: Naive Bayes (classic, fast, good for text)
print("     Training Naive Bayes...")
nb_model = MultinomialNB()
nb_model.fit(X_train, y_train)

# Model 2: Logistic Regression (often more accurate)
print("     Training Logistic Regression...")
lr_model = LogisticRegression(max_iter=1000, random_state=42)
lr_model.fit(X_train, y_train)

# ------------------------------------------------------------
# Step 6: Evaluate both models
# ------------------------------------------------------------
print("\n[5/6] Evaluating models on test data...")

nb_pred = nb_model.predict(X_test)
lr_pred = lr_model.predict(X_test)

nb_accuracy = accuracy_score(y_test, nb_pred)
lr_accuracy = accuracy_score(y_test, lr_pred)

print("\n" + "=" * 60)
print("  RESULTS")
print("=" * 60)
print(f"  Naive Bayes accuracy:       {nb_accuracy * 100:.2f}%")
print(f"  Logistic Regression accuracy: {lr_accuracy * 100:.2f}%")
print("=" * 60)

# Use the better model
if lr_accuracy >= nb_accuracy:
    best_model = lr_model
    best_name = "Logistic Regression"
    best_accuracy = lr_accuracy
else:
    best_model = nb_model
    best_name = "Naive Bayes"
    best_accuracy = nb_accuracy

print(f"\n  ✅ Best model: {best_name} ({best_accuracy * 100:.2f}% accuracy)")

# Show detailed report
print("\n" + "-" * 60)
print(f"  Detailed report for {best_name}:")
print("-" * 60)
best_pred = lr_pred if best_name == "Logistic Regression" else nb_pred
print(classification_report(y_test, best_pred, target_names=["Safe", "Phishing"]))

# ------------------------------------------------------------
# Step 7: Save the model for future use
# ------------------------------------------------------------
print("[6/6] Saving model...")

with open(model_path, "wb") as f:
    pickle.dump({"model": best_model, "vectorizer": vectorizer}, f)

print(f"     ✅ Model saved to: {model_path.name}")

# ------------------------------------------------------------
# Step 8: Interactive test — try it on a new email!
# ------------------------------------------------------------
print("\n" + "=" * 60)
print("  LIVE TEST — Predict new emails")
print("=" * 60)

test_emails = [
    "URGENT: Click this link to verify your bank account now",
    "Hey, can you send me the files when you get a chance?",
    "Your Apple ID has been locked. Verify immediately to restore access.",
    "Reminder: Dentist appointment tomorrow at 10 AM.",
]

for email in test_emails:
    features = vectorizer.transform([email])
    prediction = best_model.predict(features)[0]
    probability = best_model.predict_proba(features)[0]
    
    label = "🚨 PHISHING" if prediction == 1 else "✅ SAFE"
    confidence = max(probability) * 100
    
    print(f"\n  Email: \"{email[:60]}...\"" if len(email) > 60 else f"\n  Email: \"{email}\"")
    print(f"  Prediction: {label} ({confidence:.1f}% confidence)")

print("\n" + "=" * 60)
print("  Done! Model is ready.")
print("=" * 60)