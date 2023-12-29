# Edlight Take Home Task
This django project was set up as a take home task to showcase my skill using Django, API development, and general web development practices. In the codebase you'll find a RESTful API, external API connections, and more!

This project was completed by Jacob Simerly.

## Features
- **Analyze Images**: The ability to upload an image (either a base 64 string or a file upload via form) and then have that image sent off to ChatGPT's vision-preview model to get a description of what is happening in the image.

- **Infinite Image Scroll**: The API also included an infinite scroll feature which was implemented using DRF's pagination feature. This works by returning a dictionary with the keys 'results', 'next', 'previous'. The results will* be displayed on the frontend and once the client user starts getting too close to the last comment, the client will use the 'next' key to send a request for more results to continue the flow of images or comments.

- **Single Image Views**: This end point would provide ALL of the information for a single image. Including a paginated version of the comments, which just like described in the previous feature is infinite scroll.

- **Comment Management**: This endpoint was to allow the client to leave comments on specific images.

## Enviroment
To run this you'll need:

-**Python 3.8**: The coding language used by all of these libraries and packages.

-**Django 3.x**: Django is a 'batteries included' framework that takes care of a lot of the tedious part of building a site. This API takes advantage of the routing, ORM, testing, and request.

-**Django Restframework (DRF)**: DRF is a django extension library that makes it easier to create restful endpoints. It does this by using serializers and prebuilt API subclasses.

-**Pillow 10.x**: Pillow is a image management library used for converted base64 and binary image files.

-**Celery**: Celery is a async and task management library used to run tasks asyncrously. It was used in this project to a response to the client before the image analysis had been completed.

-**Redis**: Is a memeory management library that is often paried with celery to use as a messaging broker. In this example when all of the celery workers are unavialable, redis will hold that data.

## Installation
1. **Clone the Repo**
```
git clone https://github.com/jsimerly/edlight-task
cd edlight-task
```

2. **Set Up Venv**
```
python -m venv venv
```
For the sake of this project, I included my venv in the source code and did not put .venv into .gitignore.

3. **Install Dependancies**
```
pip install -r requirements.txt
```
This should get you all of the packages you need to run the api.

4. **Enviromental (local) variables**

   These variable I did include in .gitignore as they contain my passwords and gpt_api_keys.
 
  But here is what you'll need:

```
SECRET_KEY=insecure-django-security-key
DEBUG=True
SECURE_SSL_REDIRECT=False

ALLOWED_HOSTS=127.0.0.1,127.0.0.1:8000,127.0.0.1:8080,localhost,127.0.0.1:5173

CORS_ALLOWED=http://127.0.0.1:8000,http://127.0.0.1,http://127.0.0.1:5173
CSRF_TRUSTED_ORIGINS=http://127.0.0.1:8000,http://127.0.0.1,http://127.0.0.1:8080
CSRF_COOKIE_DOMAIN=127.0.0.1

MEDIA_URL=http://127.0.0.1:8000/media/

SU_USERNAME= [username for superuser]
SU_PASSWORD= [password]
SU_EMAIL= [email]

DATABASE_NAME=[database name]
DATABASE_USER=[user name]
DATABASE_PASSWORD=[db password]
DATABASE_HOST=[db host]
DATABASE_PORT=[db port]

OPENAI_API_KEY=[your openai key here]

HASHID_SALT=[a salt key you can use for hashing, not featured in the project but good practice]
```

5. **Migrations**
```
python manage.py makemigrations
python manage.py migrate
```

6. **Run the App**
```
python manage.py runserver
```
In a seperate cmd
```
celery -A edlight-task worker --loglevel=info
```

## API Endpoints
- **Analyze Image**
  - **URL**: '/analyze-image'
  - **Method**: 'POST'
  - **Body**: 'img': image file or base64 image string
- **Infinite Image Scroll**
  - **URL**: '/images'
  - **Method**: 'GET'
- **View Single Image**
  - **URL**: '/image/<uuid>'
  - **Method**: 'GET'
- **Add Comment to Image**
  - **URL**: '/images'
  - **Method**: 'POST'
  - **Body**: 'text': Text of the comment being left by the user
- **View Paginated Comments**
  - **URL**: '/image/<uuid>/pag-comments'
  - **Method**: 'GET'
  - **Notes:**: This wasn't a requested enpoint but an endpoint that helped make the nest pagination more efficent.
 
## Testing
Run the test using this command:
```
python manage.py test
```

Please note that running these test will charge your GPT account per request. If you do not want this please disable them by commenting out `AnalyzeImageViewTest` in tests.

## Database Schema
### Image Model
- **UUID('uuid')**
  - Postgres Type: UUIDField
  - Primary Key
  - Unique
  - Uneditable
  - Non-null
  - uui4 default

- **Image File('img')**
  - Postgres Type: ImageField
  - Stores an ImageFile (not base64)
  - Non-null
 
- **Description('desc')**
  - Postgres Type: CharField
  - max_length is 1000

- **Upload Date('upload_date')**
  - Postgres Type: CharField
  - Auto set on creation
  - Uneditable
  - Django Timezone format
 
- **Edited Date('edited_date')**
  - Postgres Type: DateTimeField
  - Auto set on update
  - Django Timezone format

- **Ordering**:
  - The default ordering is by upload_date in descending order.

### Comment Model
- **UUID('uuid')**
  - Postgres Type: UUIDField
  - Primary Key
  - Unique
  - Uneditable
  - Non-null
  - uui4 default
 
- **Image('image')**
  - Postgres Type: ForeignKey (many to one)
    - Linked to Image
    - Cascade on delete
- **Text('text')**
  - Postgres Type: TextField
    
- **Upload Date('upload_date')**
  - Postgres Type: CharField
  - Auto set on creation
  - Uneditable
  - Django Timezone format
 
- **Edited Date('edited_date')**
  - Postgres Type: DateTimeField
  - Auto set on update
  - Django Timezone format
 
- **Ordering**:
  - The default ordering is by upload_date in descending order.

