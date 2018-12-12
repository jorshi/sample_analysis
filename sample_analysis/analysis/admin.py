from django.contrib import admin
from .models import SamplePack, Kit, Sample, Tag, Manufacturer

admin.site.register(SamplePack)
admin.site.register(Kit)
admin.site.register(Sample)
admin.site.register(Tag)
admin.site.register(Manufacturer)

# Register your models here.
