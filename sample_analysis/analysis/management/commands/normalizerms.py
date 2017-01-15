import sys
import essentia.standard as es
import math
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Avg
from analysis.models import Sample, Analysis 

class Command(BaseCommand):
    help = 'Normalize RMS values'
    
    # Executes on command runtime
    def handle(self, *args, **options):
        
        a = Analysis.objects.all().aggregate(rms_avg=Avg('rms'))
        for analysis in Analysis.objects.all():
            analysis.rms = analysis.rms - a['rms_avg']
            analysis.save()
