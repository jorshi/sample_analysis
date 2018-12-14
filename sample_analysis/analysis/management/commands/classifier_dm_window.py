"""
Version of classifier script that classifies different drum machines
using the max variance method developed here that maximizes the
variance across samples for each sample by selecting a different
window length and size for each feature.

usage:
    python ./manage.py classifier_dm_window.py [sample_type] [window_length]
"""

import sys
import numpy as np
from sklearn import preprocessing
from sklearn.metrics import confusion_matrix, accuracy_score 
from sklearn.model_selection import cross_val_predict
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.linear_model import Perceptron
from sklearn.ensemble import RandomForestClassifier
from sklearn.dummy import DummyClassifier
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count, Variance
from analysis.models import Sample, AnalysisPCA, AnalysisFull


class Command(BaseCommand):
    help = """Drum Machine Classifier using Maximum Variance - Please note that the drum machines (samplepacks) are hard
    coded into the python management file, please see the python file for this command
    /analysis/management/command/classifier_dm_window.py"""

    # Override of the add_argument method
    def add_arguments(self, parser):

        # Required argument for the type of analysis to run
        parser.add_argument('sample_type', nargs=1, type=str)
        parser.add_argument('window_length', nargs=1, type=int)
        parser.add_argument('window_start', nargs=1, type=int)

    # Executes on command runtime
    def handle(self, *args, **options):

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

        if options['sample_type'][0] == 'ki':

            analysisObjects = AnalysisFull.objects.filter(
                window_length=options['window_length'][0],
                window_start=options['window_start'][0],
                sample__sample_type='ki',
                sample__kit__sample_pack__in=[155,100,75,92,132,144],
                sample__exclude=False,
            )

            analysisVar = AnalysisFull.objects.filter(sample__sample_type='ki')

        elif options['sample_type'][0] == 'sn':

            analysisObjects = AnalysisFull.objects.filter(
                window_length=options['window_length'][0],
                window_start=options['window_start'][0],
                sample__sample_type='sn',
                sample__kit__sample_pack__in=[155,100,35,92,132,48,144,197],
                sample__exclude=False,
            )

            analysisVar = AnalysisFull.objects.filter(sample__sample_type='sn')

        else:
            self.stderr.write("Sample type must be 'ki' or 'sn'")
            exit()

        maxVarWindows = {}
        count = {}
        for feature in dimensions:
            variance = analysisVar.values('window_length', 'window_start').annotate(Variance(feature))
            arg = np.argmax([item[feature + '__variance'] for item in variance])
            
            if (variance[arg]['window_length'], variance[arg]['window_start']) in count:
                count[(variance[arg]['window_length'], variance[arg]['window_start'])] += 1
            else:
                count[(variance[arg]['window_length'], variance[arg]['window_start'])] = 1




            maxVarWindows[feature] = (variance[arg]['window_length'], variance[arg]['window_start'])

        data = []
        target = []

        # Create a numpy matrix of the analyis objects. Also, keep track of the sample order
        # as they are retrieved from the database by storing references to the sample in the
        # sampleOrder list
        for item in analysisObjects:
            target.append(item.sample.kit.sample_pack.id)
            sampleObjs = [obj for obj in analysisVar.filter(sample_id=item.sample_id)]
            windowMap = {(a.window_length, a.window_start):a for a in sampleObjs} 
            features = []
            for feature in dimensions:
                aObj = windowMap[maxVarWindows[feature]]
                features.append(getattr(aObj, feature))
            data.append(features)

        (unique, counts) = np.unique(target, return_counts=True)

        print "\nClass ids: %s" % unique
        print "Items per class: %s" % counts
        print "Total items being classified: %s" % sum(counts)
        
        # Scale everything
        dataScaled = np.array(data)
        minMaxScaler = preprocessing.MinMaxScaler()
        dataScaled = minMaxScaler.fit_transform(dataScaled)

        print "\nBaseline"
        dummyClass = DummyClassifier()
        pred = cross_val_predict(dummyClass, dataScaled, target, cv=10)
        print accuracy_score(target, pred)
        print confusion_matrix(target, pred)

        print "\nRunning SVC Classifier"
        svc = SVC()
        pred = cross_val_predict(svc, dataScaled, target, cv=10)
        average = accuracy_score(target, pred)
        print accuracy_score(target, pred)
        print confusion_matrix(target, pred)

        print "\nRunning Perceptron Classifier"
        perceptron = Perceptron()
        pred = cross_val_predict(perceptron, dataScaled, target, cv=10)
        average = average + accuracy_score(target, pred)
        print accuracy_score(target, pred)
        print confusion_matrix(target, pred)

        print "\nRunning Random Forest Classifier"
        randomForest = RandomForestClassifier()
        pred = cross_val_predict(randomForest, dataScaled, target, cv=10)
        average = average + accuracy_score(target, pred)
        print accuracy_score(target, pred)
        print confusion_matrix(target, pred)

        print "\nAverage Classification Score: %s" % (average / 3.0)

