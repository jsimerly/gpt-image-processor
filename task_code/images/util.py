from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
import base64
import os
import re
ALLOWED_EXTENSIONS = ['.jpeg', '.jpg', '.png', '.webp']

def convert_b64_to_img_file(b64_data:str) -> ContentFile:
    '''
        Converts an image file encoded in b64 string format to a binary image file so we can use it with our other methods.

        The reason we have this method is because if we need to recieve a base64 image from the client. While it will take more bandwidth, it may be necesarry or easier to implement in some cases.
    '''
    if b64_data is None:
        raise ValueError('convert_to_img_file must include the parameter b64_data')
    
    if not isinstance(b64_data, str):
         raise ValueError('the base64 data is expected to be a string.')
    
    #this block is used to split the image data and the formatting data like the extension
    try:
        format, imgstr = b64_data.split(';base64,')
        ext = format.split('/')[-1]
        decoded_img = base64.b64decode(imgstr)
    except ValueError:
        raise ValueError("Invalid base64 data.")
    except Exception as e:
        raise ValueError(f"An error occurred while decoding base64 data: {e}")

    try:
        img = Image.open(BytesIO(decoded_img))
    except IOError:
        raise ValueError("Failed to open the image. The provided data may not be an image.")

    buffer = BytesIO()

    #I am not compressing the images at all as they're going to be used by AIs to analyize the image.
    try:
            if ext.lower() in ['jpeg', 'jpg']:
                img.save(buffer, format="JPEG", quality=100)
            elif ext.lower() == 'png':
                img.save(buffer, format="PNG", compress_level=0)
            else:
                raise ValueError("Unsupported file extension. Only JPEG and PNG are supported.")
    except Exception as e:
        raise ValueError(f"An error occurred while processing the image: {e}")
    
    img_compressed = buffer.getvalue()
    
    return ContentFile(img_compressed, name='temp' + ext)

def convert_binary_file_to_base64(image_file) -> str:
    '''
        Used to convert a image file to base64. Base64 will be easier to use with external apis as it is compatable with JSON. 
        
        If the extra bandwidth because a concern, it may be worth exploring other external image processors that can take form requests in addition to JSON or do more client side pre-processing.
    '''
    try:
        with Image.open(image_file) as image:
            # Convert image to RGB if it's not already in that mode
            if image.mode != 'RGB':
                image = image.convert('RGB')

            buffer = BytesIO()
            image.save(buffer, format='JPEG')
            img_base64 = base64.b64encode(buffer.getvalue())

            # Properly format the base64 string for data URI schema
            return f"data:image/jpeg;base64,{img_base64.decode('utf-8')}"

    except Exception as e:
        raise ValueError(f"An error occurred while processing the image: {e}")


def is_base64(string):
    if not re.match(r'^data:image\/', string):
        return False

    try:
        base64_data = string.split(';base64,')[1]
    except IndexError:
        return False
    try:
        decoded_data = base64.b64decode(base64_data)
    except (base64.binascii.Error, ValueError):
        return False
    
    try:
        Image.open(BytesIO(decoded_data))
    except IOError:
        return False
    return True

def is_img_file(file):
    try:
        with Image.open(file) as img:
            is_img = True if img.format else False
            return is_img
        
    except IOError:
        return False

def get_file_extension(image_file) -> str:
        _, file_extension = os.path.splitext(image_file.name)
        file_extension = file_extension.lower()
        return file_extension

def is_allowed_extension(image_file) -> bool:
    ext = get_file_extension(image_file)
    return ext in ALLOWED_EXTENSIONS
         