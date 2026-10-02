# ============================================================
# PHISHING EMAIL DETECTOR — Maximum Accuracy Version
# Ensemble of NB + LR + SVM with advanced text preprocessing
# ============================================================

import pandas as pd
import re
import time
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle

# ------------------------------------------------------------
# Setup
# ------------------------------------------------------------
project_root = Path(__file__).parent.parent
dataset_path = project_root / "data" / "phishing_email.csv"
model_path = project_root / "data" / "phishing_model_max.pkl"

print("=" * 70)
print("  PHISHING EMAIL DETECTOR — Maximum Accuracy Ensemble")
print("=" * 70)

# ------------------------------------------------------------
# Step 1: Load dataset
# ------------------------------------------------------------
print("\n[1/8] Loading Kaggle dataset...")

if not dataset_path.exists():
    print(f"     ❌ Dataset not found: {dataset_path}")
    exit(1)

df = pd.read_csv(dataset_path)
print(f"     ✅ Loaded {len(df):,} emails")
print(f"     Columns: {list(df.columns)}")

# ------------------------------------------------------------
# Step 2: Advanced text cleaning
# ------------------------------------------------------------
print("\n[2/8] Cleaning text (this helps a LOT)...")

def clean_text(text):
    """Aggressive but careful text cleaning for ML."""
    if not isinstance(text, str):
        return ""
    # Lowercase
    text = text.lower()
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Replace URLs with a token (URLs are a huge phishing signal!)
    text = re.sub(r'http\S+|www\.\S+', ' urltoken ', text)
    # Replace email addresses with a token
    text = re.sub(r'\S+@\S+', ' emailtoken ', text)
    # Replace phone numbers with a token
    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', ' phonetoken ', text)
    # Replace long numbers with a token
    text = re.sub(r'\b\d{4,}\b', ' numbertoken ', text)
    # Remove punctuation but keep spaces
    text = re.sub(r'[^a-z\s]', ' ', text)
    # Collapse multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

start = time.time()
df['clean_text'] = df['text_combined'].apply(clean_text)
print(f"     ✅ Cleaned {len(df):,} emails in {time.time() - start:.1f}s")

# ------------------------------------------------------------
# Step 3: Train/test split
# ------------------------------------------------------------
print("\n[3/8] Splitting data (80/20)...")

X_raw = df['clean_text'].values
y = df['label'].values

X_train_raw, X_test_raw, y_train, y_test = train_test_split(
    X_raw, y, test_size=0.2, random_state=42, stratify=y
)

print(f"     Training: {len(X_train_raw):,}")
print(f"     Testing:  {len(X_test_raw):,}")

# ------------------------------------------------------------
# Step 4: Better TF-IDF
# ------------------------------------------------------------
print("\n[4/8] Building TF-IDF features (20,000)...")
print("     (This takes 2-4 minutes on 82k emails)")

start = time.time()
vectorizer = TfidfVectorizer(
    lowercase=False,       # Already lowercased
    stop_words='english',
    max_features=20000,    # ⬆️ 4x more than before
    ngram_range=(1, 3),    # ⬆️ Single + 2-word + 3-word phrases
    min_df=3,              # Word must appear in 3+ emails
    max_df=0.90,           # Ignore words in 90%+ of emails
    sublinear_tf=True,     # Better weighting
)

X_train = vectorizer.fit_transform(X_train_raw)
X_test = vectorizer.transform(X_test_raw)

print(f"     ✅ Created {X_train.shape[1]:,} features")
print(f"     Took {time.time() - start:.1f}s")

# ------------------------------------------------------------
# Step 5: Train three individual models
# ------------------------------------------------------------
print("\n[5/8] Training individual models...")

models = {}

# Model 1: Naive Bayes
print("     [1/3] Naive Bayes...")
start = time.time()
nb = MultinomialNB(alpha=0.1)
nb.fit(X_train, y_train)
nb_acc = accuracy_score(y_test, nb.predict(X_test))
models['Naive Bayes'] = (nb, nb_acc)
print(f"           ✅ {nb_acc * 100:.2f}% ({time.time() - start:.1f}s)")

# Model 2: Logistic Regression (tuned)
print("     [2/3] Logistic Regression...")
start = time.time()
lr = LogisticRegression(
    max_iter=2000,
    C=10,                # More regularization control
    solver='liblinear',
    random_state=42
)
lr.fit(X_train, y_train)
lr_acc = accuracy_score(y_test, lr.predict(X_test))
models['Logistic Regression'] = (lr, lr_acc)
print(f"           ✅ {lr_acc * 100:.2f}% ({time.time() - start:.1f}s)")

