from django.db import models

# Create your models here.


class Audio(models.Model):
    audio_path = models.CharField(max_length=300)
    duration = models.FloatField()
    transcript = models.CharField(max_length=300)
    sample_rate = models.IntegerField(default=None)
    exported = models.BooleanField(default=False)
    distributed = models.BooleanField(default=False)