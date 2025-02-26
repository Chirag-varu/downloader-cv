import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Hello, FastAPI is working!"}

@app.post("/download")
async def get_video_details(data: dict):
    url = data.get("url")
    
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")

    try:
        ydl_opts = {
            "format": "best",
            "quiet": True,
            "cookiefile": "cookies.txt"  # Use your saved cookies
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        video_details = {
            "title": info.get("title", "No title"),
            "thumbnail": info.get("thumbnail", ""),
            "download_url": info.get("url", "")
        }

        return {"success": True, "video": video_details}
    
    except Exception as e:
        print(f"Error: {str(e)}")  # Log the error
        raise HTTPException(status_code=500, detail=f"Error fetching video: {str(e)}")
