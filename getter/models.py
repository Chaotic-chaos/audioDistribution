from django.db import models

# Create your models here.


class Audio(models.Model):
    # audio_path
    audio_path = models.CharField(max_length=300)
    # audio duration
    duration = models.FloatField()
    # audio transcripts
    transcript = models.CharField(max_length=300)
    # audio sample rate
    sample_rate = models.IntegerField(default=None)
    # whether audio is exported or not
    exported = models.BooleanField(default=False)
    # whether audio is distributed or not
    distributed = models.BooleanField(default=False)
    # where the audio comes from
    source = models.CharField(max_length=300)