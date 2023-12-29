from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from images.util import is_base64, is_img_file, convert_binary_file_to_base64, convert_b64_to_img_file
from images.tasks import process_image_and_create_obj
from images.models import Image, Comment
from images.serializers import ImageSerializer, CommentSerializer


# Create your views here.
class AnalyzeImageView(APIView):
    def post(self, request):
        img_data = request.data.get('img')
        #check file type the convert to base64
        if hasattr(img_data, 'read') and is_img_file(img_data): 
            try:
                b64_img = convert_binary_file_to_base64(img_data)
            except ValueError as e:
                return Response({'error_msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            img_file = img_data
        elif is_base64(img_data):
            b64_img = img_data
            try:
                img_file = convert_b64_to_img_file(img_data)
            except ValueError as e:
                return Response({'error_msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error_msg': 'An image must be either base64 or attached as a file to this request.'}, status=status.HTTP_400_BAD_REQUEST)    
              
        process_image_and_create_obj(b64_img, img_file)
        return Response(status=status.HTTP_202_ACCEPTED)
        
class ImagePagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page_size'
    max_page_size = 30

class InfiniteImagesView(ListAPIView):
    serializer_class = ImageSerializer
    pagination_class = ImagePagination

    def get_queryset(self):
        return Image.objects.all().order_by('-upload_date')
    
class SingleImageView(APIView):
    def get(self, request, uuid):
        image_obj = get_object_or_404(Image, pk=uuid)

        serializer = ImageSerializer(image_obj)

        return Response(serializer.data, status=status.HTTP_200_OK)   

class CommentPagination(PageNumberPagination):
    page_size = 20
    page_query_param = 'page_size'
    max_page_size = 80

class CommentListView(ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = CommentPagination

    def get_queryset(self):
        image_pk = self.kwargs['uuid']
        return Comment.objects.filter(image__pk=image_pk).order_by('-upload_date')
    
class LeaveComment(APIView):
    serializer_class = CommentSerializer

    def post(self, request, uuid):
        image = get_object_or_404(Image, pk=uuid)
        text = request.data.get('text')

        serializer_data = {
            'image': image.pk,
            'text': text,
        }
        serializer = self.serializer_class(data=serializer_data)
        
        try:
            if serializer.is_valid():
                serializer.save()

                return Response(status=status.HTTP_201_CREATED)
            return Response({'error_msg': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'error_msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        