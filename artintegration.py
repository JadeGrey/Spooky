import requestintegration
import requests
import json
import time
import uploadintegration
import discord
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()


async def run(interaction, prompt: str, nsfwp: str, typep: str, nsfw: str = False):
    await interaction.edit_original_response(content=f"Request recieved!")
    if nsfwp == 'y':
        nsfw = True
    rdata = await requestintegration.createPayload(prompt, nsfwp, typep)
    response = requests.request("POST", requestintegration.url, headers=requestintegration.headers, data=rdata)
    response.text
    data = response.json()

    if str(data["status"]) == "processing":
        pid = str(data["id"])
        await interaction.edit_original_response(content=f"Processing (ETA: {round(int(data['eta']))}s)")
        return await fetch(pid=pid, nsfw=nsfw)
    elif str(data["status"]) == "success":
        urlPath = str(data["output"]).replace("[", "").replace("'", "").replace("]", "")
        nsfwurl = ""
        # if nsfw == True:
        #     nsfwurl = "/nsfw"
        return f"{os.getenv('UPATH')}{nsfwurl}/{uploadintegration.send(urlPath, nsfw)}"
    else:
        await interaction.edit_original_response(content=f"Failed! Retrying in 5s.")
        return await failed(interaction, prompt, nsfwp, typep)

async def fetch(pid, nsfw):
    print("fetch attempt")
    url = "https://stablediffusionapi.com/api/v4/dreambooth/fetch"
    fetch_payload = json.dumps({
    "key": os.getenv("PKEY"),
    "request_id": str(pid)
    })

    fetch_headers = {
    'Content-Type': 'application/json'
    }

    fetch_response = requests.request("POST", url, headers=fetch_headers, data=fetch_payload)
    fetch_data = fetch_response.json()
    
    if str(fetch_data["status"]) == "processing":
        await asyncio.sleep(5)
        return await fetch(pid=pid, nsfw=nsfw)


    fetch_response.text
    urlPath = str(fetch_data["output"]).replace("[", "").replace("'", "").replace("]", "")
    nsfwurl = ""
    # if nsfw == True:
    #     nsfwurl = "/nsfw"
    return f"{os.getenv('UPATH')}{nsfwurl}/{uploadintegration.send(urlPath, nsfw)}"
    

async def failed(interaction, prompt, nsfwp, typep):
    if nsfwp == 'y':
        nsfw = True
    print("failed attempt")
    await asyncio.sleep(5)
    return await run(interaction, prompt, nsfwp, typep)