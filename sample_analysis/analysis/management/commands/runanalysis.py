import sys
import essentia.standard as es
from django.core.management.base import BaseCommand, CommandError
from analysis.models import Sample, Analysis 

class Command(BaseCommand):
    help = 'Run Essentia Analysis on Sample Set'
    
    def add_arguments(self, parser):
        parser.add_argument('analysis_type', nargs='+', type=str)


    def handle(self, *args, **options):

        # Different options for analysis functions
        functions = {
            'loudness': self.loudness,
        }

        # Try running analysis function
        try:
            functions.get(options['analysis_type'][0])()
        except TypeError:
            raise CommandError(
                'Analysis type does not exists. Select from %s' % functions.keys()
            )


    def loudness(self):

        samples = Sample.objects.all()
        loudnessAnalysis = es.Loudness()

        for sample in samples:
            # Get audio and run loudness analysis
            loader = es.MonoLoader(filename=sample.path)
            audio = loader()
            loudness = loudnessAnalysis(audio)

            # Get analysis object for this sample and save
            try:
                analysisObject = Analysis.objects.get(sample=sample)
            except Analysis.DoesNotExist:
                analysisObject = Analysis(sample=sample)

            analysisObject.loudness = loudness
            analysisObject.save()
