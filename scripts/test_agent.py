import joblib

# Load models
dept_model = joblib.load("models/department_model.pkl")
cat_model = joblib.load("models/category_model.pkl")

# Sample complaint
sample_text = "There is a broken water pipe leaking near the school entrance."

# Predict
predicted_dept = dept_model.predict([sample_text])[0]
predicted_cat = cat_model.predict([sample_text])[0]

print("Complaint:", sample_text)
print("Predicted Department:", predicted_dept)
print("Predicted Category:", predicted_cat)
