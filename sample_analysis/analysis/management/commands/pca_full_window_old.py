"""
Command line tool for running Primary Component Analysis on
analysis objects of a selected sample type

usage:
    python ./manage.py pca sample_type
"""

import sys
import numpy as np
from sklearn import preprocessing
from sklearn.decomposition import PCA
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count, Variance
from analysis.models import Sample, Analysis, AnalysisPCA, AnalysisFull


class Command(BaseCommand):
    help = 'Principal Component Analysis'

    # Override of the add_argument method
    def add_arguments(self, parser):

        # Required argument for the type of analysis to run
        parser.add_argument('sample_type', nargs=1, type=str)
        parser.add_argument('window_length', nargs=1, type=int)
        parser.add_argument('window_start', nargs=1, type=int)

    # Executes on command runtime
    def handle(self, *args, **options):
        
        choices = [x[0] for x in Sample.SAMPLE_TYPE_CHOICES]
        if options['sample_type'][0] not in choices:
            print "Sample type must by one of %s" % choices
            sys.exit(1)

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

        # Get all the analysis objects for a particular sample type
        analysisObjects = AnalysisFull.objects.filter(
            window_length=options['window_length'][0],
            window_start=options['window_start'][0],
            sample__sample_type=options['sample_type'][0],
            sample__exclude=False,
            #outlier=False
        )

        print len(analysisObjects)
        matrix = []
        sampleOrder = []

        analysisVar = AnalysisFull.objects.filter(sample__sample_type=options['sample_type'][0])

        maxVarWindows = {}
        for feature in dimensions:
            variance = analysisVar.values('window_length', 'window_start').annotate(Variance(feature))
            arg = np.argmax([item[feature + '__variance'] for item in variance])
            maxVarWindows[feature] = (variance[arg]['window_length'], variance[arg]['window_start'])

        # Create a numpy matrix of the analyis objects. Also, keep track of the sample order
        # as they are retrieved from the database by storing references to the sample in the
        # sampleOrder list
        for item in analysisObjects:
            sampleOrder.append(item.sample)
            sampleObjs = [obj for obj in analysisVar.filter(sample_id=item.sample_id)]
            windowMap = {(a.window_length,a.window_start):a for a in sampleObjs} 
            features = []
            for feature in dimensions:
                aObj = windowMap[maxVarWindows[feature]]
                features.append(getattr(aObj, feature))
            matrix.append(features)

        # Scale everything
        nMatrix = np.array(matrix)
        nMatrix = preprocessing.scale(nMatrix)

        # Perform PCA
        pca = PCA()
        pca.fit(nMatrix)
        y = pca.transform(nMatrix)

        # Save the calculated PCA dimensions as new objects related to corresponding sample
        #for i in range(len(y)):
        #    try:
        #        newPca = AnalysisPCA.objects.get(sample=sampleOrder[i])
        #    except AnalysisPCA.DoesNotExist:
        #        newPca = AnalysisPCA()
        #        newPca.sample = sampleOrder[i]
        #    for j in range(len(y[i])):
        #        setattr(newPca, "dim_%s" % (j + 1), y[i][j])
        #    newPca.save()

        print "Explained Variance Ratio"
        print pca.explained_variance_ratio_

        print "\nExplained Variance"
        print pca.explained_variance_

        print "\nComponent Weightings"
        print pca.components_
        np.savetxt('output.csv', pca.components_, delimiter=",")

        print "\nTop Components"
        dim1Top = np.argsort(np.absolute(pca.components_[0]))[::-1]
        dim2Top = np.argsort(np.absolute(pca.components_[1]))[::-1]

        print "\nDimension 1"
        for i in range(5):
            sys.stdout.write("'%s' " % np.array(dimensions)[dim1Top[i]])
        print ""
        print pca.components_[0][dim1Top]

        print "\nDimension 2"
        for i in range(5):
            sys.stdout.write("'%s' " % np.array(dimensions)[dim2Top[i]])
        print ""
        print pca.components_[0][dim2Top]

