from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import fasttext
import tensorflow as tf
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import uvicorn
from pydantic import BaseModel


class Input(BaseModel):
    Input: str


embed = fasttext.load_model('keyboard.bin')
model = tf.keras.models.load_model('word.keras')
words = embed.get_words()
word_vectors = np.array([embed.get_word_vector(word) for word in words])
app = FastAPI()


@app.post('/recommend')
async def recommend(input:  Input):
    Input1 = input.Input
    length = len(Input1.split(' '))
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


if __name__ == '__main__':
    uvicorn.run("client:app", host='0.0.0.0', port=8500)
