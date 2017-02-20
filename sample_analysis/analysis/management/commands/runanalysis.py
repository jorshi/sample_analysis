import sys
import essentia.standard as es
import numpy as np
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
            'spectral_centroid_1': {
                'function': self.spectral_centroid_1,
                'loader': self.loaders['eqloud'],
            },
            'spectral_centroid_2': {
                'function': self.spectral_centroid_2,
                'loader': self.loaders['eqloud'],
            },
            'temporal_centroid': {
                'function': self.temporal_centroid,
                'loader': self.loaders['eqloud'],
            },
            'rms': {
                'function': self.rms,
                'loader': self.loaders['eqloud'],
            },
            'spectral_kurtosis': {
                'function': self.spectral_kurtosis,
                'loader': self.loaders['eqloud'],
            },
            'pitch_salience': {
                'function': self.pitch_salience,
                'loader': self.loaders['eqloud'],
            },
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


    def getMeanTemporalCentroid(self):

        samples = Sample.objects.all()
        temporal = [sample.tamporal_centroid for sample in samples]



    def runAnalysis(self):

        samples = Sample.objects.all().filter(exclude=False)
        numSamples = len(samples)

        self.stdout.write("Running %s analysis on %s samples. " % (self.field, numSamples))
        i = 0.0

        for sample in samples:

            # Get audio and run loudness analysis
            try:
                loader = self.analysis['loader'](filename=sample.path)
                audio = loader()

                # Trim the audio clip
                trimmer = es.Trimmer(startTime=sample.start_time, endTime=sample.stop_time)
                audio = trimmer(audio)

            except RuntimeError:
                self.stderr.write("%s failed to load. Excluding sample from further analysis" % sample.path)
                sample.exclude = True
                sample.save()
                i = i + 1
                continue

            # Get analysis object for this sample and save
            try:
                analysisObject = Analysis.objects.get(sample=sample)
            except Analysis.DoesNotExist:
                analysisObject = Analysis(sample=sample)

            # Store temporal centroid
            if self.field in ['spectral_centroid_2']:
                self.temporalCentroid = analysisObject.temporal_centroid
                if self.temporalCentroid == None:
                    print "Run temporal centroid first"
                    sys.exit()

            value = self.analysis['function'](audio)
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


    def spectral_centroid_1(self, audio):

        # Zero pad
        if len(audio) < 1024:
            newAudio = np.zeros((1024,), audio.dtype)
            for i in range(len(audio)):
                newAudio[i] = audio[i]
            audio = newAudio

        return self.spectral_centroid(audio[0:1024])
    

    def spectral_centroid_2(self, audio):
        
        tSamples = int(self.temporalCentroid * 44100)
        frame = np.zeros((1024,), audio.dtype)
        length = (len(audio) - tSamples) if (len(audio) - tSamples) < 1024 else 1024

        for i in range(length):
            frame[i] = audio[i + tSamples]

        return self.spectral_centroid(frame)

    
    def onset(self, audio):
        
        startStop = es.StartStopSilence()
        startFrame = 0
        stopFrame = 0

        for frame in es.FrameGenerator(audio, 64, 32):
           startFrame, stopFrame = startStop(frame)

        startTime = float(startFrame * 32) / 44100.0
        stopTime = float(stopFrame * 32) / 44100.0

        return startTime

    def pitch_salience(self, audio):

        if self.esFunction is None:
            self.esFunction = es.PitchSalience(lowBoundary=20)

        return self.esFunction(audio)

