
import sys
import random
from random import choice

import matplotlib.pyplot as plt
import numpy as np
from numpy.random import rand
from sklearn import preprocessing
from sklearn.neighbors import NearestNeighbors

from django.core.management.base import BaseCommand, CommandError
from analysis.models import Sample, SamplePack, AnalysisPCA, AnalysisFull, PCAStat, Manifold


class Command(BaseCommand):

    # Override of the add_argument method
    def add_arguments(self, parser):

        # Required argument for the type of analysis to run
        parser.add_argument('reduction_method', nargs=1, type=str)
        parser.add_argument('sample_type', nargs=1, type=str)
        parser.add_argument('window_length', nargs=1, type=int)
        parser.add_argument('window_start', nargs=1, type=int)
        parser.add_argument('--reference', nargs=1, type=int, default=None)

    # Executes on command runtime
    def handle(self, *args, **options):

        choices = [x[0] for x in Sample.SAMPLE_TYPE_CHOICES]
        if options['sample_type'][0] not in choices:
            print("Sample type must by one of %s" % choices)
            sys.exit(1)

        methods = [x[0] for x in Manifold.MANIFOLD_METHODS]
        methods.append('pca')
        methods.append('none')
        if options['reduction_method'][0] not in methods:
            print("Reduction method must be one of %s" % methods)
            sys.exit(1)

        # Get all the embedded samples for a particular sample type & reduction method type in a sample pack
        if options['reduction_method'][0] == 'none':
            samples = AnalysisFull.objects.filter(
                window_length=options['window_length'][0],
                window_start=options['window_start'][0],
                sample__sample_type=options['sample_type'][0],
            )
        elif options['reduction_method'][0] != 'pca':
            samples = Manifold.objects.filter(
                method=options['reduction_method'][0],
                window_length=options['window_length'][0],
                window_start=options['window_start'][0],
                sample__sample_type=options['sample_type'][0],
            )
        else:
            samples = AnalysisPCA.objects.filter(
                window_length=options['window_length'][0],
                window_start=options['window_start'][0],
                sample__sample_type=options['sample_type'][0],
            )


        # Create numpy array of samples
        matrix = []
        sampleOrder = []
        refIndex = random.randint(0, len(samples))
        index = 0

        if options['reduction_method'][0] == 'none':
            for item in samples:
                sampleOrder.append(item.sample)
                matrix.append([getattr(item, d) for d in self.get_dimensions()])

            matrix = np.array(matrix)
            matrix = preprocessing.scale(matrix)

        else:
            for item in samples:
                if options['reference'] and item.sample_id == options['reference'][0]:
                    refIndex = index
                sampleOrder.append(item.sample)
                matrix.append([item.dim_1, item.dim_2])
                index = index + 1

            matrix = np.array(matrix)

        nbrs = NearestNeighbors(n_neighbors=matrix.shape[0], algorithm='brute').fit(matrix)
        distances, indices = nbrs.kneighbors(matrix)


        print("Reference id: %s" % samples[refIndex].sample_id)
        nearestSamples = []
        for nearest in indices[refIndex][0:6]:
            nearestSamples.append(samples[int(nearest)].sample_id)

        midSample = indices[refIndex][int(matrix.shape[0]/2.0)]
        midSample = samples[int(midSample)].sample_id

        farSample = indices[refIndex][-1]
        farSample = samples[int(farSample)].sample_id

        samples = nearestSamples.copy()
        samples.append(midSample)
        samples.append(farSample)

        sampleObjs = Sample.objects.filter(id__in = samples)
        sampleMap = {}
        for item in sampleObjs:
            sampleMap[item.id] = item

        print("Nearest:")
        for id in nearestSamples:
            print(id, sampleMap[id].path)

        print("Mid Far:")
        print(midSample, sampleMap[midSample].path)

        print("Far:")
        print(farSample, sampleMap[farSample].path)








    def get_dimensions(self):

        return [
            'bark_1_mean','bark_2_mean','bark_3_mean','bark_4_mean','bark_5_mean','bark_6_mean','bark_7_mean',
            'bark_8_mean','bark_9_mean','bark_10_mean','bark_11_mean','bark_12_mean','bark_13_mean','bark_14_mean',
            'bark_15_mean','bark_16_mean','bark_17_mean','bark_18_mean','bark_19_mean','bark_20_mean','bark_21_mean',
            'bark_22_mean','bark_23_mean','bark_24_mean','bark_25_mean','bark_26_mean','bark_27_mean',
            'bark_1_dev','bark_2_dev','bark_3_dev','bark_4_dev','bark_5_dev','bark_6_dev','bark_7_dev',
            'bark_8_dev','bark_9_dev','bark_10_dev','bark_11_dev','bark_12_dev','bark_13_dev','bark_14_dev',
            'bark_15_dev','bark_16_dev','bark_17_dev','bark_18_dev','bark_19_dev','bark_20_dev','bark_21_dev',
            'bark_22_dev','bark_23_dev','bark_24_dev','bark_25_dev','bark_26_dev','bark_27_dev',
            'bark_kurtosis', 'bark_skewness', 'bark_spread',
            'bark_kurtosis_dev', 'bark_skewness_dev', 'bark_spread_dev',
            'hfc', 'hfc_dev',
            'mfcc_1_mean','mfcc_2_mean','mfcc_3_mean','mfcc_4_mean','mfcc_5_mean','mfcc_6_mean','mfcc_7_mean',
            'mfcc_8_mean','mfcc_9_mean','mfcc_10_mean','mfcc_11_mean','mfcc_12_mean','mfcc_13_mean',
            'mfcc_1_dev','mfcc_2_dev','mfcc_3_dev','mfcc_4_dev','mfcc_5_dev','mfcc_6_dev','mfcc_7_dev',
            'mfcc_8_dev','mfcc_9_dev','mfcc_10_dev','mfcc_11_dev','mfcc_12_dev','mfcc_13_dev',
            'temporal_centroid',
            'rms',
            'lat',
            'zero_crossing_rate',
            'pitch_salience',
            'spectral_complexity',
            'spectral_decrease',
            'spectral_energy',
            'spectral_energyband_low',
            'spectral_energyband_middle_low',
            'spectral_energyband_middle_high',
            'spectral_energyband_high',
            'spectral_flatness_db',
            'spectral_flux',
            'spectral_rms',
            'spectral_rolloff',
            'spectral_strongpeak',
            'inharmonicity',
            'tristimulus_1',
            'tristimulus_2',
            'tristimulus_3',
            'spectral_centroid',
            'spectral_kurtosis',
            'spectral_spread',
            'zero_crossing_rate_dev',
            'pitch_salience_dev',
            'spectral_complexity_dev',
            'spectral_decrease_dev',
            'spectral_energy_dev',
            'spectral_energyband_low_dev',
            'spectral_energyband_middle_low_dev',
            'spectral_energyband_middle_high_dev',
            'spectral_energyband_high_dev',
            'spectral_flatness_db_dev',
            'spectral_flux_dev',
            'spectral_rms_dev',
            'spectral_rolloff_dev',
            'spectral_strongpeak_dev',
            'inharmonicity_dev',
            'tristimulus_1_dev',
            'tristimulus_2_dev',
            'tristimulus_3_dev',
            'spectral_centroid_dev',
            'spectral_kurtosis_dev',
            'spectral_spread_dev'
        ]
