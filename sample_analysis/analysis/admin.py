from django.contrib import admin
from .models import SamplePack, Kit, Sample, Analysis, Tag

admin.site.register(SamplePack)
admin.site.register(Kit)
admin.site.register(Sample)
admin.site.register(Analysis)
admin.site.register(Tag)

# Register your models here.
