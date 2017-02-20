import sys
import essentia.standard as es
import math
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Avg
from analysis.models import Sample, Analysis 

class Command(BaseCommand):
    help = 'Save duration in analysis object'
    
    # Executes on command runtime
    def handle(self, *args, **options):
        
        objects = Analysis.objects.filter(outlier=False)
        for analysis in objects:
            analysis.duration = analysis.sample.stop_time - analysis.sample.start_time
            analysis.save()
