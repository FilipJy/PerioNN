from fastapi import FastAPI, Form
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = load_model('page5.2.h5')  


import pickle

with open('tokenizer_name.pickle', 'rb') as handle:
    tokenizer_name = pickle.load(handle)

with open('tokenizer_publisher.pickle', 'rb') as handle:
    tokenizer_publisher = pickle.load(handle)


correction_data = {
    "name": "",
    "year": 0,
    "issue": 0,
    "publisher": "",
    "predicted_pages": 0.0,
}

@app.post("/predict")
async def predict_pages(
    name: str = Form(...),
    year: int = Form(...),
    issue: int = Form(...),
    publisher: str = Form(...),
):
    try:
        
        name = str(name)
        publisher = str(publisher)

        name_seq = tokenizer_name.texts_to_sequences([name])
        publisher_seq = tokenizer_publisher.texts_to_sequences([publisher])

        max_sequence_length = 100
        name_seq_padded = pad_sequences(name_seq, maxlen=max_sequence_length)
        publisher_seq_padded = pad_sequences(publisher_seq, maxlen=max_sequence_length)

        
        input_data = np.concatenate((name_seq_padded, publisher_seq_padded, np.array([[issue]]), np.array([[year]])), axis=1)

        
        prediction = model.predict(input_data)

        
        correction_data["name"] = name
        correction_data["year"] = year
        correction_data["issue"] = issue
        correction_data["publisher"] = publisher
        correction_data["predicted_pages"] = prediction[0][0]

        return {"Predicted Pages": f'{prediction[0][0]:.2f}'}

    except Exception as e:
        return {"error": "Please enter valid input values."}

@app.post("/correct")
async def correct_and_retrain(corrected_pages: float = Form(...)):
    try:
        correction_data["corrected_pages"] = corrected_pages

        
        with open('corrections.csv', 'a') as f:
            f.write(f"{correction_data['name']},{correction_data['year']},{correction_data['issue']},{correction_data['publisher']},{correction_data['predicted_pages']},{correction_data['corrected_pages']}\n")

        return {"message": "Correction data has been saved. The model will be retrained with corrections."}

    except Exception as e:
        return {"error": "Please enter a valid corrected value."}
