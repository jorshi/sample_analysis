from __future__ import unicode_literals

from django.db import models

class Tag(models.Model):
    word = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return self.word


class SamplePack(models.Model):
    id_name = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    tags = models.ManyToManyField(Tag, related_name='samples_packs')
    date = models.DateField(null=True, blank=True)
    info_link = models.URLField(default=None, blank=True)
    exclude = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class Kit(models.Model):
    sample_pack = models.ForeignKey('SamplePack', on_delete=models.CASCADE)
    id_number = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('sample_pack', 'id_number')

    def __unicode__(self):
        return "%s kit_%s" % (self.sample_pack.name, self.id_number)


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
    start_time = models.FloatField(blank=True, null=True)
    stop_time = models.FloatField(blank=True, null=True)
    exclude = models.BooleanField(default=False)

    class Meta:
        unique_together = ('kit', 'path')


    def __unicode__(self):
        return "%s %s" % (self.kit.__unicode__(), self.sample_type)


class Analysis(models.Model):

    sample = models.OneToOneField(Sample, on_delete=models.CASCADE)
    outlier = models.BooleanField(default=False)

    duration = models.FloatField(blank=True, null=True)
    equal_loudness = models.FloatField(blank=True, null=True)
    spectral_centroid = models.FloatField(blank=True, null=True)
    spectral_centroid_1 = models.FloatField(blank=True, null=True)
    spectral_centroid_2 = models.FloatField(blank=True, null=True)
    temporal_centroid = models.FloatField(blank=True, null=True)
    rms = models.FloatField(blank=True, null=True)
    spectral_kurtosis = models.FloatField(blank=True, null=True)
    pitch_salience = models.FloatField(blank=True, null=True)

class AnalysisZ(models.Model):

    sample = models.OneToOneField(Sample, on_delete=models.CASCADE)

    duration = models.FloatField(blank=True, null=True)
    #loudness = models.FloatField(blank=True, null=True)
    equal_loudness = models.FloatField(blank=True, null=True)
    spectral_centroid = models.FloatField(blank=True, null=True)
    #spectral_centroid_1 = models.FloatField(blank=True, null=True)
    #spectral_centroid_2 = models.FloatField(blank=True, null=True)
    temporal_centroid = models.FloatField(blank=True, null=True)
    rms = models.FloatField(blank=True, null=True)
    spectral_kurtosis = models.FloatField(blank=True, null=True)
    pitch_salience = models.FloatField(blank=True, null=True)

class AnalysisRobustScale(models.Model):

    sample = models.OneToOneField(Sample, on_delete=models.CASCADE)

    duration = models.FloatField(blank=True, null=True)
    #loudness = models.FloatField(blank=True, null=True)
    equal_loudness = models.FloatField(blank=True, null=True)
    spectral_centroid = models.FloatField(blank=True, null=True)
    #spectral_centroid_1 = models.FloatField(blank=True, null=True)
    #spectral_centroid_2 = models.FloatField(blank=True, null=True)
    temporal_centroid = models.FloatField(blank=True, null=True)
    rms = models.FloatField(blank=True, null=True)
    spectral_kurtosis = models.FloatField(blank=True, null=True)
    pitch_salience = models.FloatField(blank=True, null=True)
