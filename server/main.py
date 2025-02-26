import requests
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
        if "youtube.com" in url or "youtu.be" in url:
            # Use yt-dlp for YouTube
            ydl_opts = {
                "format": "best",
                "quiet": True
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

            video_details = {
                "title": info.get("title", "No title"),
                "thumbnail": info.get("thumbnail", ""),
                "download_url": info.get("url", "")
            }

            return {"success": True, "platform": "YouTube", "video": video_details}
        
        elif "facebook.com" in url or "fb.watch" in url:
            # Use GetFvid API for Facebook
            api_url = f"https://getfvid.com/downloader?url={url}"
            response = requests.get(api_url)

            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to fetch Facebook video")

            video_info = response.json()
            return {"success": True, "platform": "Facebook", "video": video_info}

        else:
            raise HTTPException(status_code=400, detail="Unsupported platform")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
