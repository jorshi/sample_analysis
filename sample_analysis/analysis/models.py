from __future__ import unicode_literals

from django.db import models

class SamplePack(models.Model):
    id_name = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)

class Kit(models.Model):
    sample_pack = models.ForeignKey('SamplePack', on_delete=models.CASCADE)
    id_number = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('sample_pack', 'id_number')

class Sample(models.Model):

    KICK = 'ki'
    SNARE = 'sn'
    UNKNOWN = 'un'
    SAMPLE_TYPE_CHOICES = (
        (KICK, 'Kick'),
        (SNARE, 'Snare'),
        (UNKNOWN, 'Unknown'),
    )

    kit = models.ForeignKey('Kit', on_delete=models.CASCADE)
    path = models.FilePathField(max_length=200)
    sample_type = models.CharField(
        max_length=2,
        choices=SAMPLE_TYPE_CHOICES,
        default=UNKNOWN,
    )
    
    class Meta:
        unique_together = ('kit', 'path')


class Analysis(models.Model):

    sample = models.OneToOneField(Sample, on_delete=models.CASCADE)
    loudness = models.FloatField(blank=True, null=True)
    equal_loudness = models.FloatField(blank=True, null=True)
    spectral_centroid = models.FloatField(blank=True, null=True)
    temporal_centroid = models.FloatField(blank=True, null=True)
    rms = models.FloatField(blank=True, null=True)
    spectral_kurtosis = models.FloatField(blank=True, null=True)

# Create your models here.
