from __future__ import unicode_literals

from django.db import models

class Tag(models.Model):
    word = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return self.word

class Manufacturer(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return self.name


class SamplePack(models.Model):
    id_name = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    tags = models.ManyToManyField(Tag, related_name='samples_packs')
    date = models.DateField(null=True, blank=True)
    info_link = models.URLField(null=True, blank=True)
    manufacturer = models.ForeignKey('Manufacturer', null=True, blank=True)
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

class AnalysisMinMax(models.Model):

    sample = models.OneToOneField(Sample, on_delete=models.CASCADE)

    equal_loudness = models.FloatField(blank=True, null=True)
    spectral_centroid = models.FloatField(blank=True, null=True)
    spectral_centroid_1 = models.FloatField(blank=True, null=True)
    spectral_centroid_2 = models.FloatField(blank=True, null=True)
    temporal_centroid = models.FloatField(blank=True, null=True)
    rms = models.FloatField(blank=True, null=True)
    spectral_kurtosis = models.FloatField(blank=True, null=True)
    pitch_salience = models.FloatField(blank=True, null=True)


class AnalysisPCA(models.Model):

    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    window_length = models.IntegerField(blank=True, null=True)
    window_start = models.IntegerField(blank=True, null=True)

    dim_1 = models.FloatField(blank=True, null=True)
    dim_2 = models.FloatField(blank=True, null=True)
    dim_3 = models.FloatField(blank=True, null=True)
    dim_4 = models.FloatField(blank=True, null=True)
    dim_5 = models.FloatField(blank=True, null=True)
    dim_6 = models.FloatField(blank=True, null=True)
    dim_7 = models.FloatField(blank=True, null=True)
    dim_8 = models.FloatField(blank=True, null=True)

    class Meta:
        unique_together = (('sample', 'window_length', 'window_start'),)


class Manifold(models.Model):

    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    window_length = models.IntegerField(blank=True, null=True)
    window_start = models.IntegerField(blank=True, null=True)

    method = models.CharField(max_length=200)

    dim_1 = models.FloatField(blank=True, null=True)
    dim_2 = models.FloatField(blank=True, null=True)
    dim_3 = models.FloatField(blank=True, null=True)
    dim_4 = models.FloatField(blank=True, null=True)

    class Meta:
        unique_together = (('sample', 'window_length', 'window_start', 'method'),)


class AnalysisFull(models.Model):

    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    window_length = models.IntegerField(blank=True, null=True)
    window_start = models.IntegerField(blank=True, null=True)

    bark_1_mean = models.FloatField(blank=True, null=True)
    bark_2_mean = models.FloatField(blank=True, null=True)
    bark_3_mean = models.FloatField(blank=True, null=True)
    bark_4_mean = models.FloatField(blank=True, null=True)
    bark_5_mean = models.FloatField(blank=True, null=True)
    bark_6_mean = models.FloatField(blank=True, null=True)
    bark_7_mean = models.FloatField(blank=True, null=True)
    bark_8_mean = models.FloatField(blank=True, null=True)
    bark_9_mean = models.FloatField(blank=True, null=True)
    bark_10_mean = models.FloatField(blank=True, null=True)
    bark_11_mean = models.FloatField(blank=True, null=True)
    bark_12_mean = models.FloatField(blank=True, null=True)
    bark_13_mean = models.FloatField(blank=True, null=True)
    bark_14_mean = models.FloatField(blank=True, null=True)
    bark_15_mean = models.FloatField(blank=True, null=True)
    bark_16_mean = models.FloatField(blank=True, null=True)
    bark_17_mean = models.FloatField(blank=True, null=True)
    bark_18_mean = models.FloatField(blank=True, null=True)
    bark_19_mean = models.FloatField(blank=True, null=True)
    bark_20_mean = models.FloatField(blank=True, null=True)
    bark_21_mean = models.FloatField(blank=True, null=True)
    bark_22_mean = models.FloatField(blank=True, null=True)
    bark_23_mean = models.FloatField(blank=True, null=True)
    bark_24_mean = models.FloatField(blank=True, null=True)
    bark_25_mean = models.FloatField(blank=True, null=True)
    bark_26_mean = models.FloatField(blank=True, null=True)
    bark_27_mean = models.FloatField(blank=True, null=True)

    bark_1_dev = models.FloatField(blank=True, null=True)
    bark_2_dev = models.FloatField(blank=True, null=True)
    bark_3_dev = models.FloatField(blank=True, null=True)
    bark_4_dev = models.FloatField(blank=True, null=True)
    bark_5_dev = models.FloatField(blank=True, null=True)
    bark_6_dev = models.FloatField(blank=True, null=True)
    bark_7_dev = models.FloatField(blank=True, null=True)
    bark_8_dev = models.FloatField(blank=True, null=True)
    bark_9_dev = models.FloatField(blank=True, null=True)
    bark_10_dev = models.FloatField(blank=True, null=True)
    bark_11_dev = models.FloatField(blank=True, null=True)
    bark_12_dev = models.FloatField(blank=True, null=True)
    bark_13_dev = models.FloatField(blank=True, null=True)
    bark_14_dev = models.FloatField(blank=True, null=True)
    bark_15_dev = models.FloatField(blank=True, null=True)
    bark_16_dev = models.FloatField(blank=True, null=True)
    bark_17_dev = models.FloatField(blank=True, null=True)
    bark_18_dev = models.FloatField(blank=True, null=True)
    bark_19_dev = models.FloatField(blank=True, null=True)
    bark_20_dev = models.FloatField(blank=True, null=True)
    bark_21_dev = models.FloatField(blank=True, null=True)
    bark_22_dev = models.FloatField(blank=True, null=True)
    bark_23_dev = models.FloatField(blank=True, null=True)
    bark_24_dev = models.FloatField(blank=True, null=True)
    bark_25_dev = models.FloatField(blank=True, null=True)
    bark_26_dev = models.FloatField(blank=True, null=True)
    bark_27_dev = models.FloatField(blank=True, null=True)

    bark_kurtosis = models.FloatField(blank=True, null=True)
    bark_skewness = models.FloatField(blank=True, null=True)
    bark_spread = models.FloatField(blank=True, null=True)

    bark_kurtosis_dev = models.FloatField(blank=True, null=True)
    bark_skewness_dev = models.FloatField(blank=True, null=True)
    bark_spread_dev = models.FloatField(blank=True, null=True)

    hfc = models.FloatField(blank=True, null=True)
    hfc_dev = models.FloatField(blank=True, null=True)

    mfcc_1_mean = models.FloatField(blank=True, null=True)
    mfcc_2_mean = models.FloatField(blank=True, null=True)
    mfcc_3_mean = models.FloatField(blank=True, null=True)
    mfcc_4_mean = models.FloatField(blank=True, null=True)
    mfcc_5_mean = models.FloatField(blank=True, null=True)
    mfcc_6_mean = models.FloatField(blank=True, null=True)
    mfcc_7_mean = models.FloatField(blank=True, null=True)
    mfcc_8_mean = models.FloatField(blank=True, null=True)
    mfcc_9_mean = models.FloatField(blank=True, null=True)
    mfcc_10_mean = models.FloatField(blank=True, null=True)
    mfcc_11_mean = models.FloatField(blank=True, null=True)
    mfcc_12_mean = models.FloatField(blank=True, null=True)
    mfcc_13_mean = models.FloatField(blank=True, null=True)

    mfcc_1_dev = models.FloatField(blank=True, null=True)
    mfcc_2_dev = models.FloatField(blank=True, null=True)
    mfcc_3_dev = models.FloatField(blank=True, null=True)
    mfcc_4_dev = models.FloatField(blank=True, null=True)
    mfcc_5_dev = models.FloatField(blank=True, null=True)
    mfcc_6_dev = models.FloatField(blank=True, null=True)
    mfcc_7_dev = models.FloatField(blank=True, null=True)
    mfcc_8_dev = models.FloatField(blank=True, null=True)
    mfcc_9_dev = models.FloatField(blank=True, null=True)
    mfcc_10_dev = models.FloatField(blank=True, null=True)
    mfcc_11_dev = models.FloatField(blank=True, null=True)
    mfcc_12_dev = models.FloatField(blank=True, null=True)
    mfcc_13_dev = models.FloatField(blank=True, null=True)

    temporal_centroid = models.FloatField(blank=True, null=True)
    rms = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)

    zero_crossing_rate = models.FloatField(blank=True, null=True)
    pitch_salience = models.FloatField(blank=True, null=True)
    spectral_complexity = models.FloatField(blank=True, null=True)
    spectral_crest = models.FloatField(blank=True, null=True)
    spectral_decrease = models.FloatField(blank=True, null=True)
    spectral_energy = models.FloatField(blank=True, null=True)
    spectral_energyband_low = models.FloatField(blank=True, null=True)
    spectral_energyband_middle_low = models.FloatField(blank=True, null=True)
    spectral_energyband_middle_high = models.FloatField(blank=True, null=True)
    spectral_energyband_high = models.FloatField(blank=True, null=True)
    spectral_flatness_db = models.FloatField(blank=True, null=True)
    spectral_flux = models.FloatField(blank=True, null=True)
    spectral_rms = models.FloatField(blank=True, null=True)
    spectral_rolloff = models.FloatField(blank=True, null=True)
    spectral_strongpeak = models.FloatField(blank=True, null=True)
    inharmonicity = models.FloatField(blank=True, null=True)

    zero_crossing_rate_dev = models.FloatField(blank=True, null=True)
    pitch_salience_dev = models.FloatField(blank=True, null=True)
    spectral_complexity_dev = models.FloatField(blank=True, null=True)
    spectral_crest_dev = models.FloatField(blank=True, null=True)
    spectral_decrease_dev = models.FloatField(blank=True, null=True)
    spectral_energy_dev = models.FloatField(blank=True, null=True)
    spectral_energyband_low_dev = models.FloatField(blank=True, null=True)
    spectral_energyband_middle_low_dev = models.FloatField(blank=True, null=True)
    spectral_energyband_middle_high_dev = models.FloatField(blank=True, null=True)
    spectral_energyband_high_dev = models.FloatField(blank=True, null=True)
    spectral_flatness_db_dev = models.FloatField(blank=True, null=True)
    spectral_flux_dev = models.FloatField(blank=True, null=True)
    spectral_rms_dev = models.FloatField(blank=True, null=True)
    spectral_rolloff_dev = models.FloatField(blank=True, null=True)
    spectral_strongpeak_dev = models.FloatField(blank=True, null=True)
    inharmonicity_dev = models.FloatField(blank=True, null=True)
    
    tristimulus_1 = models.FloatField(blank=True, null=True)
    tristimulus_2 = models.FloatField(blank=True, null=True)
    tristimulus_3 = models.FloatField(blank=True, null=True)

    tristimulus_1_dev = models.FloatField(blank=True, null=True)
    tristimulus_2_dev = models.FloatField(blank=True, null=True)
    tristimulus_3_dev = models.FloatField(blank=True, null=True)

    spectral_centroid = models.FloatField(blank=True, null=True)
    spectral_kurtosis = models.FloatField(blank=True, null=True)
    spectral_skewness = models.FloatField(blank=True, null=True)
    spectral_spread = models.FloatField(blank=True, null=True)

    spectral_centroid_dev = models.FloatField(blank=True, null=True)
    spectral_kurtosis_dev = models.FloatField(blank=True, null=True)
    spectral_skewness_dev = models.FloatField(blank=True, null=True)
    spectral_spread_dev = models.FloatField(blank=True, null=True)

    class Meta:
        unique_together = (('sample', 'window_length', 'window_start'),)
