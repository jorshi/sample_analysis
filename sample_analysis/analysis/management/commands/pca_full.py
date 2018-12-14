"""
Command line tool for running Primary Component Analysis on
analysis objects of a selected sample type

usage:
    python ./manage.py pca sample_type
"""

import sys
import numpy as np
import math
import pandas as pd
from sklearn import preprocessing
from sklearn.decomposition import PCA
import scipy.stats as stats
from django.core.management.base import BaseCommand, CommandError
from analysis.models import Sample, AnalysisPCA, AnalysisFull, PCAStat


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

        # Get all the analysis objects for a particular sample type
        analysisObjects = AnalysisFull.objects.filter(
            window_length=options['window_length'][0],
            sample__sample_type=options['sample_type'][0],
            window_start=options['window_start'][0],
            sample__exclude=False,
            #outlier=False
        )
        matrix = []
        sampleOrder = []

        # Create a numpy matrix of the analyis objects. Also, keep track of the sample order
        # as they are retrieved from the database by storing references to the sample in the
        # sampleOrder list
        for item in analysisObjects:
            sampleOrder.append(item.sample)
            matrix.append([getattr(item, d) for d in dimensions])

        nMatrix = np.array(matrix)
        self.bartlett(nMatrix)

        # Scale everything
        nMatrix = preprocessing.scale(nMatrix)
        gKMO, vKMO = self.globalKMO(nMatrix)

        # Uncomment for removal of dimensions that don't have a KMO greater than 0.6
        #retain = np.where(vKMO > 0.6)
        #nMatrix = nMatrix[:,retain[0]]
        #print "Removing %s" % np.array(dimensions)[np.where(vKMO <= 0.6)[0]]

        g2KMO, v2KMO = self.globalKMO(nMatrix)
        print stats.levene(*nMatrix)

        print g2KMO

        # Perform PCA
        pca = PCA(n_components=4)
        pca.fit(nMatrix)
        y = pca.transform(nMatrix)

        # Save the calculated PCA dimensions as new objects related to corresponding sample
        for i in range(len(y)):
            try:
                newPca = AnalysisPCA.objects.get(
                    sample=sampleOrder[i],
                    window_length=options['window_length'][0],
                    window_start=options['window_start'][0]
                )
            except AnalysisPCA.DoesNotExist:
                newPca = AnalysisPCA(
                    sample = sampleOrder[i],
                    window_length = options['window_length'][0],
                    window_start = options['window_start'][0]
                )
            for j in range(len(y[i])):
                setattr(newPca, "dim_%s" % (j + 1), y[i][j])
            newPca.save()

        print "Explained Variance Ratio"
        print pca.explained_variance_ratio_
        print sum(pca.explained_variance_ratio_[0:2])*100

        try:
            newPcaStat = PCAStat.objects.get(
                sample_type=options['sample_type'][0],
                window_length=options['window_length'][0],
                window_start=options['window_start'][0]
            )
        except PCAStat.DoesNotExist:
            newPcaStat = PCAStat(
                sample_type=options['sample_type'][0],
                window_length = options['window_length'][0],
                window_start = options['window_start'][0]
            )

        for j in range(len(pca.explained_variance_ratio_)):
            setattr(newPcaStat, "dim_%s_variance_ratio" % (j + 1), pca.explained_variance_ratio_[j])
        newPcaStat.variance_sum_2d = sum(pca.explained_variance_ratio_[0:2])*100
        newPcaStat.save()

        print "\nExplained Variance"
        print pca.explained_variance_

        print "\nComponent Weightings"
        #print pca.components_
        #np.savetxt('output.csv', pca.components_, delimiter=",")
        #print self.varimax(pca.components_)


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

    
    """
    Bartlett's Test of Sphericity
    """
    def bartlett(self, matrix):

        d = pd.DataFrame(matrix)
        dCorr = d.corr()

        n, p = matrix.shape

        chi2 = -(n - 1 - ((2*p + 5) / 6)) * np.log(np.linalg.det(dCorr.values))
        ddl = p*(p-1)/2
    
        print chi2
        print ddl
        pvalue = stats.chi2.pdf(chi2, ddl)

        print pvalue

    def globalKMO(self, matrix):

        dCorr = np.corrcoef(matrix, rowvar=False)

        # Inverse Correlation Matrix
        corrInv = np.linalg.inv(dCorr)

        corrInvRows, corrInvCols = corrInv.shape
        
        A = np.ones(corrInv.shape)

        for i in range(0, corrInvRows, 1):
            for j in range(i, corrInvCols, 1):
                A[i,j] = -corrInv[i,j] / (math.sqrt(corrInv[i,i] * corrInv[j,j]))
                A[j,i] = A[i,j]

        matrixCorr = np.asarray(dCorr)

        kmoNum = np.sum(np.square(matrixCorr)) - np.sum(np.square(np.diagonal(matrixCorr)))
        kmoDenom = kmoNum + (np.sum(np.square(A)) - np.sum(np.square(np.diagonal(A))))

        # Per Variable
        kmoVars = np.zeros(len(dCorr))

        for j in range(0, len(dCorr)):
            kmoJNum = np.sum(np.square(matrixCorr[:,j])) - np.square(matrixCorr[j,j])
            kmoJDenom = kmoJNum + (np.sum(np.square(A[:,j])) - np.square(A[j,j]))
            kmoVars[j] = kmoJNum / kmoJDenom

        return (kmoNum / kmoDenom, kmoVars)


    def varimax(self, Phi, gamma = 1.0, q = 20, tol = 1e-6):
        from numpy import eye, asarray, dot, sum, diag
        from numpy.linalg import svd
        p,k = Phi.shape
        R = eye(k)
        d=0.0
        for i in xrange(q):
            d_old = d
            Lambda = dot(Phi, R)
            u,s,vh = svd(dot(Phi.T,asarray(Lambda)**3 - (gamma/p) * dot(Lambda, diag(diag(dot(Lambda.T,Lambda))))))
            R = dot(u,vh)
            d = sum(s)
            if d/d_old < tol: break
        return dot(Phi, R)
