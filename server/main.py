from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp
import os

options = {
    "format": "best",
    "cookies": "/cookies.txt"
}

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello, FastAPI is working!"}
# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/download")
async def get_video_details(data: dict):
    url = data.get("url")
    
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")

    try:
        ydl_opts = {
            'format': 'best',
            'quiet': True
        }
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)

        video_details = {
            "title": info["title"],
            "thumbnail": info["thumbnail"],
            "download_url": info["url"]  
        }

        return {"success": True, "video": video_details}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching video: {str(e)}")
