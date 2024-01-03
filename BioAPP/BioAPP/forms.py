# forms.py

from django import forms
from .models import Gene, Exam, Patient, Consultation, AnalysisResult

class GeneForm(forms.ModelForm):
    class Meta:
        model = Gene
        fields = ['name', 'sequence', 'description']

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['name', 'date', 'genes']

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'


class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = '__all__'

class AnalyseResultatForm(forms.ModelForm):
    class Meta:
        model = AnalysisResult
        fields = '__all__'
