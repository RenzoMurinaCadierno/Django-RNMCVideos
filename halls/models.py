from django.db import models
from django.contrib.auth.models import User

class Hall(models.Model):
    title = models.CharField(max_length=256)

    # one user has one hall
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Video(models.Model):
    title = models.CharField(max_length=256)
    url = models.URLField()
    youtube_id = models.CharField(max_length=256)

    # one call can have multiple videos
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
