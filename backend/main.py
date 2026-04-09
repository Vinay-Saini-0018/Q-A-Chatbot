from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from backend.core.chains import answer_query

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for local development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Chatbot Backend is running!"}

@app.get("/files")
async def list_files():
    """
    Returns a list of all files in the 'data/' directory.
    """
    try:
        if not os.path.exists("data"):
            return {"files": []}
        files = [f for f in os.listdir("data") if os.path.isfile(os.path.join("data", f))]
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not list files: {str(e)}")

class Query(BaseModel):
    query: str
    file: str


# this will take the file from user and save to data folder
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Uploads a file and saves it to the 'data/' directory so it can be processed later.
    """
    try:
        os.makedirs("data", exist_ok=True)
        file_location = f"data/{file.filename}"
        
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
            
        return {"filename": file.filename, "message": "File uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not upload file: {str(e)}")

# this will answer question using the saved file
@app.post("/ask")
def ask_question(query_obj: Query):
    """
    Takes a query and a filepath, and returns the chatbot's answer based on the file content.
    """
    try:
        # answer_query expects the question text and the filepath
        answer = answer_query(query=query_obj.query, filepath=query_obj.file)
        
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))