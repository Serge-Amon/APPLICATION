

from django.contrib import admin
from .models import Gene, Experiment, Sample, AnalysisResult, Exam, Patient,Consultation

admin.site.register(Gene)
admin.site.register(Experiment)
admin.site.register(Sample)
admin.site.register(AnalysisResult)
admin.site.register(Exam)
admin.site.register(Patient)
admin.site.register(Consultation)
