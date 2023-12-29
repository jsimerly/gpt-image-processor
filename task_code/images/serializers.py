from rest_framework import serializers
from images.models import Image, Comment
from django.urls import reverse


class ImageSerializer(serializers.ModelSerializer):
    comments_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['uuid', 'img', 'desc', 'upload_date', 'edited_date', 'comments_url'] 

    def get_comments_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(reverse('image-comments', args=[obj.pk]))
        return None

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['uuid', 'image', 'text', 'upload_date', 'edited_date']

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Text in a comment cannot be empty.")
        return value       