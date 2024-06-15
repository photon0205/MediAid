from django.db import models

class Symptom(models.Model):
    description = models.CharField(max_length=255)

class Diagnosis(models.Model):
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE)
    result = models.CharField(max_length=255)
