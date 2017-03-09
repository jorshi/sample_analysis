import sys
import essentia.standard as es
from sklearn.neighbors import NearestNeighbors
from sklearn import preprocessing
from sklearn.decomposition import PCA
import numpy as np
import math
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Avg
from analysis.models import Sample, Analysis, AnalysisMinMax 

#import plotly as py
#import plotly.graph_objs as go

class Command(BaseCommand):
    help = 'Perform Min Max Scaling on entire analysis set'
    

    # Executes on command runtime
    def handle(self, *args, **options):
        
        # Dimensions to consider in outlier calculation
        dimensions = [
            #'duration',
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
        analysisObjects = Analysis.objects.filter(outlier=False)
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
        
        # Min max scale
        scaled = preprocessing.MinMaxScaler().fit_transform(nMatrix)
        nMatrix = np.array(scaled)

        for i in range(len(sampleOrder)):
            try:
                newMinMax = AnalysisMinMax.objects.get(sample=sampleOrder[i])
            except AnalysisMinMax.DoesNotExist:
                newMinMax = AnalysisMinMax()
                newMinMax.sample = sampleOrder[i] 

            for j in range(len(nMatrix[i])):
                setattr(newMinMax, dimensions[j], nMatrix[i][j])  
            
            newMinMax.save()
