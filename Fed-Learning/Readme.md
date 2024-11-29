```markdown
# 🚀 FastAPI Server and Client Setup  

This repository contains a **FastAPI server** and a corresponding **client** for interacting with the server. Follow the instructions below to get started.  

---

## 📂 File Structure  

- `main.py` - The FastAPI server script.  
- `client.py` - The Python client script for interacting with the server.  

---

## 🖥️ Requirements  

Ensure you have the following installed:  
- Python 3.7 or higher  
- `uvicorn`  
- `fastapi`  

You can install the necessary dependencies by running:  

```bash
pip install fastapi uvicorn
```

---

## 🚀 Starting the Server  

To start the FastAPI server, run the following command:  

```bash
uvicorn main:app --reload
```

### ⚙️ Server Details  

- **Default Host**: `127.0.0.1`  
- **Default Port**: `8000`  

You can access the interactive API docs at:  
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)  

---

## 🧪 Running the Client  

Once the server is running, execute the client script to interact with it:  

```bash
python3 client.py
```

The client script sends requests to the server and processes the responses.  

---

 
```
