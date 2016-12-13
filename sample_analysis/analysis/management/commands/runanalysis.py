import sys
import essentia.standard as es
from django.core.management.base import BaseCommand, CommandError
from analysis.models import Sample, Analysis 

class Command(BaseCommand):
    help = 'Run Essentia Analysis on Sample Set'
    loaders = {
        'mono': es.MonoLoader,
        'eqloud': es.EqloudLoader
    }
    
    # Override of the add_argument method
    def add_arguments(self, parser):

        # Required argument for the type of analysis to run
        parser.add_argument('analysis_type', nargs='+', type=str)

        # Optional argument to specify the type of essentia loader
        parser.add_argument(
            '--loader',
            dest='loader',
            default = 'mono',
            help = 'Specify the type of essentia audio loader'
        )

    
    # Executes on command runtime
    def handle(self, *args, **options):
        
        if options['loader']:
            try:
                self.loader = self.loaders[options['loader']]
            except KeyError:
                raise CommandError(
                    'Invalid loader type. Select from %s' % self.loaders.keys()
                )

        # Different options for analysis functions
        functions = {
            'loudness': self.loudness,
            'equalloudness': self.equalLoudness,
        }

        # Try running analysis function
        try:
            function = functions.get(options['analysis_type'][0])
        except TypeError:
            raise CommandError(
                'Analysis type does not exists. Select from %s' % functions.keys()
            )

        function()
        self.stdout.write(self.style.SUCCESS('Complete'))
    

    # Run Essentia Loudness with the Equal Loudess Loader
    def equalLoudness(self):
        self.loudness(True)


    # Run Essentia Loudness Analysis on Entire Sample Set
    def loudness(self, equal=False):

        if equal:
            self.loader = self.loaders['eqloud']
        else:
            self.loader = self.loaders['mono']

        samples = Sample.objects.all()
        numSamples = len(samples)
        loudnessAnalysis = es.Loudness()

        self.stdout.write("Running loudness analysis on %s samples. " % numSamples)
        i = 0.0

        for sample in samples:

            # Get audio and run loudness analysis
            loader = self.loader(filename=sample.path)
            audio = loader()
            loudness = loudnessAnalysis(audio)

            # Get analysis object for this sample and save
            try:
                analysisObject = Analysis.objects.get(sample=sample)
            except Analysis.DoesNotExist:
                analysisObject = Analysis(sample=sample)

            if equal:
                analysisObject.equal_loudness = loudness
            else:
                analysisObject.loudness = loudness
            analysisObject.save()

            i = i + 1
            self.stdout.write("\t\t%2.2f%% Complete" % (100.0*(i/float(numSamples))), ending='\r')
            self.stdout.flush()

        self.stdout.write("\r", ending='\r')
        self.stdout.flush()
