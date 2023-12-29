from django.db import models
from uuid import uuid4


class Image(models.Model):
    '''
    Here we're setting a uuid as a primary key. This will be used as the key to find this objects data in our posgres database.

    The reason we're chooisng to use a uuid (instead of a standard id) is because we're planning on using this at scale which means we will need to implement sharding. By using a UUID, this will prevent collision between sharded databases.
    '''
    
    uuid = models.UUIDField(
        unique=True, 
        editable=False, 
        default=uuid4,
        primary_key=True
    )
    img = models.ImageField(upload_to='images/', null=False, blank=False)

    #Using a charfield over a text field for database storage efficency. May need to adjust to a textfield if our external image processor is returning larger respones.
    desc = models.CharField(max_length=1000)

    upload_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'Image ({self.pk}): {self.desc[0:30]}'

    class Meta:
        ordering = ['-upload_date']

class Comment(models.Model):
    uuid = models.UUIDField(
        unique=True, 
        editable=False, 
        default=uuid4,
        primary_key=True
    )
    image = models.ForeignKey(
        Image, 
        on_delete=models.CASCADE,
        null=False,
    )
    text = models.TextField()

    upload_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment {self.uuid} on Image {self.image.uuid}"
    
    class Meta:
        ordering = ['-upload_date']