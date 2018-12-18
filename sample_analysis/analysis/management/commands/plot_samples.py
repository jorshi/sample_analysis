
from django.core.management.base import BaseCommand, CommandError
import matplotlib.pyplot as plt
from numpy.random import rand
from analysis.models import Sample, SamplePack, AnalysisPCA, AnalysisFull, PCAStat, Manifold

DrumMachines = {
 'ki': [155,100,75,92,132,144],
 'sn':  [155,100,35,92,132,48,144,197],
}

Colours = [
 '#26294a',
 '#017351',
 '#03c383',
 '#fbbf45',
 '#ef6a32',
 '#ed0345',
 '#a12a5e',
 '#710162',
]

class Command(BaseCommand):

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

        # Get all the embedded samples for a particular sample type & reduction method type in a sample pack
        if options['sample_type'][0] == 'ki':
            if options['reduction_method'][0] != 'pca':
                samples = Manifold.objects.filter(
                    method=options['reduction_method'][0],
                    window_length=options['window_length'][0],
                    window_start=options['window_start'][0],
                    sample__sample_type='ki',
                    sample__kit__sample_pack__in=DrumMachines['ki'],
                )
            else:
                samples = AnalysisPCA.objects.filter(
                    window_length=options['window_length'][0],
                    window_start=options['window_start'][0],
                    sample__sample_type='ki',
                    sample__kit__sample_pack__in=DrumMachines['ki'],
                )

        elif options['sample_type'][0] == 'sn':
            if options['reduction_method'][0] != 'pca':
                samples = Manifold.objects.filter(
                    method=options['reduction_method'][0],
                    window_length=options['window_length'][0],
                    window_start=options['window_start'][0],
                    sample__sample_type='sn',
                    sample__kit__sample_pack__in=DrumMachines['sn'],
                )
            else:
                samples = AnalysisPCA.objects.filter(
                    window_length=options['window_length'][0],
                    window_start=options['window_start'][0],
                    sample__sample_type='sn',
                    sample__kit__sample_pack__in=DrumMachines['sn'],
                )
        else:
            self.stderr.write("Sample type must be 'ki' or 'sn'")
            exit()

        # Get names of Drum Machines for plotting
        machines = SamplePack.objects.filter(id__in=DrumMachines[options['sample_type'][0]])

        # Plot the samples 
        fig, ax = plt.subplots()
        
        i = 0
        for machine in DrumMachines[options['sample_type'][0]]:
            
            pack = machines.filter(id=machine)
            
            x = [j.dim_1 for j in samples.filter(sample__kit__sample_pack=machine)]
            y = [j.dim_2 for j in samples.filter(sample__kit__sample_pack=machine)]

            ax.scatter(x, y, c=Colours[i], label=pack[0].name, s=30, alpha=0.75)
            i = i + 1

        ax.grid(True)
        ax.legend()
        
        fig.suptitle('%s %s' % (options['reduction_method'][0], options['sample_type'][0]), fontsize=16)

        plt.show()


