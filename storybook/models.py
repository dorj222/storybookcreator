from django.db import models
import uuid

class Storybook(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=250)
    createdAt = models.DateTimeField()
    duration = models.FloatField()
    iterations = models.IntegerField()
    status = models.BooleanField()
    
class Image(models.Model):
    storybook_id = models.ForeignKey(Storybook, on_delete=models.CASCADE, related_name='images')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # image = models.ImageField(upload_to='storybook_images/')
    description = models.CharField(max_length=250)
