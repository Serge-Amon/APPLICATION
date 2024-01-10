
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from django.views import View
from .models import Gene, Patient, Consultation  # Assurez-vous que Gene et Exam sont correctement importés
from .forms import  ExamForm,ConsultationForm,PatientForm
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.template import loader
from django.db.models import Q
import csv
from django.http import HttpResponse

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
    template_name= 'consultation_create.html'
    if request.method == 'POST':      
        patient_form = PatientForm(request.POST)
        
        consultation_form = ConsultationForm(request.POST)
        #print('Response de la requete patient :' ,patient_form.is_valid())
        
        # if patient_form.is_valid():
        #     print(consultation_form)
            
            # nom = patient_form.cleaned_data.get('nom')
            # prenom = patient_form.cleaned_data.get('prenom')
            # email = patient_form.cleaned_data.get('email')
            
            # donnees_formulaires = {
            #     'nom': nom,
            #     'prenom': prenom,
            #     'email': email,
            # }
            # print(donnees_formulaires)
        
        print('Response de la requete patient :' ,patient_form.is_valid())
        print('Response de la requete patient :' ,consultation_form.is_valid())
        
        if patient_form.is_valid() and consultation_form.is_valid():
            patient = patient_form.save()
            consultation_instance = consultation_form.save(commit=False)
            consultation_instance.patient = patient
            print('Consultation a ete enregistree : ', consultation_instance)
            
            consultation_instance.save()

            return redirect('consultations')
    else:
        patient_form = PatientForm()
        consultation_form = ConsultationForm()
    context = {'patient_form': patient_form, 'consultation_form': consultation_form}
    return render(request, f'{template_name}', context)
# views.py

# def search_patient(request):
#     query = request.GET.get('q')

#     if query:
#         results = Patient.objects.filter(
#             Q(first_name__icontains=query) | Q(last_name__icontains=query)
#         )
#     else:
#         results = Patient.objects.all()

#     return render(request, 'search_patient.html', {'results': results, 'query': query})


# views.py
def success_patient(request):
    template_name = 'success_patients.html'
    return render(request, f'{template_name}', {'patient_id': request.POST})

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


def list_consultations(request):
    template_name = 'list_consultations.html'
    consultations = Consultation.objects.all()
    consultation_s = []

    nom = request.GET.get('nom', '')
    examen = request.GET.get('examen', '')

    if nom:
        consultations_nom = consultations.filter(patient__name__icontains=nom)
        print("Consultations filtrées par nom :", consultations_nom)  # Ajout de cette ligne pour le débogage
        consultations = consultations_nom

    if examen:
        consultations_exam = consultations.filter(examen__icontains=examen)
        print("Consultations filtrées par examen :", consultations_exam)  # Ajout de cette ligne pour le débogage
        consultations = consultations_exam

    for consultation in consultations:
        patient_info = str(consultation.patient).split('|')
        formatted_date = consultation.date_consultation.strftime("%Y-%m-%d %H:%M:%S")
        consultation_s.append({
            'id': consultation.id,
            'date': formatted_date,
            'patient_name': patient_info[0],
            'patient_surname': patient_info[1],
            'patient_email': patient_info[2],
            'examen': consultation.examen,
            'medecin_traitant': consultation.medecin_traitant
        })

    context = {
        'consultations': consultation_s,
        'nom_recherche': nom,
        'examen_recherche': examen
    }

    return render(request, f'listings/{template_name}', context)



def get_patient_by_id(patient_id):
    return get_object_or_404(Patient, id=patient_id)

def patient_detail(request, id):
    patient = get_patient_by_id(id)
    return render(request, 'listings/detail_record.html', {'patient': patient})

# def get_latest_patient():
#     latest_patient = Patient.objects.order_by('-id').first()
#     return latest_patient


# def get_latest_consultation():
#     latest_consultation = Consultation.objects.order_by('-id').first
#     return latest_consultation
    


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


def export_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Date', 'Nom', 'Prenom', 'Email', 'Examen', 'Medecin Traitant'])

    consultations = Consultation.objects.all()
    nom = request.GET.get('nom', '')
    examen = request.GET.get('examen', '')

    if nom:
        consultations = consultations.filter(patient__name__icontains=nom)
    if examen:
        consultations = consultations.filter(examen__icontains=examen)

    for consultation in consultations:
        patient_info = str(consultation.patient).split('|')
        formatted_date = consultation.date_consultation.strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([
            consultation.id,
            formatted_date,
            patient_info[0],
            patient_info[1],
            patient_info[2],
            consultation.examen,
            consultation.medecin_traitant
        ])

    return response



def search_patient(request):
    query = request.GET.get('nom')  # Récupérer le paramètre 'nom' de l'URL
    template_name = 'list_patients.html'
    if query:
        patients = Patient.objects.filter(nom__icontains=query)  # Recherche insensible à la casse
        return render(request, f'{template_name}', {'patients': patients, 'query': query})
    else:
        patients = Patient.objects.all()
        return render(request, f'{template_name}', {'patients': patients})
    
    
def export_consultations(request):
    template_name = 'export_consultations.html'
    return render(request, f'{template_name}')


def filter_consultations(request):
    consultations = Consultation.objects.all()
    print("Liste des consultations :", consultations)
    template_name = 'list_consultations.html'
    nom = request.GET.get('nom')
    examen = request.GET.get('examen')
    print('Requete effectuee sur le nom :', nom)
    print("Requete effectue sur l'examen :", examen)
    
    
    if nom:
        consultations = consultations.filter(patient__icontains=f'{nom}')
    if examen:
        consultations = consultations.filter(examen__icontains=examen)
    
    return render(request, f'listings/{template_name}', {'consultations': consultations})

# def list_consultations(request):
#     template_name = 'list_consultations.html'
#     consultations = Consultation.objects.all()

#     nom = request.GET.get('nom')
#     examen = request.GET.get('examen')

#     if nom:
#         consultations = consultations.filter(patient_name__icontains=nom)

#     if examen:
#         consultations = consultations.filter(examen__icontains=examen)

#     return render(request, f'listings/{template_name}', {'consultation_s': consultations})
