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

class DateInput(forms.DateInput):
    input_type= 'date'
    format = '%d/%m/%Y'

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'sexe' : forms.TextInput(attrs={'class': 'form-control'}),
            'date_naissance': DateInput(attrs={'class': 'form-control'}),
            'Situation_Matrimoniale': forms.TextInput(attrs={'class': 'form-control'}),
            'addresse': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'medecin_traitant': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}),
        }


class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['examen', 'medecin_traitant', 'resultat']
    
    widgets = {
        'examen' : forms.TextInput(attrs={'class': 'form-control'}),
        'medecin_traitant': forms.TextInput(attrs={'class': 'form-control'}),
        'resultat': forms.TextInput(attrs={'class': 'required'})
    }
        
class AnalyseResultatForm(forms.ModelForm):
    class Meta:
        model = AnalysisResult
        fields = '__all__'
