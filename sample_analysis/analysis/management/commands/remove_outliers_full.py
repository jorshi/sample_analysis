"""
Command for determining outliers from analysis and marking
them so they can be left out from further analysis. All analysis
features are first normalized and then the average distance to
the three nearest neighbours is used to determine whether a sample
is an outlier. If the distance is above a set threshold then that
sample is marked as an outlier.

    Usage: python ./manage.py remove_outliers sample_type
"""

import sys
from sklearn.neighbors import NearestNeighbors
from sklearn import preprocessing
import numpy as np
from django.core.management.base import BaseCommand, CommandError
from analysis.models import Sample, Analysis, AnalysisFull


class Command(BaseCommand):
    help = 'Mark Outliers'

    # Distance threshold for determining an outlier
    THRESH = 1.0

    # Override of the add_argument method
    def add_arguments(self, parser):

        # Required argument for the type of analysis to run
        parser.add_argument('sample_type', nargs=1, type=str)
        parser.add_argument('window_length', nargs=1, type=int)


    # Executes on command runtime
    def handle(self, *args, **options):

        choices = [x[0] for x in Sample.SAMPLE_TYPE_CHOICES]
        if options['sample_type'][0] not in choices:
            print "Sample type must by one of %s" % choices
            sys.exit(1)

        # Dimensions to consider in outlier calculation

        dimensions = [
            'bark_1_mean','bark_2_mean','bark_3_mean','bark_4_mean','bark_5_mean','bark_6_mean','bark_7_mean',
            'bark_8_mean','bark_9_mean','bark_10_mean','bark_11_mean','bark_12_mean','bark_13_mean','bark_14_mean',
            'bark_15_mean','bark_16_mean','bark_17_mean','bark_18_mean','bark_19_mean','bark_20_mean','bark_21_mean',
            'bark_22_mean','bark_23_mean','bark_24_mean','bark_25_mean','bark_26_mean','bark_27_mean',
            'bark_kurtosis', 'bark_skewness', 'bark_spread',
            'hfc',
            'mfcc_1_mean','mfcc_2_mean','mfcc_3_mean','mfcc_4_mean','mfcc_5_mean','mfcc_6_mean','mfcc_7_mean',
            'mfcc_8_mean','mfcc_9_mean','mfcc_10_mean','mfcc_11_mean','mfcc_12_mean','mfcc_13_mean',
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
            'spectral_spread'
        ]

        # Get all the samples
        analysisObjects = AnalysisFull.objects.filter(
            window_length=options['window_length'][0],
            sample__sample_type=options['sample_type'][0],
            sample__exclude=False,
            sample__kit__sample_pack__exclude=False,
        )
        matrix = []
        order = []

        # Create a numpy matrix of the analyis objects
        for item in analysisObjects:
            order.append(item.id)
            matrix.append([getattr(item, d) for d in dimensions])
        
        nOrder = np.array(order)
        nMatrix = np.array(matrix)

        # Scale everything
        #nMatrix = preprocessing.scale(nMatrix)
        minMaxScaler = preprocessing.MinMaxScaler()
        nMatrix = minMaxScaler.fit_transform(nMatrix)

        # Remove outliers based on nearest neighbor calulcations
        nbrs = NearestNeighbors(n_neighbors=4, algorithm='ball_tree').fit(nMatrix)
        distances, indices = nbrs.kneighbors(nMatrix)

        # Average distance of three nearest neighbours. The first neighbour is the
        # sample itself which will always have a distance of zero. Not including
        # that in the average
        averageDistance = []
        for d in distances:
            averageDistance.append(np.average(d[1:]))

        # Determine outliers and save the ids of the analysis objects to an array
        x = np.array(averageDistance)
        condList = [x > self.THRESH]
        choice = [x]
        rejects = np.select(condList, choice)
        rejectSamples = nOrder[np.nonzero(rejects)]
    
        print rejectSamples
        sys.exit()
        
        # Mark outliers and update in DB
        for analysisId in rejectSamples:
            analysisObject = Analysis.objects.get(id=analysisId)
            analysisObject.outlier = True
            analysisObject.save()

        print "%s outlier(s) found and marked" % len(rejectSamples)
