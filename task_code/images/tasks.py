from celery import shared_task
from images.gpt_image_processor import request_img_desc
from requests import Response
from images.models import Image

@shared_task
def async_request_img_desc(base64_img_str:str) -> dict:
    response = request_img_desc(base64_img_str)
    return response

@shared_task
def process_image_and_create_obj(b64_img:str, img_file) -> Image:
    try:
        response = async_request_img_desc(b64_img)
        print(response.json())
        img_desc = response['choices'][0]['message']

        # Create an Image object and save it to the database
        image = Image.objects.create(img=img_file, desc=img_desc)
        return image
    except:
        raise Exception("There was an error while using gpt's image processing.")