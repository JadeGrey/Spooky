import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://stablediffusionapi.com/api/v3/dreambooth"

async def createPayload(prompt: str, nsfwp: str, typep: str):
     
  if nsfwp.lower() == "y":
      nsfw = ", nsfw, 18+, missing clothes, both nipples)"
  else:
      nsfw = ", sfw)"
  payload = json.dumps({
    "key": os.getenv("PKEY"),
      "model_id": typep,
      "prompt": f"high quality (({prompt})) f/1.4, ISO 200, 1/160s, 8K, RAW, unedited, symmetrical balance, in-frame, 8K" + nsfw,
      "negative_prompt": "painting, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, deformed, ugly, blurry, bad anatomy, bad proportions, extra limbs, cloned face, skinny, glitchy, double torso, extra arms, extra hands, mangled fingers, missing lips, ugly face, distorted face, extra legs, anime",
      "width": "512",
      "height": "512",
      "samples": "1",
      "num_inference_steps": "30",
      "seed": None,
      "guidance_scale": 7.5,
      "webhook": None,
      "track_id": None
  })
  return payload

headers = {
  'Content-Type': 'application/json'
}