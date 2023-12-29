from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase
from rest_framework import status
import os
from images.models import Image, Comment
from images.serializers import ImageSerializer
from uuid import uuid4


# Create your tests here.

#Views Tests
class AnalyzeImageViewTest(APITestCase):
    # def test_valid_img_b64(self):
    #     url = reverse('load_image')
    #     current_dir = os.path.dirname(os.path.abspath(__file__))
    #     image_path = os.path.join(current_dir, 'test_image.txt')
    #     with open(image_path, 'r') as file:
    #         valid_b64_data = file.read().strip()

    #     response = self.client.post(url, {'img': valid_b64_data}, format='json')

    #     self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    # def test_valid_img_file(self):
    #     url = reverse('load_image')
    #     current_dir = os.path.dirname(os.path.abspath(__file__))
    #     image_path = os.path.join(current_dir, 'test_image.jpg')
    #     with open(image_path, 'rb') as img:

    #         image_file = SimpleUploadedFile(image_path, img.read(), content_type='image/jpeg')
    #         response = self.client.post(url, {'img': image_file}, format='multipart')

    #         self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_invalid_img(self):
        url = reverse('load_image')
        invalid_data = 'not_an_image'

        response = self.client.post(url, {'img': invalid_data}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class InfiniteImagesViewTest(APITestCase):
    def setUp(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, 'test_image.txt')
        self.images = []
        for _ in range(15): 
            image = Image.objects.create(img=image_path, desc='Test Desc')
            self.images.append(image)

    def test_image_pagination(self):
        response = self.client.get('/task/images/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertIn('results', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        
        pagination_size = 10 
        self.assertEqual(len(response.data['results']), pagination_size)

    def test_get_images(self):
        response = self.client.get('/task/images/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_value = min(len(self.images), 10)
        self.assertEqual(len(response.data['results']), expected_value)


class SingleImageViewTest(APITestCase):
    def setUp(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, 'test_image.txt')
        self.image = Image.objects.create(img=image_path, desc='Test Desc')

    def test_get_iamge(self):
        url = reverse('single-image', kwargs={'uuid': self.image.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = ImageSerializer(self.image)
        self.assertEqual(response.data, serializer.data)       

    def test_invalid_pk(self):
        invalid_uuid = uuid4()
        url = reverse('single-image', kwargs={'uuid': invalid_uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class LeaveCommentTest(APITestCase):
    def setUp(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, 'test_image.jpg')
        self.image = Image.objects.create(img=image_path, desc='Test Desc')

    def test_leave_comment_valid(self):
        url = reverse('leave-comment', kwargs={'uuid': self.image.pk})
        comment_data = { 
            "text": "Test comment"
        }
        response = self.client.post(url, comment_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().text, "Test comment")

    def test_leave_comment_id(self):
        invalid_uuid = uuid4()
        url = reverse('leave-comment', kwargs={'uuid': invalid_uuid})
        invalid_comment_data = {
            "text": ""
        }

        response = self.client.post(url, invalid_comment_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Comment.objects.count(), 0)

    def test_leave_comment_comment(self):
        url = reverse('leave-comment', kwargs={'uuid': self.image.pk})
        comment_data = { 
            "text": ""
        }
        response = self.client.post(url, comment_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)

class CommentListViewTest(APITestCase):
    def setUp(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, 'test_image.jpg')
        self.image = Image.objects.create(img=image_path, desc='Test Desc')

        self.comments = []
        for _ in range(5):  # Create a few comments
            comment = Comment.objects.create(image=self.image, text="Test Comment")
            self.comments.append(comment)

    def test_get_comments(self):
        url = reverse('image-comments', kwargs={'uuid': self.image.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), Comment.objects.filter(image=self.image).count())

    def test_comment_pagination(self):
        for _ in range(40):
            comment = Comment.objects.create(image=self.image, text='test comment')
            self.comments.append(comment)

        url = reverse('image-comments', kwargs={'uuid': self.image.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('results', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)

#OPEN AI