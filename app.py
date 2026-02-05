from fastapi import FastAPI, UploadFile, File
import shutil
from agent import process_claim

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Synapx FNOL Agent running"}

@app.post("/process-claim")
async def process_claim_api(file: UploadFile = File(...)):
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return process_claim(file_path)
