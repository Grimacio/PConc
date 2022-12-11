from threading import Thread
from PIL import Image
from tkinter import Tk
from tkinter.filedialog import askdirectory
import os

def resize(imagem, dimensoes):
    copy= Image.open(imagem)
    copy=copy.resize(dimensoes)
    return copy

def watermark(imagem):
    watermark= Image.open("watermark.png")
    imagem=Image.open(imagem)
    # image watermark
    position=(0,0) 
    crop_image = watermark.copy()
    
    # add watermark
    copied_image = imagem.copy()
    copied_image.paste(crop_image, position, crop_image)
    return copied_image

def thumbnail(ficheiro, tamanho):
    imagem=Image.open(ficheiro)
    imagem.thumbnail(tamanho)
    ##imagem.save(ficheiro.split(".")[0]+ ".thumbnail", "JPEG")
    return imagem

def threadFunc():
    return

