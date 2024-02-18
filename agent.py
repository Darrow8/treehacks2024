from uagents import Agent, Context
from TikTokApi import TikTokApi
from yt_dlp import YoutubeDL
import asyncio
import os
import json
import urllib.request
from bs4 import BeautifulSoup
import youtube as yt

ydl_opts = {
    'outtmpl': 'videos/%(id)s.mp4',
}

ms_token = os.environ.get("ms_token", None) # get your own ms_token from your cookies on tiktok.com

alice = Agent(name="alice", seed="agent1qww3ju3h6kfcuqf54gkghvt2pqe8qp97a7nzm2vp8plfxflc0epzcjsv79t")
async def trending_videos():
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3,headless=False)
        async for video in api.trending.videos(count=1):
            print(video)

            with YoutubeDL(ydl_opts) as ydl:
                ydl.download(["https://www.tiktok.com/@" + video.author.username + "/video/" + video.id])

                yt.run(f"Test ${video.id}", f"videos/{video.id}.mp4")


@alice.on_event("startup")
async def say_hello(ctx: Context):
    
    ctx.logger.info(f'downloading tiktok file')

if __name__ == "__main__":
    # alice.run()
    asyncio.run(trending_videos())
