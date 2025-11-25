import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib

# Load cleaned data
df = pd.read_csv("data/seed_data_cleaned.csv")

# Train department model
dept_model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", LogisticRegression())
])
dept_model.fit(df["text"], df["department"])
joblib.dump(dept_model, "models/department_model.pkl")

# Train category model
cat_model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", LogisticRegression())
])
cat_model.fit(df["text"], df["category"])
joblib.dump(cat_model, "models/category_model.pkl")

print("✅ Models trained and saved to models/ folder")
