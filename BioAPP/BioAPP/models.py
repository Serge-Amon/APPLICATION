# models.py

from django.db import models
###############################################################################################
####################### classe patient ################################
###############################################################################################
class Patient(models.Model):
    CHOIX_SEXE = (
        ('F','Feminin'),
        ('M','Masculin')
    )
    CHOIX_SITUATION = (
        ('C', 'Célibataire'),
        ('M', 'Marié(e)'),
        ('V', 'Veuf(ve)')
    )
    name = models.CharField(max_length = 255)
    prenom = models.CharField(max_length = 255)
    sexe = models.CharField(max_length = 1, choices = CHOIX_SEXE)
    Situation_Matrimoniale = models.CharField(max_length = 1, choices = CHOIX_SITUATION)
    phone = models.CharField(max_length = 255)
    addresse = models.CharField(max_length= 255)
    date_naissance = models.DateField()
    email = models.CharField(max_length = 255)

    def __str__(self):
        return self.name

###############################################################################################
####################### classe Gene ################################
###############################################################################################

class Gene(models.Model):
    name = models.CharField(max_length=255)
    sequence = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.name

###############################################################################################
####################### classe Examen ################################
###############################################################################################
class Exam(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    genes = models.ManyToManyField(Gene, related_name='exams')

    def __str__(self):
        return self.name

###############################################################################################
####################### classe Consultation ################################
###############################################################################################
class Consultation(models.Model):
    patient = models.ForeignKey(Patient, on_delete = models.CASCADE)
    examen = models.ForeignKey(Exam, on_delete = models.CASCADE)
    medecin_traitant = models.CharField(max_length = 255)
    date_consultation = models.DateField()

    def __str__(self):
        return f"Consultation for {self.patient} - {self.examen} - {self.date_consultation}"
###############################################################################################
####################### classe Experience ################################
###############################################################################################

class Experiment(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date_started = models.DateField()

    def __str__(self):
        return self.name
    

###############################################################################################
####################### classe Sample ################################
###############################################################################################

class Sample(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

###############################################################################################
####################### classe Resultat analyse ################################
###############################################################################################

class AnalysisResult(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    result_data = models.JSONField()

    def __str__(self):
        return f"Resultat pour {self.sample.name}"
