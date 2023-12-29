import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ['OPENAI_API_KEY']


#more info here: https://platform.openai.com/docs/guides/vision
def img_desc_payload(base64_img_str:str) -> dict:
    return {
        "model": "gpt-4-vision-preview", 
        "messages": [
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": "Give a description of this image."
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_img_str}"
                }
                }
            ]
            }
        ],

        "max_tokens": 1065 
        # 765 + 300; 765 being the token cost of an 800x800 image. 300 being the max tokens for the output. We could create this number dynamically based on image size, but may also make sense to standardize image sizes instead. This will potentially provide worse descriptions but limit cost.
    }


def openai_request(payload:dict) -> requests.Response:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers=headers,
        json=payload,
    )
    return response

def request_img_desc(base64_img_str:str) -> requests.Response:
    payload = img_desc_payload(base64_img_str)
    response = openai_request(payload)
    return response

