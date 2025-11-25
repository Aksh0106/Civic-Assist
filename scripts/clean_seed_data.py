import pandas as pd
import re

def clean_text(text):
    if not text:
        return ""
    t = text.strip()
    t = re.sub(r"\s+", " ", t)  # remove extra spaces
    t = re.sub(r"[^\w\s.,]", "", t)  # remove symbols except punctuation
    return t

df = pd.read_csv("data/seed_data.csv")
df["text"] = df["text"].apply(clean_text)
df.to_csv("data/seed_data_cleaned.csv", index=False)

print("✅ Cleaned data saved to data/seed_data_cleaned.csv")