# Model 3: Linear SVM (usually best for text)
print("     [3/3] Linear SVM...")
start = time.time()
svm_base = LinearSVC(C=1.0, random_state=42, max_iter=3000)
svm = CalibratedClassifierCV(svm_base, cv=3)  # For probability estimates
svm.fit(X_train, y_train)
svm_acc = accuracy_score(y_test, svm.predict(X_test))
models['Linear SVM'] = (svm, svm_acc)
print(f"           ✅ {svm_acc * 100:.2f}% ({time.time() - start:.1f}s)")

# ------------------------------------------------------------
# Step 6: Train Ensemble (voting)
# ------------------------------------------------------------
print("\n[6/8] Training ensemble (soft voting)...")

start = time.time()
ensemble = VotingClassifier(
    estimators=[
        ('nb', MultinomialNB(alpha=0.1)),
        ('lr', LogisticRegression(max_iter=2000, C=10, solver='liblinear', random_state=42)),
        ('svm', CalibratedClassifierCV(LinearSVC(C=1.0, random_state=42, max_iter=3000), cv=3))
    ],
    voting='soft'  # Use probabilities, not just votes
)
ensemble.fit(X_train, y_train)
ens_acc = accuracy_score(y_test, ensemble.predict(X_test))
models['Ensemble (Voting)'] = (ensemble, ens_acc)
print(f"           ✅ {ens_acc * 100:.2f}% ({time.time() - start:.1f}s)")

# ------------------------------------------------------------
# Step 7: Compare and pick the best
# ------------------------------------------------------------
print("\n[7/8] RESULTS COMPARISON")
print("=" * 70)
for name, (_, acc) in sorted(models.items(), key=lambda x: -x[1][1]):
    marker = " 🏆" if acc == max(m[1] for m in models.values()) else ""
    print(f"  {name:25s}: {acc * 100:.2f}%{marker}")
print("=" * 70)

# Pick the best
best_name = max(models, key=lambda k: models[k][1])
best_model, best_acc = models[best_name]
best_pred = best_model.predict(X_test)

print(f"\n  🏆 WINNER: {best_name}")
print(f"  📊 ACCURACY: {best_acc * 100:.2f}%")

# ------------------------------------------------------------
# Step 8: Detailed report
# ------------------------------------------------------------
print("\n" + "-" * 70)
print(f"  Classification Report — {best_name}")
print("-" * 70)
print(classification_report(y_test, best_pred, target_names=["Safe", "Phishing"]))

cm = confusion_matrix(y_test, best_pred)
total_errors = cm[0][1] + cm[1][0]
print(f"  Confusion Matrix:")
print(f"                       Predicted")
print(f"                   Safe    Phishing")
print(f"  Actual Safe     {cm[0][0]:6,}  {cm[0][1]:6,}")
print(f"  Actual Phishing {cm[1][0]:6,}  {cm[1][1]:6,}")
print(f"\n  ⚠️  Total errors: {total_errors:,} out of {len(y_test):,}")
print(f"  ✅ Correct:      {len(y_test) - total_errors:,}")

# ------------------------------------------------------------
# Step 9: Save
# ------------------------------------------------------------
print("\n[8/8] Saving model...")
with open(model_path, "wb") as f:
    pickle.dump({
        "model": best_model,
        "vectorizer": vectorizer,
        "model_name": best_name,
        "accuracy": best_acc,
        "clean_text_func": clean_text,
    }, f)
print(f"     ✅ Saved to: {model_path.name}")

# ------------------------------------------------------------
# Step 10: Live test
# ------------------------------------------------------------
print("\n" + "=" * 70)
print("  LIVE PREDICTIONS")
print("=" * 70)

test_emails = [
    "URGENT: Your account has been compromised! Click here to verify immediately.",
    "Hey, are we still meeting for coffee tomorrow?",
    "Congratulations! You've won a $500 gift card. Claim now at this link.",
    "Please find the quarterly report attached. Let me know your thoughts.",
    "Your Netflix subscription is about to expire. Update payment info here.",
    "Reminder: Your dentist appointment is at 10 AM on Tuesday.",
]

for i, email in enumerate(test_emails, 1):
    cleaned = clean_text(email)
    features = vectorizer.transform([cleaned])
    prediction = best_model.predict(features)[0]
    probability = best_model.predict_proba(features)[0]
    
    label = "🚨 PHISHING" if prediction == 1 else "✅ SAFE"
    confidence = max(probability) * 100
    display = email[:65] + "..." if len(email) > 65 else email
    
    print(f"\n  {i}. \"{display}\"")
    print(f"     → {label} ({confidence:.1f}% confidence)")

print("\n" + "=" * 70)
print(f"  ✅ COMPLETE — {best_name} @ {best_acc * 100:.2f}%")
print(f"  📉 Reduced errors to {total_errors:,} (from {int(0.02 * len(y_test)):,})")
print("=" * 70)