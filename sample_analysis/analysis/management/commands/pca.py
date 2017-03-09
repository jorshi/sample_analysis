import sys
import essentia.standard as es
from sklearn.neighbors import NearestNeighbors
from sklearn import preprocessing
from sklearn.decomposition import PCA
import numpy as np
import math
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Avg
from analysis.models import Sample, Analysis, AnalysisRobustScale, AnalysisPCA, PCAComponents, PCAVariance  

#import plotly as py
#import plotly.graph_objs as go

class Command(BaseCommand):
    help = 'Principal Component Analysis'
    

    # Executes on command runtime
    def handle(self, *args, **options):
        
        # Dimensions to consider in PCA
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

        # Get all the analysis objects for a particular sample type
        analysisObjects = Analysis.objects.filter(
            sample__sample_type='sn', 
            outlier=False
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


        print pca.explained_variance_ratio_
        print pca.explained_variance_
        print pca.components_

        #py.offline.plot([trace], filename='plot2.html')

        
