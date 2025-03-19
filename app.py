from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from openai import OpenAI
import os

app = FastAPI(title="Speech to Text API")

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "sk-ds-team-general-uRHEpM4v8JyZPznqvmSMT3BlbkFJPIMx3gi9v6BQOn58RbSN"))

@app.post("/transcribe")
async def speech_to_text(file: UploadFile = File(...)):
    """
    Convert speech audio to text using OpenAI's Whisper API
    """
    try:
        contents = await file.read()
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as f:
            f.write(contents)
        
        with open(temp_file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        
        os.remove(temp_file_path)
        
        return JSONResponse(content={
            "text": transcript.text,
            "status": "success"
        })
    
    except Exception as e:

        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
