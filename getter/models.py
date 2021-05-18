from django.db import models

# Create your models here.


class Audio(models.Model):
    audio_path = models.CharField(max_length=300)
    duration = models.FloatField()
    transcript = models.CharField(max_length=300)
    exported = models.BooleanField(default=0)