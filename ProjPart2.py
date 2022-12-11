from threading import Thread
from threading import Condition
from PIL import Image
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
    return imagem

def tWatermark(self):
    global listacopy
    global path
    global watermarkReady
    while len(listacopy)>0:
        self.acquire()
        imagem= listacopy.pop()

        watermark(path+"/"+imagem).save(path+ "/watermark/"+imagem, "PNG")
        print("acabei 1")
        watermarkReady+=[path+"/watermark/"+imagem]
        self.notify_all()
        self.release()
    return

def tResize(self):
    
    global dimensoes
    i=0
    while watermarkThread.is_alive() or len(watermarkReady)>i:
        self.acquire()
        if len(watermarkReady)<=i:
            self.wait()
            print("acordei")
        else:
            target=watermarkReady[i]
            print("encontrei1")
            resize(target, dimensoes).save(path +"/resized/"+ target.split("/")[-1], "PNG")
            i+=1
        self.release()
    return

def tThumbnail(self):
    
    global tamanho
    j=0
    while watermarkThread.is_alive() or len(watermarkReady)>j:
        self.acquire()  
        if len(watermarkReady)<=j:
            self.wait()
            print("acordei")
        else:
            target=watermarkReady[j]
            print("encontrei2")
            thumbnail(target, tamanho).save(path +"/thumbnail/"+ target.split("/")[-1], "PNG")
            j+=1
        self.release()
    
    return
        

dimensoes= (500,500)
tamanho = (50,50)
watermarkReady=[]
print("Select Image Folder")
path = askdirectory(title='Select Folder')
print(path)
os.mkdir(path+"/watermark")
os.mkdir(path+"/resized")
os.mkdir(path+"/thumbnail")

lista=[]

f= open("nomes.txt", "r")

with f as texto:
    for line in texto:
        lista+=[line.replace("\n", "")]

listacopy=lista.copy()


condition = Condition()

watermarkThread= Thread(target=tWatermark, args=(condition,))
resizeThread= Thread(target=tResize, args=(condition,))
thumbnailThread= Thread(target=tThumbnail, args=(condition,))

watermarkThread.start()
resizeThread.start()
thumbnailThread.start()

watermarkThread.join()
resizeThread.join()
thumbnailThread.join()

print("done")