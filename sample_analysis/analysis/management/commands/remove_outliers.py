import sys
import essentia.standard as es
from sklearn.neighbors import NearestNeighbors
from sklearn import preprocessing
import numpy as np
import math
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Avg
from analysis.models import Sample, Analysis, AnalysisRobustScale 

class Command(BaseCommand):
    help = 'Mark Outliers'
    

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
            sample__sample_type='sn', 
            sample__exclude=False,
            sample__kit__sample_pack__exclude=False,
        )
        matrix = []
        order = []
        sampleOrder = []

        # Create a numpy matrix of the analyis
        for item in analysisObjects:
            order.append(item.id)
            sampleOrder.append(item.sample)
            matrix.append([getattr(item, d) for d in dimensions])

        nOrder = np.array(order)
        nMatrix = np.array(matrix)
        
        # Scale erything
        scaled = preprocessing.scale(nMatrix)
        nMatrix = np.array(scaled)

        # Remove outliers based on nearest neighbor calulcations
        nbrs = NearestNeighbors(n_neighbors=4, algorithm='ball_tree').fit(nMatrix)
        distances, indices = nbrs.kneighbors(nMatrix)

        averageDistance = []
        for d in distances:
            averageDistance.append(np.average(d[1:]))
        
        x = np.array(averageDistance)
        condList = [x > 2.5]
        choice = [x]

        rejects = np.select(condList, choice)
        rejectSamples = nOrder[np.nonzero(rejects)]

        sampleIds = []
        for analysisId in rejectSamples:
            analysisObject = Analysis.objects.get(id=analysisId)
            analysisObject.outlier = True
            analysisObject.save()
