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
from analysis.models import Sample, Analysis, AnalysisPCA


class Command(BaseCommand):
    help = 'Principal Component Analysis'

    # Override of the add_argument method
    def add_arguments(self, parser):

        # Required argument for the type of analysis to run
        parser.add_argument('sample_type', nargs=1, type=str)


    # Executes on command runtime
    def handle(self, *args, **options):
        
        choices = [x[0] for x in Sample.SAMPLE_TYPE_CHOICES]
        if options['sample_type'][0] not in choices:
            print "Sample type must by one of %s" % choices
            sys.exit(1)

        # Dimensions to consider in PCA
        dimensions = [
            'equal_loudness',
            'rms',
            'spectral_centroid',
            'spectral_centroid_1',
            'spectral_centroid_2',
            'temporal_centroid',
            'spectral_kurtosis',
            'pitch_salience'
        ]

        # Get all the analysis objects for a particular sample type
        analysisObjects = Analysis.objects.filter(
            sample__sample_type=options['sample_type'][0],
            outlier=False
        )
        matrix = []
        sampleOrder = []

        # Create a numpy matrix of the analyis objects. Also, keep track of the sample order
        # as they are retrieved from the database by storing references to the sample in the
        # sampleOrder list
        for item in analysisObjects:
            sampleOrder.append(item.sample)
            matrix.append([getattr(item, d) for d in dimensions])

        # Scale everything
        nMatrix = np.array(matrix)
        nMatrix = preprocessing.scale(nMatrix)

        # Perform PCA
        pca = PCA()
        pca.fit(nMatrix)
        y = pca.transform(nMatrix)

        # Save the calculated PCA dimensions as new objects related to corresponding sample
        for i in range(len(y)):
            try:
                newPca = AnalysisPCA.objects.get(sample=sampleOrder[i])
            except AnalysisPCA.DoesNotExist:
                newPca = AnalysisPCA()
                newPca.sample = sampleOrder[i]
            for j in range(len(y[i])):
                setattr(newPca, "dim_%s" % (j + 1), y[i][j])
            newPca.save()

        print "Explained Variance Ratio"
        print pca.explained_variance_ratio_

        print "\nExplained Variance"
        print pca.explained_variance_

        print "\nComponent Weightings"
        print pca.components_
