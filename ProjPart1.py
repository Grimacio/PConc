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
    global listacopy
    global path
    while len(listacopy)>0:
        imagem= listacopy.pop()
        dimensoes=(250,250)
        tamanho=(50,50)

        watermark(path+"/"+imagem).save(path+ "/watermark/"+imagem, "PNG")

        resize(path+ "/watermark/" +imagem, dimensoes).save(path +"/resized/"+ imagem, "PNG")

        thumbnail(path+"/resized/" + imagem, tamanho).save(path + "/thumbnail/" +imagem, "PNG")

    return


print("Select Image Folder")
path = askdirectory(title='Select Folder')
print(path)
os.mkdir(path+"/watermark")
os.mkdir(path+"/resized")
os.mkdir(path+"/thumbnail")
numeroThreads=int(input("Number of Threads?:\n"))
lista=[]
new=[]

f= open("nomes.txt", "r")

with f as texto:
    for line in texto:
        lista+=[line.replace("\n", "")]



listacopy=lista
listaThreads=[]
for i in range( numeroThreads):
    newThread = Thread(target=threadFunc)
    newThread.start()
    listaThreads+=[newThread]
for item in listaThreads:
    item.join()
    print("done")



