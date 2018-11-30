"""
Script for loading samples contained in a folder
structure SamplePack/kit_xx/kick/sample.wav
into the database model
"""
import sys, os
from django.utils.encoding import smart_text
from django.core.management.base import BaseCommand, CommandError
from analysis.models import SamplePack, Kit, Sample, Tag
import essentia.standard as es


class Command(BaseCommand):
    help = 'Load drum samples into database'
    sampleTypes = {
        'kick': Sample.KICK,
        'snare': Sample.SNARE,
    }

    def add_arguments(self, parser):
        parser.add_argument('directory', nargs='+', type=str)

        parser.add_argument(
            '--tags',
            type=str,
            dest='tags',
            default=None,
            help='Tags to add to sample packs'
        )


    def handle(self, *args, **options):

        self.tags = []
        if options['tags'] is not None:
            for tag in options['tags'].split(','):
                try:
                    tagObject = Tag.objects.get(word=tag)
                except Tag.DoesNotExist:
                    tagObject = Tag(word=tag)
                    tagObject.save()

                self.tags.append(tagObject)

        for directory in options['directory']:
            self.exploreSamplePack(directory, os.path.abspath(directory))

    
    def exploreSamplePack(self, name, root, prev=None):

        # Check out all directory items
        for item in os.listdir(root):
            fullPath = os.path.abspath(os.path.join(root,item))

            # If this item is a diectory, it's either a sample pack, kit, kick or snare
            if os.path.isdir(fullPath):
                if item.lower() in self.sampleTypes.keys():
                    if isinstance(prev, SamplePack):
                        try:
                            kit = Kit.objects.get(sample_pack=prev, id_number=1)
                            prev = kit
                        except Kit.DoesNotExist:
                            kit = Kit(sample_pack=prev, id_number=1)
                            kit.save()
                            prev = kit

                    # Load samples for kick or snare
                    sampleType = self.sampleTypes[item] 
                    for fileItem in os.listdir(fullPath):
                        if fileItem[0] == '.':
                            continue
                        samplePath = smart_text(os.path.abspath(os.path.join(fullPath,fileItem)))

                        # Try to extract start and stop time of the sample in question
                        # if it fails then remove it from further testing
                        try:
                            startTime, stopTime = self.onsetDetection(samplePath)
                        except RuntimeError:
                            continue

                        try:
                            sample = Sample.objects.get(kit=prev, path=samplePath)
                            sample.start_time = startTime
                            sample.stop_time = stopTime
                        except Sample.DoesNotExist:
                            sample = Sample(kit=prev, path=samplePath, sample_type=sampleType,
                                            start_time=startTime, stop_time=stopTime)
                        
                        sample.save()

                # Assuming that no sample packs start with kit (:/)
                elif item.lower().startswith('kit_'):
                    # Create a kit attached to this
                    kitNo = int(item.split('_')[1])

                    try:
                        kit = Kit.objects.get(sample_pack=prev, id_number=kitNo)
                    except Kit.DoesNotExist:
                        kit = Kit(sample_pack=prev, id_number=kitNo)
                        kit.save()

                    self.exploreSamplePack(item, fullPath, kit)

                else:
                    # Create a new sample pack
                    id = item.replace(" ", "_").lower()

                    try:
                        samplePack = SamplePack.objects.get(id_name=id)
                    except SamplePack.DoesNotExist:
                        samplePack = SamplePack(id_name=id, name=item)
                        samplePack.save()

                    [samplePack.tags.add(tag) for tag in self.tags]
                    samplePack.save()

                    self.exploreSamplePack(item, fullPath, samplePack)


    def onsetDetection(self, samplePath):

        # Get audio from file
        loader = es.MonoLoader(filename=samplePath.encode('utf-8'))
        audio = loader()

        startStop = es.StartStopSilence()
        startFrame = 0
        stopFrame = 0

        for frame in es.FrameGenerator(audio, 64, 32):
           startFrame, stopFrame = startStop(frame)

        startTime = float(startFrame * 32) / 44100.0
        stopTime = float((stopFrame * 32) + 64) / 44100.0

        return startTime, stopTime
