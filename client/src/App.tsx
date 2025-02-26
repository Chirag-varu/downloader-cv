"use client";

import { useState } from "react";
import axios from "axios";
import { Download, Loader2, Video, Youtube } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { motion } from "framer-motion";

interface VideoDetails {
  thumbnail: string;
  title: string;
  download_url: string;
}

export default function App() {
  const [videoURL, setVideoURL] = useState("");
  const [videoDetails, setVideoDetails] = useState<VideoDetails | null>(null);
  const [status, setStatus] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const fetchVideoDetails = async () => {
    if (!videoURL.trim()) {
      setStatus("⚠️ Please enter a valid video URL!");
      return;
    }

    setIsLoading(true);
    setStatus("Fetching video details...");

    try {
      const response = await axios.post("http://localhost:5000/download", { url: videoURL }, {
        headers: { "Content-Type": "application/json" },
      });

      if (response.data.success) {
        setVideoDetails(response.data.video);
        setStatus("");
      } else {
        setStatus("Failed to fetch video details.");
      }
    } catch (error) {
      setStatus("Error fetching video details.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center h-screen w-full bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-500 flex-col p-6">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-lg"
      >
        <Card className="border-none shadow-xl bg-white/90 backdrop-blur-lg rounded-2xl">
          <CardHeader className="pb-4 text-center">
            <div className="flex justify-center mb-4">
              <div className="w-16 h-16 rounded-full bg-gradient-to-br from-indigo-600 to-purple-600 flex items-center justify-center shadow-md">
                <Video className="h-8 w-8 text-white" />
              </div>
            </div>
            <CardTitle className="text-3xl font-bold text-gray-800">Video Downloader</CardTitle>
            <CardDescription className="text-gray-600">Download YouTube & Facebook videos easily</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="relative">
              <Input
                type="text"
                placeholder="Paste YouTube or Facebook URL..."
                className="pr-12 border-2 border-gray-300 focus:border-indigo-500 h-12 rounded-lg text-gray-800 focus:ring-indigo-300"
                value={videoURL}
                onChange={(e) => setVideoURL(e.target.value)}
              />
              <Youtube className="absolute right-3 top-3 text-gray-500" size={24} />
            </div>

            <Button
              className="w-full h-12 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white font-semibold shadow-md rounded-lg transition-all duration-300"
              onClick={fetchVideoDetails}
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                  Processing...
                </>
              ) : (
                <>
                  <Video className="mr-2 h-5 w-5" />
                  Get Video
                </>
              )}
            </Button>

            {status && (
              <Alert variant={status.includes("⚠️") || status.includes("Error") ? "destructive" : "default"}>
                <AlertDescription>{status}</AlertDescription>
              </Alert>
            )}
          </CardContent>

          {videoDetails && (
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
              <CardContent className="pt-2">
                <div className="overflow-hidden rounded-lg shadow-lg">
                  <img
                    src={videoDetails.thumbnail || "/placeholder.svg"}
                    alt="Video thumbnail"
                    className="w-full h-auto object-cover transition-transform hover:scale-105 duration-300 rounded-lg"
                  />
                </div>
                <h3 className="mt-4 text-lg font-semibold text-gray-800 text-center line-clamp-2">
                  {videoDetails.title}
                </h3>
              </CardContent>
              <CardFooter>
                <a
                  href={videoDetails.download_url}
                  className="w-full"
                  download
                  target="_blank"
                  rel="noreferrer"
                >
                  <Button className="w-full bg-gradient-to-r from-green-500 to-teal-500 hover:from-green-600 hover:to-teal-600 text-white font-semibold shadow-md rounded-lg transition-all duration-300">
                    <Download className="mr-2 h-5 w-5" />
                    Download Video
                  </Button>
                </a>
              </CardFooter>
            </motion.div>
          )}
        </Card>
      </motion.div>

      <p className="text-white text-sm mt-6 opacity-80">© {new Date().getFullYear()} Video Downloader | Made with ❤️ by Chirag</p>
    </div>
  );
}
