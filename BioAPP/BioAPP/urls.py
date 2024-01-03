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
from django.contrib import admin
from .views import GeneListView, ExamCreateView, ConsultationCreateView,PatientView

# urls.py
from django.urls import path
from .views import search_patient, export_results, home



urlpatterns = [
    path('admin/', admin.site.urls),
    path('genes/', GeneListView.as_view(), name='gene_list'),
    path('exams/create/', ExamCreateView.as_view(), name='exam_create'),
    path('consultation/create/', ConsultationCreateView.as_view(), name='consultation_create'),
    path('patient/', PatientView.as_view(), name='patient'),
    path('search/', search_patient, name='search_patient'),
    path('export-results/', export_results, name='export_results'),
    path('', home,  name="accueil")
    # Ajoutez d'autres URL au besoin
]
