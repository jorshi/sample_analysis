"""
Command for running drum machine classification on
dimension reduced sample space.

Note that the drum machines are hard coded into this file,
they will need to be updated by the user.

usage:
    python ./manage.py classifier dm [method] [sample_type] [window_length] [window_start]
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
from analysis.models import Sample, AnalysisPCA, AnalysisFull, Classification, Manifold


class Command(BaseCommand):
    help = 'Drum Machine Classification after Dimension Reduction'

    # Override of the add_argument method
    def add_arguments(self, parser):

        # Required argument for the type of analysis to run
        parser.add_argument('reduction_method', nargs=1, type=str)
        parser.add_argument('sample_type', nargs=1, type=str)
        parser.add_argument('window_length', nargs=1, type=int)
        parser.add_argument('window_start', nargs=1, type=int)

    # Executes on command runtime
    def handle(self, *args, **options):

        choices = [x[0] for x in Sample.SAMPLE_TYPE_CHOICES]
        if options['sample_type'][0] not in choices:
            print "Sample type must by one of %s" % choices
            sys.exit(1)


        methods = [x[0] for x in Manifold.MANIFOLD_METHODS]
        methods.append('pca')
        if options['reduction_method'][0] not in methods:
            print "Reduction method must be one of %s" % methods
            sys.exit(1)

        dimensions = ['dim_1', 'dim_2']

        # Get all the analysis objects for a particular sample type
        if options['sample_type'][0] == 'ki':
            if options['reduction_method'][0] != 'pca':
                samples = Manifold.objects.filter(
                    method=options['reduction_method'][0],
                    window_length=options['window_length'][0],
                    window_start=options['window_start'][0],
                    sample__sample_type='ki',
                    sample__kit__sample_pack__in=[155,100,75,92,132,144],
                )
            else:
                samples = AnalysisPCA.objects.filter(
                    window_length=options['window_length'][0],
                    window_start=options['window_start'][0],
                    sample__sample_type='ki',
                    sample__kit__sample_pack__in=[155,100,75,92,132,144],
                )

        elif options['sample_type'][0] == 'sn':
            if options['reduction_method'][0] != 'pca':
                samples = Manifold.objects.filter(
                    method=options['reduction_method'][0],
                    window_length=options['window_length'][0],
                    window_start=options['window_start'][0],
                    sample__sample_type='sn',
                    sample__kit__sample_pack__in=[155,100,35,92,132,48,144,197],
                )
            else:
                samples = AnalysisPCA.objects.filter(
                    window_length=options['window_length'][0],
                    window_start=options['window_start'][0],
                    sample__sample_type='sn',
                    sample__kit__sample_pack__in=[155,100,35,92,132,48,144,197],
                )
        else:
            self.stderr.write("Sample type must be 'ki' or 'sn'")
            exit()

        classificationId = "Drum Machine: %s" % options['reduction_method'][0]

        try:
            newClassification = Classification.objects.get(
                info=classificationId,
                window_length=options['window_length'][0],
                window_start=options['window_start'][0],
                sample_type=options['sample_type'][0],
            )
        except Classification.DoesNotExist:
            newClassification = Classification(
                info=classificationId,
                window_length=options['window_length'][0],
                window_start=options['window_start'][0],
                sample_type=options['sample_type'][0],
            )

        data = []
        target = []

        # Create a numpy matrix of the analyis objects. Also, keep track of the sample order
        # as they are retrieved from the database by storing references to the sample in the
        # sampleOrder list
        for item in samples:
            target.append(item.sample.kit.sample_pack.id)
            data.append([getattr(item, d) for d in dimensions])

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
        newClassification.baseline = accuracy_score(target, pred)
        print newClassification.baseline
        print confusion_matrix(target, pred)

        print "\nRunning SVC Classifier"
        svc = SVC()
        pred = cross_val_predict(svc, dataScaled, target, cv=10)
        newClassification.svc = accuracy_score(target, pred)
        average = newClassification.svc
        print newClassification.svc
        print confusion_matrix(target, pred)

        print "\nRunning Perceptron Classifier"
        perceptron = Perceptron()
        pred = cross_val_predict(perceptron, dataScaled, target, cv=10)
        newClassification.perceptron = accuracy_score(target, pred)
        average = average + newClassification.perceptron
        print newClassification.perceptron
        print confusion_matrix(target, pred)

        print "\nRunning Random Forest Classifier"
        randomForest = RandomForestClassifier()
        pred = cross_val_predict(randomForest, dataScaled, target, cv=10)
        newClassification.random_forest = accuracy_score(target, pred)
        average = average + newClassification.random_forest
        print newClassification.random_forest
        print confusion_matrix(target, pred)

        newClassification.average = average / 3.0
        print "\nAverage Classification Score: %s" % newClassification.average

        newClassification.save()
