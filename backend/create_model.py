import pickle
from model_class import LogClassifier

model = LogClassifier()
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("model.pkl created successfully.")
