import sys
import essentia.standard as es
import math
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
        analysisTypes = {
            'loudness': {
                'function': self.loudness,
                'loader': self.loaders['mono'],
            },
            'equal_loudness': {
                'function': self.loudness,
                'loader': self.loaders['eqloud'],
            },
            'spectral_centroid': {
                'function': self.spectral_centroid,
                'loader': self.loaders['eqloud'],
            },
            'temporal_centroid': {
                'function': self.temporal_centroid,
                'loader': self.loaders['eqloud'],
            },
            'rms': {
                'function': self.rms,
                'loader': self.loaders['mono'],
            },
            'spectral_kurtosis': {
                'function': self.spectral_kurtosis,
                'loader': self.loaders['eqloud'],
            }
        }

        # Try running analysis function
        try:
            self.field = options['analysis_type'][0]
            self.analysis = analysisTypes.get(self.field)
        except TypeError:
            raise CommandError(
                'Analysis type does not exists. Select from %s' % functions.keys()
            )

        self.esFunction = None
        self.runAnalysis()
        self.stdout.write(self.style.SUCCESS('Complete'))


    def runAnalysis(self):

        samples = Sample.objects.all()
        numSamples = len(samples)

        self.stdout.write("Running %s analysis on %s samples. " % (self.field, numSamples))
        i = 0.0

        for sample in samples:

            # Get audio and run loudness analysis
            loader = self.analysis['loader'](filename=sample.path)
            audio = loader()
            value = self.analysis['function'](audio)

            # Get analysis object for this sample and save
            try:
                analysisObject = Analysis.objects.get(sample=sample)
            except Analysis.DoesNotExist:
                analysisObject = Analysis(sample=sample)

            setattr(analysisObject, self.field, value)
            analysisObject.save()

            i = i + 1
            self.stdout.write("\t\t%2.2f%% Complete" % (100.0*(i/float(numSamples))), ending='\r')
            self.stdout.flush()

        self.stdout.write("\r", ending='\r')
        self.stdout.flush()


    # Run Essentia Loudness
    def loudness(self, audio):

        if self.esFunction is None:
            self.esFunction = es.Loudness()

        return self.esFunction(audio)


    # Temporal Centroid
    def temporal_centroid(self, audio):

        envelope = es.Envelope()
        temporal = es.Centroid(range=(float(len(audio)-1)/44100))

        return temporal(envelope(audio))


    # Spectral Centroid
    def spectral_centroid(self, audio):

        if self.esFunction is None:
            self.esFunction = es.SpectralCentroidTime()

        return self.esFunction(audio)

    #RMS
    def rms(self, audio):

        if self.esFunction is None:
            self.esFunction = es.RMS()

        return 20*math.log10(self.esFunction(audio))


    def spectral_kurtosis(self, audio):

        spectralKurtosis = []
        mean = es.Mean()

        if self.esFunction is None:
            self.esFunction = [es.Windowing(type='hann'), es.Spectrum(), es.CentralMoments(), es.DistributionShape()]

        for frame in es.FrameGenerator(audio, frameSize=1024, hopSize=512, startFromZero=True):
            value = frame
            for function in self.esFunction:
                value = function(value)

            spectralKurtosis.append(value[2])

        return mean(spectralKurtosis)






