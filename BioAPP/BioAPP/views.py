
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from django.views import View
from .models import Gene, Patient, Consultation  # Assurez-vous que Gene et Exam sont correctement importés
from .forms import  ExamForm,ConsultationForm,PatientForm
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template import loader
from django.db.models import Q


class GeneListView(View):
    template_name = '/templates/gene_list.html'

    def get(self, request):
        genes = Gene.objects.all()
        return render(request, self.template_name, {'genes': genes})

class ExamCreateView(View):
    template_name = '/templates/exam_create.html'

    def get(self, request):
        form = ExamForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save()
            return redirect('gene_list')  # Redirige vers la liste des gènes ou toute autre vue que vous avez

        return render(request, self.template_name, {'form': form})

def create_patient_and_consultation(request):
    endpoint = 'patients'
    template_name = "consultation_create.html"
    if request.method == 'POST':
        patient_form = PatientForm(request.POST)
        consultation_form = ConsultationForm(request.POST)
        if patient_form.is_valid() and consultation_form.is_valid():
            patient= patient_form.save()
            consultation = consultation_form.save(commit=False)
            consultation.patient = patient
            consultation.save()
            return redirect(f'{endpoint}')
    else:
        patient_form = PatientForm()
        consultation_form = ConsultationForm()
    
    return render(request, f'{template_name}', {'patient_form': patient_form, 'consultation_form': consultation_form})
# views.py

def search_patient(request):
    query = request.GET.get('q')

    if query:
        results = Patient.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
    else:
        results = Patient.objects.all()

    return render(request, 'search_patient.html', {'results': results, 'query': query})


# views.py


def export_results(request):
    query = request.GET.get('q')
    results = Patient.objects.filter(
        Q(first_name__icontains=query) | Q(last_name__icontains=query)
    )

    # Générer le contenu du fichier CSV (ou tout autre format d'export que vous souhaitez)
    csv_content = render_to_string('export_results.csv', {'results': results})

    # Créer la réponse HTTP avec le contenu du fichier CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="export_results.csv"'
    response.write(csv_content)

    return response


def home(request):
    home_page = '/templates/base.html'
    return render(request, 'base.html')


def list_patients(request):
    template_name ='liste_patients.html'
    patients = Patient.objects.all()
    return render(request,f'listings/{template_name}', {'patients':patients})


def get_patient_by_id(patient_id):
    return get_object_or_404(Patient, id=patient_id)

def patient_detail(request, id):
    patient = get_patient_by_id(id)
    return render(request, 'listings/detail_record.html', {'patient': patient})

def get_latest_patient():
    latest_patient = Patient.objects.order_by('-id').first()
    return latest_patient


def get_latest_consultation():
    latest_consultation = Consultation.objects.order_by('-id').first
    return latest_consultation
    


def error(request, exception):
    template_name = 'error404'
    try:
        loader.get_template(f'{template_name}.html')
    except :
        return render(request, f'{template_name}.html', {}, status=404)
    
    
def diagnostic_create(request):
    latest_consultation = Consultation.objects.order_by('-id').first
    if request.method == 'POST':
        # Logique de sauvegarde de la consultation
        pass  # À remplacer par la logique de sauvegarde de la consultation
    else:
        initial_data = {
            'inputNom': latest_consultation.nom,
            'inputPrenom': latest_consultation.prenom,
            'inputBod': latest_consultation.date_de_naissance,
            'inputSexe': latest_consultation.sexe,
            'matrimoniale': latest_consultation.situation_matrimoniale,
            'inputAdress': latest_consultation.adresse,
            'inputMed': latest_consultation.medecin_traitant,
            'inputEmail': latest_consultation.email,
            'inputExam': '',  # Ajoutez le champ d'examen demandé ici si nécessaire
        }
        form = ConsultationForm(initial=initial_data)
