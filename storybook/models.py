from django.db import models
import uuid

class Storybook(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=250)
    createdAt = models.DateTimeField()
    starting_sentence = models.CharField(max_length=250)
    finished_playthrough = models.BooleanField()
    drawing = models.JSONField(default=list)
    signed_the_book = models.BooleanField()
    decision_of_authorship = models.CharField(max_length=100)

class Image(models.Model):
    storybook_id = models.ForeignKey(Storybook, on_delete=models.CASCADE, related_name='images')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    def get_upload_to(self, filename):
        return 'storybook_images/%s/%s' % (self.storybook_id_id, filename)
    image = models.ImageField(upload_to=get_upload_to, null=True) 
    description = models.TextField()
        
class Description(models.Model):
    storybook_id = models.ForeignKey(Storybook, on_delete=models.CASCADE, related_name='description')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=250)