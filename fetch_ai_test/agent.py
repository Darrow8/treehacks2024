from uagents import Agent, Context
from TikTokApi import TikTokApi
from yt_dlp import YoutubeDL
import asyncio
import os
import json
import urllib.request
from bs4 import BeautifulSoup

ydl_opts = {
    'outtmpl': 'videos/%(id)s',
}

ms_token = os.environ.get("ms_token", None) # get your own ms_token from your cookies on tiktok.com

alice = Agent(name="alice", seed="agent1qww3ju3h6kfcuqf54gkghvt2pqe8qp97a7nzm2vp8plfxflc0epzcjsv79t")
async def trending_videos():
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3,headless=False)
        async for video in api.trending.videos(count=1):
            print(video)

            # urllib.request.urlretrieve(video.as_dict[], 'test.mp4') 
            # print(video.as_dict)
            # saveFile(video.as_dict)
        
async def movie_videos():
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, 
                                  headless=False, suppress_resource_load_types=["image", "media", "font", "stylesheet"])


        async for video in api.search.videos("movies"):
            # print("username: " + video.author.username)
            # print("video id: " + video.id)
            # print("stats: " + str(video.stats))

            with YoutubeDL(ydl_opts) as ydl:
                ydl.download(["https://www.tiktok.com/@" + video.author.username + "/video/" + video.id])



@alice.on_event("startup")
async def say_hello(ctx: Context):
    
    ctx.logger.info(f'hello, my name is {ctx.name}')

@alice.on_interval(period=2.0)
async def say_hello(ctx: Context):
    ctx.logger.info(f'Nice to meet you!')
    

# contents = urllib.request.urlopen("https://www.tiktok.com/search?q=movies").read()



# # print(contents)
# soup = BeautifulSoup(contents)
# print(soup.prettify())
# # data-e2e="search_top-item-list"
# target_div = soup.find(attrs={"data-e2e": "search_top-item-list"})

# print(target_div)
# with open('save.html','w') as f:
#     f.write(soup.prettify())

# if __name__ == "__main__":
    # alice.run()
    # asyncio.run(movie_videos())
