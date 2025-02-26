import yt_dlp
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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

    # Choose correct cookie file based on the URL
    if "youtube.com" in url or "youtu.be" in url:
        cookie_file = "cookies.txt"  # YouTube cookies
    elif "facebook.com" in url or "fb.watch" in url:
        cookie_file = "cookiefb.txt"  # Facebook cookies
    else:
        cookie_file = None  # No cookies for other platforms

    try:
        ydl_opts = {
            "format": "best",
            "quiet": True,
        }

        # Add cookies if available
        if cookie_file:
            ydl_opts["cookiefile"] = cookie_file
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        video_details = {
            "title": info.get("title", "No title"),
            "thumbnail": info.get("thumbnail", ""),
            "download_url": info.get("url", "")
        }

        return {"success": True, "video": video_details}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching video: {str(e)}")
