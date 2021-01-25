from django.db import models
from django.conf import settings
from django.contrib import admin
import django.db.models.deletion



class AnimalModel(models.Model):
    idA = models.CharField(primary_key=True, max_length=254)
    idAnimal = models.CharField(max_length=254)
    imagenAnimal = models.ImageField(upload_to = "AnimalImagenes/")
    nombreAnimal = models.CharField(max_length=254)
    nombreTecnico = models.CharField(max_length=100, default=None)
    idCategoria = models.CharField(max_length=100, default=None)
    categoria = models.CharField(max_length=100, default=None)

    def __str__(self):
        return str(self.idA)


class AnimalEntry(models.Model):
    idAnimal = models.CharField(max_length=254)
    imagenAnimal = models.ImageField(upload_to = "ImagenesPrueba/")
    predictLabel = models.CharField(max_length=254)

    def __str__(self):
        return str(self.idAnimal)

admin.site.register(AnimalModel)
admin.site.register(AnimalEntry)