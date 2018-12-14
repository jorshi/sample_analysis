
from django.core.management.base import BaseCommand, CommandError
import matplotlib.pyplot as plt
from numpy.random import rand
from analysis.models import Sample, AnalysisPCA, AnalysisFull, PCAStat

class Command(BaseCommand):

    # Override of the add_argument method
    def add_arguments(self, parser):

        # Required argument for the type of analysis to run
        parser.add_argument('sample_type', nargs=1, type=str)
        parser.add_argument('window_length', nargs=1, type=int)
        parser.add_argument('window_start', nargs=1, type=int)

    # Executes on command runtime
    def handle(self, *args, **options):
        
        choices = [x[0] for x in Sample.SAMPLE_TYPE_CHOICES]
        if options['sample_type'][0] not in choices:
            print "Sample type must by one of %s" % choices
            sys.exit(1)

        # Get all the analysis objects for a particular sample type
        sampleObjects = AnalysisPCA.objects.filter(
            window_length=options['window_length'][0],
            sample__sample_type=options['sample_type'][0],
            window_start=options['window_start'][0],
        )

        # Plot the samples 
        fig, ax = plt.subplots()

        for item in sampleObjects:
            x, y = item.dim_1, item.dim_2
            ax.scatter(x, y)

        ax.grid(True)

        plt.show()


