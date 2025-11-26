from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove
import io

app = FastAPI()

# CORS – allow frontend from anywhere (for now)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # production me domain specify kar sakta hai
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "message": "BG Remover API running"}

@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    input_bytes = await file.read()

    try:
        output_bytes = remove(input_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {e}")

    return StreamingResponse(
        io.BytesIO(output_bytes),
        media_type="image/png",
        headers={"Content-Disposition": 'inline; filename="output.png"'}
    )
