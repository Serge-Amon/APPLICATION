
# views.py

from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.views import View
from .models import Gene, Exam,Consultation  # Assurez-vous que Gene et Exam sont correctement importés
from .forms import  ExamForm,ConsultationForm,PatientForm


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

class PatientView(View):
    def create_patient(request):
        if request.method == 'POST':
            form = PatientForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('liste_patients')  # Redirige vers la liste des patients
        else:
            form = PatientForm()
            return render(request, 'create_patient.html', {'form': form})


class ConsultationCreateView(CreateView):
    model = Consultation
    form_class = ConsultationForm
    template_name = 'consultation_create.html'  # Créez le template correspondant
    success_url = '/liste_consultations/'  # Redirige après la création


# views.py
from django.shortcuts import render
from .models import Patient
from django.db.models import Q

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
from django.http import HttpResponse
from django.template.loader import render_to_string

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
