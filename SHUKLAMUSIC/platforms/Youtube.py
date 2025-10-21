import asyncio
import os
import random
import json
import yt_dlp
import aiohttp
from typing import Union
from pyrogram.types import Message
from pyrogram.enums import MessageEntityType
from youtubesearchpython.__future__ import VideosSearch
from SHUKLAMUSIC.utils.formatters import time_to_seconds
from SHUKLAMUSIC.utils.database import is_on_off

API_KEY = "AIzaSyDXEUiyrUFyp-e7_CRFRCzkQ2n2qqPSsHE"
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


def cookie_txt_file():
    cookie_dir = os.path.join(os.getcwd(), "cookies")
    if not os.path.exists(cookie_dir):
        return None
    cookies_files = [f for f in os.listdir(cookie_dir) if f.endswith(".txt")]
    if not cookies_files:
        return None
    return os.path.join(cookie_dir, random.choice(cookies_files))


async def download_song(link: str):
    """
    Downloads audio of a YouTube video using yt-dlp.
    Returns local file path.
    """
    video_id = link.split("v=")[-1].split("&")[0]
    for ext in ["mp3", "m4a", "webm"]:
        path = os.path.join(DOWNLOAD_FOLDER, f"{video_id}.{ext}")
        if os.path.exists(path):
            return path

    cookie_file = cookie_txt_file()
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{DOWNLOAD_FOLDER}/%(id)s.%(ext)s",
        "quiet": True,
        "nocheckcertificate": True,
        "cookiefile": cookie_file if cookie_file else None,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=True)
        return os.path.join(DOWNLOAD_FOLDER, f"{info['id']}.mp3")


async def download_video(link: str):
    """
    Downloads video of a YouTube link using yt-dlp.
    Returns local file path.
    """
    video_id = link.split("v=")[-1].split("&")[0]
    for ext in ["mp4", "webm", "mkv"]:
        path = os.path.join(DOWNLOAD_FOLDER, f"{video_id}.{ext}")
        if os.path.exists(path):
            return path

    cookie_file = cookie_txt_file()
    ydl_opts = {
        "format": "(bestvideo[height<=720][width<=1280][ext=mp4])+bestaudio/best",
        "outtmpl": f"{DOWNLOAD_FOLDER}/%(id)s.%(ext)s",
        "quiet": True,
        "nocheckcertificate": True,
        "cookiefile": cookie_file if cookie_file else None,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=True)
        return os.path.join(DOWNLOAD_FOLDER, f"{info['id']}.{info['ext']}")


async def search_youtube(query: str):
    """
    Uses YouTube Data API to search a song/video and returns first video link.
    """
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults=1&q={query}&key={API_KEY}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            if "items" in data and data["items"]:
                video_id = data["items"][0]["id"]["videoId"]
                return f"https://www.youtube.com/watch?v={video_id}"
    return None


class YouTubeAPI:
    base = "https://www.youtube.com/watch?v="

    async def track(self, query: str):
        link = await search_youtube(query)
        if not link:
            return None
        results = VideosSearch(link, limit=1)
        result = (await results.next())["result"][0]
        return {
            "title": result["title"],
            "link": result["link"],
            "vidid": result["id"],
            "duration_min": result["duration"],
            "thumb": result["thumbnails"][0]["url"].split("?")[0],
        }

    async def download_audio(self, link: str):
        return await download_song(link)

    async def download_video(self, link: str):
        return await download_video(link)
