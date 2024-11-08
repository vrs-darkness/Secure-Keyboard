from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
import fasttext
import tensorflow as tf
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import uvicorn
from format import Input, Train
from Coe.cosine import COE
from Distributed_paillier_cryptosystem.encryption import DPC
import pickle
import requests
import re
import pandas as pd

embed = fasttext.load_model('keyboard.bin')
model = tf.keras.models.load_model('word.keras')
words = embed.get_words()
dpc = DPC()
partial = dpc.split_private_key(1, 1)
word_vectors = np.array([embed.get_word_vector(word) for word in words])
app = FastAPI()
Store = {'Data': []}


def datasetmaker(data: dict):
    vocab = set()
    max_length = 3
    Data = {'X': [], 'Y': []}
    for i in data['Data']:
        info = re.sub(r'[!@#$%^&*()\-=_{}[\];:"\'<>,.?/|\\]', '', i)
        info = i.split(' ')
        for x in range(0, len(info)-max_length):
            Data['X'].append(" ".join(info[x:x+max_length]))
            Data['Y'].append(info[x+max_length])
            vocab = set.union(vocab, info[x:x+max_length+1])
    return Data


def datasetembeder(data: dict):
    Data_embed = {'X': [], 'Y': []}
    for i in range(len(data['X'])):
        Data_embed['X'].append(np.array([embed.get_word_vector(word) for word in embed.get_line(data['X'][i])[0]]))
        Data_embed['Y'].append(embed.get_sentence_vector(data['Y'][i]).reshape(1, -1))
    Data_embed['X'] = np.array(Data_embed['X'])
    Data_embed['Y'] = np.array(Data_embed['Y'])
    return Data_embed


@app.post('/recommend')
async def recommend(input:  Input):
    Input1 = input.Input
    length = len(Input1.split(' '))
    Store['Data'].append(Input1)
    print(Input1.split(" "))
    if (length > 6):
        print(length - 6)
        Stripped = Input1.split(" ")[length - 6:]
        print(Stripped)
        vector = np.array([embed.get_word_vector(i) for i in Stripped])
    else:
        vector = np.array([embed.get_word_vector(i) for i in Input1.split(" ")])
    result = model.predict(vector.reshape(-1, vector.shape[0], 200))
    cos_similarities = cosine_similarity([result.reshape(-1,)], word_vectors)
    top_3_indices = np.argsort(cos_similarities, axis=1)[0][::-1][:3]
    top_3_words = [words[index] for index in top_3_indices]
    payload = {'words': top_3_words}
    return JSONResponse(content=payload)


@app.post("/train_and_upload/")
async def train_and_upload(req: Train):
    # Load the model
    global_grad = req.global_grad
    try:
        model = tf.keras.models.load_model("model1.keras")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load model: {e}")
    # Prepare the dataset
    dataset = datasetmaker(Store)
    dataset = datasetembeder(dataset)
    X, Y = dataset['X'], dataset['Y']
    # Compile model
    model.compile(optimizer='adam', loss='mse')
    # Train the model for 3 epochs
    epochs = 3
    for epoch in range(epochs):
        # Predict and calculate loss
        predictions = model.predict(X)
        mse_loss = tf.keras.losses.MeanSquaredError()
        loss = mse_loss(Y, predictions)
        print(f"Epoch {epoch + 1}, Loss: {loss.numpy()}")

        # Apply COE if global_grad has entries
        if global_grad:
            for layer_idx, grad_diffs in global_grad.items():
                layer = model.layers[layer_idx]
                weights = layer.get_weights()
                modified_weights = [COE(weight) if i < len(grad_diffs) else weight for i, weight in enumerate(weights)]
                _ = dpc.ENCRYPT(modified_weights, partial)
                layer.set_weights(modified_weights)

        # Train for one epoch
        model.fit(X, Y, epochs=1, verbose=0)

    # Pickle the model
    with open("updated_model.pkl", "wb") as f:
        pickle.dump(model, f)

    # Send the pickled model to the update_weights endpoint
    with open("updated_model.pkl", "rb") as f:
        files = {'file': f}
        response = requests.post("http://127.0.0.1:8000/update_weights/", files=files)
    # Check response from the update_weights endpoint
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to update weights on the server")
    return {"message": "Model trained, pickled, and sent to the server successfully"}

if __name__ == '__main__':
    uvicorn.run("client:app", host='0.0.0.0', port=8500)
