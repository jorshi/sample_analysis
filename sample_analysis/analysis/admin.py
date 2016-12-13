from django.contrib import admin
from .models import SamplePack, Kit, Sample, Analysis

admin.site.register(SamplePack)
admin.site.register(Kit)
admin.site.register(Sample)
admin.site.register(Analysis)

# Register your models here.
