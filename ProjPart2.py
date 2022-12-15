import math 
from threading import Thread
from PIL import Image
from tkinter.filedialog import askdirectory
import os

path=""
dimensoes=0
tamanho=0
lista=[]
listacopy=[]
watermarkLOC="watermark.png"

def ap_paralelo_2():
    global path, lista
    initialize()
    lista=readtxt(path)
    createThreads()


def createThreads():
    global lista, listacopy
    listacopy=lista.copy()
    Processa_Watermark= Thread(target=tWatermark)
    Processa_Resize= Thread(target=tResize)
    Processa_Thumbnail= Thread(target=tThumbnail)

    Processa_Watermark.start()
    Processa_Watermark.join()

    Processa_Resize.start()
    Processa_Thumbnail.start()
    Processa_Resize.join()
    Processa_Thumbnail.join()

def initialize():
    print("Select Image Folder")
    global path, dimensoes, tamanho
    path = askdirectory(title='Select Folder')
    dimensoes=int(input("Resize to which size? (px):\n"))
    tamanho=int(input("Thumbnail to which size? (px):\n"))

    if not os.path.exists(path+"/Watermark-dir"):
        os.mkdir(path+"/Watermark-dir")
    if not os.path.exists(path+"/Resize-dir"):
        os.mkdir(path+"/Resize-dir")
    if not os.path.exists(path+"/Thumbnail-dir"):
        os.mkdir(path+"/Thumbnail-dir")


def readtxt(path):
    res=[]
    f= open(path+"/image-list.txt", "r")
    with f as texto:
        for line in texto:
            res+=[line.replace("\n", "")]
    return res


def resize(imagem, new_width):
    try:
        copy= Image.open(imagem)
        try:
            dimensoes = (new_width,math.ceil(new_width *1.0/copy.size[0] * copy.size[1]))
            copy=copy.resize(dimensoes)
            return copy
        except Exception as e:
            print(e)
            return None
    except Exception as e:
        print(e)
        return None

def watermark(imagem):
    global watermarkLOC
    try:
        imagem=Image.open(imagem)
        try:
            # image watermark
            position=(0,0) 
            crop_image = resize(watermarkLOC, math.ceil(imagem.size[0]/3))
            
            # add watermark
            copied_image = imagem.copy()
            copied_image.paste(crop_image, position, crop_image)
            return copied_image
        except Exception as e:
            print(e)
            return None
    except Exception as e:
        print(e)
        return None

def thumbnail(ficheiro, tamanho):
    tamanho = math.ceil(tamanho)
    if tamanho < 1:
        print("dimensao thumbnail invalida")
        return None
    try:
        imagem=Image.open(ficheiro)
        try:
            width, height = imagem.size
            if(width > height):
                new_height = tamanho
                new_width = math.ceil(new_height *1.0/height * width)
            else:
                new_width = tamanho
                new_height = math.ceil(new_width *1.0/width * height)
            imagem.thumbnail((new_width,new_height))
            corte = (math.ceil(new_width/2-tamanho/2),math.ceil(new_height/2-tamanho/2),math.ceil(new_width/2+tamanho/2),math.ceil(new_height/2+tamanho/2))
            imagem = imagem.crop(corte)
            return imagem
        except Exception as e:
            print(e)
            return None
    except Exception as e:
        print(e)
        return None

def tWatermark():
    global listacopy
    global path
    while len(listacopy)>0:
        imagem= listacopy.pop()

        if not os.path.exists(path+"/Watermark-dir/"+imagem):
            print("watermark de "+imagem.split(".")[0]+": nao encontrado")
            watermark(path+"/"+imagem).save(path+ "/Watermark-dir/"+imagem, "PNG")
        else:
            print("watermark de "+imagem.split(".")[0]+": encontrado")
    return

def tResize():
    
    global lista
    global path
    global dimensoes
    for imagem in lista:
        if not os.path.exists(path+"/Resize-dir/"+imagem):
            print("resize de "+imagem.split(".")[0]+": nao encontrado")
            resize(path+ "/Watermark-dir/" +imagem, dimensoes).save(path +"/Resize-dir/"+ imagem, "PNG")
        else:
            print("resize de "+imagem.split(".")[0]+": encontrado")
    return
        

def tThumbnail():
    
    global tamanho

    global lista
    global path
    for imagem in lista:
        if not os.path.exists(path+"/Thumbnail-dir/"+imagem):
            print("resize de "+imagem.split(".")[0]+": nao encontrado")
            thumbnail(path+"/Resize-dir/" + imagem, tamanho).save(path + "/Thumbnail-dir/" +imagem, "PNG")
        else:
            print("resize de "+imagem.split(".")[0]+": encontrado")
    return



ap_paralelo_2()