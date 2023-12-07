from django.db import models

# Create your models here.
class Storybook(models.Model):
    title = models.CharField(max_length=250)
    createdAt = models.DateTimeField()
    duration = models.FloatField()
    iterations = models.IntegerField()
    status = models.BooleanField()
