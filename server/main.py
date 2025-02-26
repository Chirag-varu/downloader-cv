import yt_dlp
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

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
        # yt-dlp options
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

        return {"success": True, "platform": "Detected", "video": video_details}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching video: {str(e)}")
