"""
URL configuration for BioAPP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import GeneListView, ExamCreateView

# urls.py
from .views import (search_patient, export_results, home, 
                    create_patient_and_consultation, list_patients,
                    error, patient_detail)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('genes/', GeneListView.as_view(), name='gene_list'),
    path('exams/create/', ExamCreateView.as_view(), name='exam_create'),
    path('consultation/create/', create_patient_and_consultation, name='consultation_create'),
    path('search/', search_patient, name='search_patient'),
    path('export-results/', export_results, name='export_results'),
    path('patients/', list_patients, name='list_patients'),
    path('', home,  name='accueil'),
    path('patients/<int:id>/', patient_detail)
    
    # Ajoutez d'autres URL au besoin
]

handler404 = error