#This file is used for routing URLs to the proper view
from django.urls import path
from images.views import *

urlpatterns = [
    path('analyze-image', AnalyzeImageView.as_view(), name='load_image'),
    path('images/', InfiniteImagesView.as_view(), name='infinite_images'),
    path('image/<uuid:uuid>', SingleImageView.as_view(), name='single-image'),
    path('image/<uuid:uuid>/comment', LeaveComment.as_view(), name='leave-comment'),

    path('image/<uuid:uuid>/pag-comments', CommentListView.as_view(), name='image-comments'), #this is used in pagination to avoid nested pagination reloading everytime there is an update to the parent.
]
