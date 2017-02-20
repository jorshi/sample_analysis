import sys
import essentia.standard as es
from sklearn.neighbors import NearestNeighbors
import numpy as np
import math
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Avg
from analysis.models import Sample, AnalysisZ 

class Command(BaseCommand):
    help = 'Mark Outliers'
    

    # Executes on command runtime
    def handle(self, *args, **options):
        
        dimensions = [
            'duration',
            'equal_loudness',
            'spectral_centroid',
            'temporal_centroid',
            'rms',
            'spectral_kurtosis',
            'pitch_salience'
        ]

        analysisObjects = AnalysisZ.objects.all()
        matrix = []
        order = []

        for item in analysisObjects:
            order.append(item.id)
            matrix.append([getattr(item, d) for d in dimensions])

        nOrder = np.array(order)
        nMatrix = np.array(matrix)
        
        print nMatrix
        
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
            analysisObject = AnalysisZ.objects.get(id=analysisId)
            sampleIds.append(analysisObject.sample)

        for sample in sampleIds:
            print sample.path
        

            
            
            
            

        


