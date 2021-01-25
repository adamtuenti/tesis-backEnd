# -*- coding: cp1252 -*-
from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import AnimalModel, AnimalEntry
from .serializers import analizarImagenSerializer
from django.http import HttpResponse
from rest_framework.response import Response
import base64
from django.core.files.base import ContentFile
import matplotlib
import numpy as np
import keras
from PIL import Image
import os
import cv2
import random as rn


class Animal(APIView):
    #cargando los 4 modelos entrenados
    modelo = keras.models.load_model('./modelo/my_model.h5')
    modelo_3clases = keras.models.load_model('./modelo/3_clases.h5')
    modelo_aereo = keras.models.load_model('./modelo/red_aereo.h5')
    modelo_marino = keras.models.load_model('./modelo/red_marina.h5')
    modelo_terrestre = keras.models.load_model('./modelo/red_terrestre.h5')


    modelos_detallados = [modelo_aereo,modelo_marino,modelo_terrestre]  #el orden esta definido de acuerdo a las clases del modelo_3clases
    
    def post(self, request, *args, **kwargs):
        
        serializer_class = analizarImagenSerializer

        base = request.data.get('imagenAnimal')
        #se transforma el codigo en base64 obtenida del cliente
        base = "data:image/jpg;base64," + base
        format, imgstr = base.split(';base64,') 
        ext = format.split('/')[-1] 
        #se transforma en una imagen
        data = ContentFile(base64.b64decode(imgstr), name='image_temporal.' + ext) # You can save this as file instance.
        file_name = "'myphoto." + ext
        IMG_SIZE = 224

        
        idAleatorio = rn.randint(1,15000)
        #se crea un nuevo elemento en el modelo animal entry con un id aleatorio
        solicitud = AnimalEntry.objects.create(idAnimal=idAleatorio, imagenAnimal=data, predictLabel='')
        imagen1 = AnimalEntry.objects.filter(idAnimal=idAleatorio)
        
        #se obtiene la url de la imagen subida
        url = imagen1[0].imagenAnimal.url
        url = '.'+str(url)
        if(url!=''):
 
            img_array = cv2.imread(url,cv2.IMREAD_COLOR)
            new_array = cv2.resize(img_array,(IMG_SIZE,IMG_SIZE))
            img = new_array.reshape(-1,IMG_SIZE,IMG_SIZE, 3)

            prediction_3_clases = self.modelo_3clases.predict(img)
            
            ind_clase = prediction_3_clases.argmax(axis=1)[0]
            
            #Se utiliza el modelo especifico de acuerdo a ind_clase
            prediction = self.modelos_detallados[ind_clase].predict(img)

            indicesOrdenados = prediction.argsort(axis=1)[0][-3:][::-1]
            prediction = prediction[0]
            

            ind_max1 = indicesOrdenados[0]
            ind_max2 = indicesOrdenados[1]
            ind_max3 = indicesOrdenados[2]

            num_max1 = prediction[ind_max1] * 100
            num_max2 = prediction[ind_max2] * 100
            num_max3 = prediction[ind_max3] * 100

            solicitud.predictLabel = ind_max1
            solicitud.save()


            #se filtra los tres indices en el modelo animal model con respecto al indice de la subcategoria del animal encontrado y al indice de la clase
            datos1 = AnimalModel.objects.filter(idAnimal=ind_max1,idCategoria=ind_clase)
            datos2 = AnimalModel.objects.filter(idAnimal=ind_max2,idCategoria=ind_clase)
            datos3 = AnimalModel.objects.filter(idAnimal=ind_max3,idCategoria=ind_clase)


            opc1 = {'nombreAnimal':datos1[0].nombreAnimal,'nombreTecnico':datos1[0].nombreTecnico,'accuracy':num_max1,'imagenAnimal':datos1[0].imagenAnimal.url}
            opc2 = {'nombreAnimal':datos2[0].nombreAnimal,'nombreTecnico':datos2[0].nombreTecnico,'accuracy':num_max2,'imagenAnimal':datos2[0].imagenAnimal.url}
            opc3 = {'nombreAnimal':datos3[0].nombreAnimal,'nombreTecnico':datos3[0].nombreTecnico,'accuracy':num_max3,'imagenAnimal':datos3[0].imagenAnimal.url}
            #se retorna una lista con los 3 diccionarios de las 3 especies relacionadas a la imagen analizada
            listaOpciones = [opc1,opc2,opc3]
            return Response(data=listaOpciones)

    


            
