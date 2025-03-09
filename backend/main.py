from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
import tensorflow as tf  # type: ignore
import os
import threading
import requests  # type: ignore
import pickle
from .encryption import DPC
import uvicorn
app = FastAPI()
dpc = DPC()
model_update_lock = threading.Lock()

global_grad: dict[int, list[float]] = {}  # type: ignore


class Training(BaseModel):
    # id: str
    grad: dict


@app.post("/snd/embed")
def sender1():
    try:
        return FileResponse("keyboard.bin")
    except Exception as e:
        print(e)
        return JSONResponse({"message": "You aren't authorized!!",
                             "code": "-2"})


@app.post("/snd/model")
def sender2():
    try:
        return FileResponse("model.keras")
    except Exception as e:
        print(e)
        return JSONResponse({"message": "You aren't authorized!!",
                             "code": "-2"})


@app.get('/start')
async def reques():
    url = 'http://0.0.0.0:8500/train_and_upload/'
    payload = {
        'global_grad': global_grad
    }
    header = {
        'Content-Type': 'application/json'
    }
    try:
        await requests.post(url, headers=header, json=payload)
    except Exception as e:
        print(e)


@app.post("/update_weights/")
async def update_weights(file: UploadFile = File(...)):
    # Save the uploaded file temporarily
    file_location = f"temp/{file.filename}"
    os.makedirs("temp", exist_ok=True)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    # Load the incoming pickled model (model1.keras)
    try:
        with open(file_location, "rb") as f:
            new_model = pickle.load(f)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error loading pickled\
                            model: {e}")

    # Load the existing model (word.keras)
    try:
        old_model = tf.keras.Model.load_model("word.keras")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading\
                            base model: {e}")

    # Check that the two models have the same architecture
    if len(old_model.layers) != len(new_model.layers):
        raise HTTPException(status_code=400, detail="Model architectures\
                            do not match.")

    # Update weights and calculate gradient differences
    for layer_idx, (old_layer, new_layer) in enumerate(zip(old_model.layers,
                                                           new_model.layers)):
        # Ensure both layers are trainable and have weights
        if not old_layer.trainable or not new_layer.trainable:
            continue
        old_weights = old_layer.get_weights()
        new_weights = dpc.decrypt([new_layer.get_weights()])[0]

        # Check that the number of weights match
        if len(old_weights) != len(new_weights):
            raise HTTPException(status_code=400, detail=f"Mismatch in weights\
                                for layer {layer_idx}")

        # Update weights by adding new weights to old weights
        updated_weights = []
        grad_diffs = []
        for ow, nw in zip(old_weights, new_weights):
            updated_w = ow + nw  # Update weights by adding
            grad_diff = nw - ow  # Calculate the gradient difference
            updated_weights.append(updated_w)
            grad_diffs.append(grad_diff)
        # Set the updated weights back to the old model's layer
        old_layer.set_weights(updated_weights)
        # Store gradient differences in global_grad for each layer
        global_grad[layer_idx] = grad_diffs

    # Save the updated model as "word.keras"
    old_model.save("word.keras")

    # Remove the temporary file
    os.remove(file_location)

    return {"message": "Model weights updated successfully",
            "gradient_diffs": global_grad}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8500)
