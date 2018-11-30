"""
Main command for running various feature extraction algorithms
on the entire set of samples referenced in the database. As the
set of analysisObject we want to extract grows this may get awkward,
but for now it works well to get all the analysisObject into the DB
and maintain the relation to the samples

Usage:
    python ./manage.py runanalysis analysis_type
"""


import sys
import essentia.standard as es
import numpy as np
import math
from django.core.management.base import BaseCommand, CommandError
from analysis.models import Sample, Analysis, AnalysisFull

import pickle

class Command(BaseCommand):
    help = 'Run a full set of low-level extractors'
    loaders = {
        'mono': es.MonoLoader,
        'eqloud': es.EqloudLoader
    }

    # Override of the add_argument method
    def add_arguments(self, parser):
        
        parser.add_argument(
            '--window_length',
            dest='window_length',
            type=int,
            default=0
        )

        parser.add_argument(
            '--window_start',
            dest='window_start',
            type=int,
            default=0
        )



    # Executes on command runtime
    def handle(self, *args, **options):

        self.windowLength = options['window_length']
        self.windowStart = options['window_start']
        self.runAnalysis()
        self.stdout.write(self.style.SUCCESS('Complete'))

    # Main function for running analysis
    def runAnalysis(self):

        # Get all samples referenced in DB, except for those
        # that have been marked as samples to exclude
        # TODO: Need to clarify whether or not sample packs
        # should be excluded if we can't find enough info on them,
        # for now including all samplepacks
        samples = Sample.objects.all().filter(
            exclude=False,
            #kit__sample_pack__exclude=False, 
        )

        numSamples = len(samples)
        self.stdout.write("Running low-level extractors on %s samples. " % (numSamples))
        i = 0.0

        for sample in samples:
            # Get audio and run loudness analysis
            try:
                loader = es.MonoLoader(filename=sample.path)
                neqAudio = loader()

                eqLoader = es.EqloudLoader(filename=sample.path)
                eqAudio = eqLoader()

                # Trim the audio clip
                trimmer = es.Trimmer(startTime=sample.start_time, endTime=sample.stop_time)
                neqAudio = trimmer(neqAudio)
                eqAudio = trimmer(eqAudio)

            except RuntimeError as esExcept:
                self.stderr.write("%s\n" % esExcept)
                self.stderr.write("%s failed to load. Excluding sample from further analysis" % sample.path)
                sample.exclude = True
                sample.save()
                i = i + 1
                continue

            # Frame size & hop size
            frameSize = 2048
            hopSize = 256
            
            # Amplitude envelope of sample
            envelope = es.Envelope()
            audioEnv = envelope(eqAudio)

            # Find attack phase and LAT
            latFunc = es.LogAttackTime()
            lat, attackStart, attackEnd = latFunc(audioEnv) 

            # Temporal Centroid on entire sample length
            tc = self.temporal_centroid(eqAudio)

            # Time segmentation starting point
            windowFunc = es.LogAttackTime(startAttackThreshold=float(self.windowStart if self.windowStart < 90 else 90)/100)
            _, windowStart, windowEnd = windowFunc(audioEnv)
            windowStart = windowStart if self.windowStart < 90 else windowEnd

            if self.windowLength > 0:
                # Window from onset
                trimmer = es.Trimmer(startTime=windowStart, endTime=windowStart + (float(self.windowLength) / 1000))
                eqAudio = trimmer(eqAudio)
                neqAudio = trimmer(neqAudio)

            # Get analysis object for this sample
            try:
                analysisObject = AnalysisFull.objects.get(
                    sample=sample,
                    window_length=self.windowLength,
                    window_start=self.windowStart
                )
            except AnalysisFull.DoesNotExist:
                analysisObject = AnalysisFull(
                    sample=sample,
                    window_length=self.windowLength,
                    window_start=self.windowStart
                )

            analysisObject.lat = lat
            analysisObject.rms = self.rms(eqAudio)
            analysisObject.temporal_centroid = tc

            # Spectral extractor without equal loudness filter
            neqSpectralExtractor = es.LowLevelSpectralExtractor(frameSize=frameSize, hopSize=hopSize)
            neqSpectralResults = neqSpectralExtractor(neqAudio)

            bark_mean = np.mean(neqSpectralResults[0], axis=0)
            analysisObject.bark_1_mean = bark_mean[0]
            analysisObject.bark_2_mean = bark_mean[1]
            analysisObject.bark_3_mean = bark_mean[2]
            analysisObject.bark_4_mean = bark_mean[3]
            analysisObject.bark_5_mean = bark_mean[4]
            analysisObject.bark_6_mean = bark_mean[5]
            analysisObject.bark_7_mean = bark_mean[6]
            analysisObject.bark_8_mean = bark_mean[7]
            analysisObject.bark_9_mean = bark_mean[8]
            analysisObject.bark_10_mean = bark_mean[9]
            analysisObject.bark_11_mean = bark_mean[10]
            analysisObject.bark_12_mean = bark_mean[11]
            analysisObject.bark_13_mean = bark_mean[12]
            analysisObject.bark_14_mean = bark_mean[13]
            analysisObject.bark_15_mean = bark_mean[14]
            analysisObject.bark_16_mean = bark_mean[15]
            analysisObject.bark_17_mean = bark_mean[16]
            analysisObject.bark_18_mean = bark_mean[17]
            analysisObject.bark_19_mean = bark_mean[18]
            analysisObject.bark_20_mean = bark_mean[19]
            analysisObject.bark_21_mean = bark_mean[20]
            analysisObject.bark_22_mean = bark_mean[21]
            analysisObject.bark_23_mean = bark_mean[22]
            analysisObject.bark_24_mean = bark_mean[23]
            analysisObject.bark_25_mean = bark_mean[24]
            analysisObject.bark_26_mean = bark_mean[25]
            analysisObject.bark_27_mean = bark_mean[26]

            bark_dev = np.std(neqSpectralResults[0], axis=0)
            analysisObject.bark_1_dev = bark_dev[0]
            analysisObject.bark_2_dev = bark_dev[1]
            analysisObject.bark_3_dev = bark_dev[2]
            analysisObject.bark_4_dev = bark_dev[3]
            analysisObject.bark_5_dev = bark_dev[4]
            analysisObject.bark_6_dev = bark_dev[5]
            analysisObject.bark_7_dev = bark_dev[6]
            analysisObject.bark_8_dev = bark_dev[7]
            analysisObject.bark_9_dev = bark_dev[8]
            analysisObject.bark_10_dev = bark_dev[9]
            analysisObject.bark_11_dev = bark_dev[10]
            analysisObject.bark_12_dev = bark_dev[11]
            analysisObject.bark_13_dev = bark_dev[12]
            analysisObject.bark_14_dev = bark_dev[13]
            analysisObject.bark_15_dev = bark_dev[14]
            analysisObject.bark_16_dev = bark_dev[15]
            analysisObject.bark_17_dev = bark_dev[16]
            analysisObject.bark_18_dev = bark_dev[17]
            analysisObject.bark_19_dev = bark_dev[18]
            analysisObject.bark_20_dev = bark_dev[19]
            analysisObject.bark_21_dev = bark_dev[20]
            analysisObject.bark_22_dev = bark_dev[21]
            analysisObject.bark_23_dev = bark_dev[22]
            analysisObject.bark_24_dev = bark_dev[23]
            analysisObject.bark_25_dev = bark_dev[24]
            analysisObject.bark_26_dev = bark_dev[25]
            analysisObject.bark_27_dev = bark_dev[26]

            analysisObject.bark_kurtosis = np.mean(neqSpectralResults[1])
            analysisObject.bark_skewness = np.mean(neqSpectralResults[2])
            analysisObject.bark_spread = np.mean(neqSpectralResults[3])

            analysisObject.bark_kurtosis_dev = np.std(neqSpectralResults[1])
            analysisObject.bark_skewness_dev = np.std(neqSpectralResults[2])
            analysisObject.bark_spread_dev = np.std(neqSpectralResults[3])

            analysisObject.hfc = np.mean(neqSpectralResults[4])
            analysisObject.hfc_dev = np.std(neqSpectralResults[4])
            
            # MFCCs
            mfcc_mean = np.mean(neqSpectralResults[5], axis=0)
            analysisObject.mfcc_1_mean = mfcc_mean[0]
            analysisObject.mfcc_2_mean = mfcc_mean[1]
            analysisObject.mfcc_3_mean = mfcc_mean[2]
            analysisObject.mfcc_4_mean = mfcc_mean[3]
            analysisObject.mfcc_5_mean = mfcc_mean[4]
            analysisObject.mfcc_6_mean = mfcc_mean[5]
            analysisObject.mfcc_7_mean = mfcc_mean[6]
            analysisObject.mfcc_8_mean = mfcc_mean[7]
            analysisObject.mfcc_9_mean = mfcc_mean[8]
            analysisObject.mfcc_10_mean = mfcc_mean[9]
            analysisObject.mfcc_11_mean = mfcc_mean[10]
            analysisObject.mfcc_12_mean = mfcc_mean[11]
            analysisObject.mfcc_13_mean = mfcc_mean[12]

            mfcc_dev = np.std(neqSpectralResults[5], axis=0)
            analysisObject.mfcc_1_dev = mfcc_dev[0]
            analysisObject.mfcc_2_dev = mfcc_dev[1]
            analysisObject.mfcc_3_dev = mfcc_dev[2]
            analysisObject.mfcc_4_dev = mfcc_dev[3]
            analysisObject.mfcc_5_dev = mfcc_dev[4]
            analysisObject.mfcc_6_dev = mfcc_dev[5]
            analysisObject.mfcc_7_dev = mfcc_dev[6]
            analysisObject.mfcc_8_dev = mfcc_dev[7]
            analysisObject.mfcc_9_dev = mfcc_dev[8]
            analysisObject.mfcc_10_dev = mfcc_dev[9]
            analysisObject.mfcc_11_dev = mfcc_dev[10]
            analysisObject.mfcc_12_dev = mfcc_dev[11]
            analysisObject.mfcc_13_dev = mfcc_dev[12]

            analysisObject.pitch_salience = np.mean(neqSpectralResults[8])
            analysisObject.spectral_complexity = np.mean(neqSpectralResults[12])
            analysisObject.spectral_crest = np.mean(neqSpectralResults[13])
            analysisObject.spectral_decrease = np.mean(neqSpectralResults[14])
            analysisObject.spectral_energy = np.mean(neqSpectralResults[15])
            analysisObject.spectral_energyband_low = np.mean(neqSpectralResults[16])
            analysisObject.spectral_energyband_middle_low = np.mean(neqSpectralResults[17])
            analysisObject.spectral_energyband_middle_high = np.mean(neqSpectralResults[18])
            analysisObject.spectral_energyband_high = np.mean(neqSpectralResults[19])
            analysisObject.spectral_flatness_db = np.mean(neqSpectralResults[20])
            analysisObject.spectral_flux = np.mean(neqSpectralResults[21])
            analysisObject.spectral_rms = np.mean(neqSpectralResults[22])
            analysisObject.spectral_rolloff = np.mean(neqSpectralResults[23])
            analysisObject.spectral_strongpeak = np.mean(neqSpectralResults[24])
            analysisObject.zero_crossing_rate = np.mean(neqSpectralResults[25])
            analysisObject.inharmonicity = np.mean(neqSpectralResults[26])

            analysisObject.pitch_salience_dev = np.std(neqSpectralResults[8])
            analysisObject.spectral_complexity_dev = np.std(neqSpectralResults[12])
            analysisObject.spectral_crest_dev = np.std(neqSpectralResults[13])
            analysisObject.spectral_decrease_dev = np.std(neqSpectralResults[14])
            analysisObject.spectral_energy_dev = np.std(neqSpectralResults[15])
            analysisObject.spectral_energyband_low_dev = np.std(neqSpectralResults[16])
            analysisObject.spectral_energyband_middle_low_dev = np.std(neqSpectralResults[17])
            analysisObject.spectral_energyband_middle_high_dev = np.std(neqSpectralResults[18])
            analysisObject.spectral_energyband_high_dev = np.std(neqSpectralResults[19])
            analysisObject.spectral_flatness_db_dev = np.std(neqSpectralResults[20])
            analysisObject.spectral_flux_dev = np.std(neqSpectralResults[21])
            analysisObject.spectral_rms_dev = np.std(neqSpectralResults[22])
            analysisObject.spectral_rolloff_dev = np.std(neqSpectralResults[23])
            analysisObject.spectral_strongpeak_dev = np.std(neqSpectralResults[24])
            analysisObject.zero_crossing_rate_dev = np.std(neqSpectralResults[25])
            analysisObject.inharmonicity_dev = np.std(neqSpectralResults[26])
            
            tristimulus = np.mean(neqSpectralResults[27], axis=0)
            analysisObject.tristimulus_1 = tristimulus[0]
            analysisObject.tristimulus_2 = tristimulus[1]
            analysisObject.tristimulus_3 = tristimulus[2]

            tristimulus_dev = np.std(neqSpectralResults[27], axis=0)
            analysisObject.tristimulus_1_dev = tristimulus_dev[0]
            analysisObject.tristimulus_2_dev = tristimulus_dev[1]
            analysisObject.tristimulus_3_dev = tristimulus_dev[2]

            # Spectral extractor with equal loudness filter
            eqSpectralExtractor = es.LowLevelSpectralEqloudExtractor(frameSize=frameSize, hopSize=hopSize)
            eqSpectralResults = eqSpectralExtractor(eqAudio)            

            analysisObject.spectral_centroid = np.mean(eqSpectralResults[3])
            analysisObject.spectral_kurtosis = np.mean(eqSpectralResults[4])
            analysisObject.spectral_skewness = np.mean(eqSpectralResults[5])
            analysisObject.spectral_spread = np.mean(eqSpectralResults[6])

            analysisObject.spectral_centroid_dev = np.std(eqSpectralResults[3])
            analysisObject.spectral_kurtosis_dev = np.std(eqSpectralResults[4])
            analysisObject.spectral_skewness_dev = np.std(eqSpectralResults[5])
            analysisObject.spectral_spread_dev = np.std(eqSpectralResults[6])

            analysisObject.save()
            
            i = i + 1
            self.stdout.write("\t\t%2.2f%%" % (100.0*(i/float(numSamples))), ending='\r')
            self.stdout.flush()

        self.stdout.write("\r", ending='\r')
        self.stdout.flush()

    # Temporal Centroid
    def temporal_centroid(self, audio):

        envelope = es.Envelope()
        temporal = es.Centroid(range=(float(len(audio)-1)/44100))

        return temporal(envelope(audio))

    #RMS
    def rms(self, audio):

        rmsFunc = es.RMS()
        return 20*math.log10(rmsFunc(audio))
