import sys
import essentia.standard as es
import numpy as np
import math
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Avg, StdDev
from analysis.models import Sample, Analysis, AnalysisZ

class Command(BaseCommand):
    help = 'Calculate Z Scores '
    
    # Executes on command runtime
    def handle(self, *args, **options):
        
        fields = [
            'equal_loudness',
            'rms',
            'spectral_centroid',
            'spectral_centroid_1',
            'spectral_centroid_2',
            'temporal_centroid',
            'spectral_kurtosis',
            'pitch_salience'
        ]

        zData = {}

        kicks = Analysis.objects.filter(sample__sample_type="ki")
        snares = Analysis.objects.filter(sample__sample_type="sn")
        

        for field in fields:
            
            print "Calculating %s" % field
            
            # Separated z-score for kicks and snares
            kickAvg = kicks.aggregate(Avg(field))["%s__avg" % field]
            snareAvg = snares.aggregate(Avg(field))["%s__avg" % field]

            kickDev = kicks.aggregate(StdDev(field))["%s__stddev" % field]
            snareDev = snares.aggregate(StdDev(field))["%s__stddev" % field]
 
            for item in kicks:

                zScore = (getattr(item, field) - kickAvg) / kickDev
                
                if item.sample in zData:
                    setattr(zData[item.sample], field, zScore)
                else:
                    # Get zscore related object
                    try:
                        zData[item.sample] = AnalysisZ.objects.get(sample=item.sample)
                    except AnalysisZ.DoesNotExist:
                        zData[item.sample] = AnalysisZ(sample=item.sample)

                    setattr(zData[item.sample], field, zScore)

            for item in snares:
                zScore = (getattr(item, field) - snareAvg) / snareDev
                
                if item.sample in zData:
                    setattr(zData[item.sample], field, zScore)
                else:
                    # Get zscore related object
                    try:
                        zData[item.sample] = AnalysisZ.objects.get(sample=item.sample)
                    except AnalysisZ.DoesNotExist:
                        zData[item.sample] = AnalysisZ(sample=item.sample)

                    setattr(zData[item.sample], field, zScore)
        

        # Save create z score object
        for key in zData:
            zData[key].save()
