from django.db import models

# Create your models here.
class RokAkademicki(models.Model):
    nazwa = models.CharField(max_length=9, unique=True)
    aktywny = models.BooleanField(default=True)

class Przedmiot(models.Model):
    rok = models.ForeignKey(RokAkademicki, on_delete=models.CASCADE)
    nazwa = models.CharField(max_length=100)

class Grupa(models.Model):
    rok = models.ForeignKey(RokAkademicki, on_delete=models.CASCADE)
    nazwa = models.CharField(max_length=100)

class Pracownik(models.Model):
    rok = models.ForeignKey(RokAkademicki, on_delete=models.CASCADE)
    imie_nazwisko = models.CharField(max_length=100)
