import requests
import os
from dotenv import load_dotenv
from io import BytesIO
import random

load_dotenv()

def send(file, nsfw):
    def isNsfw():
        if nsfw == 'y':
            return True
        return False
    params = {
    "key": os.getenv("UKEY"),
    "nsfw": isNsfw()
}
    print(file)
    upload_url = os.getenv("UURL")
    response = requests.get(file)
    file_object = BytesIO(response.content)

    file_name = f'{str(random.randint(0, 999999))}.png'
    files = {'file': (file_name, file_object)}
    response = requests.post(upload_url, files=files, params=params)

    print('Response:', response.text)
    return file_name

