"""
Command for determining outliers from analysis and marking
them so they can be left out from further analysis. All analysis
features are first normalized and then the average distance to
the three nearest neighbours is used to determine whether a sample
is an outlier. If the distance is above a set threshold then that
sample is marked as an outlier.

    Usage: python ./manage.py remove_outliers sample_type
"""

from sklearn.neighbors import NearestNeighbors
from sklearn import preprocessing
import numpy as np
from django.core.management.base import BaseCommand, CommandError
from analysis.models import Sample, Analysis


class Command(BaseCommand):
    help = 'Mark Outliers'

    # Distance threshold for determining an outlier
    THRESH = 2.5

    # Override of the add_argument method
    def add_arguments(self, parser):

        # Required argument for the type of analysis to run
        parser.add_argument('sample_type', nargs=1, type=str)


    # Executes on command runtime
    def handle(self, *args, **options):

        # Dimensions to consider in outlier calculation
        dimensions = [
            'duration',
            'equal_loudness',
            'rms',
            'spectral_centroid',
            'spectral_centroid_1',
            'spectral_centroid_2',
            'temporal_centroid',
            'spectral_kurtosis',
            'pitch_salience'
        ]

        # Get all the samples
        analysisObjects = Analysis.objects.filter(
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
        nMatrix = preprocessing.scale(nMatrix)

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

        # Mark outliers and update in DB
        for analysisId in rejectSamples:
            analysisObject = Analysis.objects.get(id=analysisId)
            analysisObject.outlier = True
            analysisObject.save()

        print "%s outlier(s) found and marked" % len(rejectSamples)
