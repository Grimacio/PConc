import math 
from threading import Thread
from PIL import Image
from tkinter.filedialog import askdirectory
import os
from time import time

path=""
dimensoes=0
tamanho=0
lista=[]
listacopy=[]
watermarkLOC="../watermark.png"
start=0
end=0



# Inicializa o programa recolhendo inputs pelo terminal, 
# recolhe os endereços das imagens e cria as threads de acordo

def ap_paralelo_2():
    
    global path, lista
    
    initialize()
    lista=readtxt(path)
    createThreads()




# Sao criadas 3 Threads, cada uma executa uma das 3 funcoes
# (tWatermark, tResize e tThumbnail)

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




# Define os valores a utilizar no programa, bem como
# a diretoria das imagens requeridas

def initialize():
    print("Select Image Folder")
    global path, dimensoes, tamanho, start
    

    # Abre uma janela em que se navega até à diretoria em
    # que se econtram as imagens e o ficheiro .txt, 
    # guardando-se o path    
    
    path = askdirectory(title='Select Folder')
    
    # A dimensao referente a imagem redimensionada
    
    dimensoes=int(input("Resize to which size? (px):\n"))
    
    # A dimensao da thumbnail
    
    tamanho=int(input("Thumbnail to which size? (px):\n"))

    # Apenas criamos as novas pastas se estas nao existirem
    start= time()
    if not os.path.exists(path+"/Watermark-dir"):
        os.mkdir(path+"/Watermark-dir")
    if not os.path.exists(path+"/Resize-dir"):
        os.mkdir(path+"/Resize-dir")
    if not os.path.exists(path+"/Thumbnail-dir"):
        os.mkdir(path+"/Thumbnail-dir")




# Com base no ficheiro "image-list.txt" presente na diretoria em que
# as imagens se encontram, é retornada uma lista com os nomes das imagens

def readtxt(path):
    res=[]
    f= open(path+"/image-list.txt", "r")
    with f as texto:
        for line in texto:
            res+=[line.replace("\n", "")]
    return res




# Com base no metodo "resize" as imagens alteram a sua largura 
# para a dimensão indicada, mantendo a relação largura-altura 
# da imagem original

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




# Com base no método "paste" a watermark e colocada no canto superior
# esquerdo da imagem original, sendo a sua largura ajustada para
# corresponder a 1/3 da largura da imagem a que se pretende aplicar

def watermark(imagem):

    global watermarkLOC

    try:
        imagem=Image.open(imagem)

        try:

            # Ajustamento da largura da watermark

            position=(0,0) 
            crop_image = resize(watermarkLOC, math.ceil(imagem.size[0]/3))

            # Colocaçao da watermark

            copied_image = imagem.copy()
            copied_image.paste(crop_image, position, crop_image)
            return copied_image
        except Exception as e:
            print(e)
            return None

    except Exception as e:
        print(e)
        return None




# Com base no método "thumbnail" a imagem e redimensionada para o
# tamanho indicado (convertendo para este tamanho a dimensao de maior 
# grau). De seguida a imagem é cortada centralmente, de modo a que
# se torne um quadrado com dimensoes iguais ao tamanho indicado

def thumbnail(ficheiro, tamanho):

    tamanho = math.ceil(tamanho)
    if tamanho < 1:
        print("dimensao thumbnail invalida")
        return None

    try:
        imagem=Image.open(ficheiro)

        try:

            width, height = imagem.size

            # Escolha da maior dimensao e conversão para a dimensão contrária

            if(width > height):
                new_height = tamanho
                new_width = math.ceil(new_height *1.0/height * width)
            else:
                new_width = tamanho
                new_height = math.ceil(new_width *1.0/width * height)

            # Redimensionamento da imagem

            imagem.thumbnail((new_width,new_height))

            # Corte central quadrado

            corte = (math.ceil(new_width/2-tamanho/2),math.ceil(new_height/2-tamanho/2),math.ceil(new_width/2+tamanho/2),math.ceil(new_height/2+tamanho/2))
            imagem = imagem.crop(corte)
            return imagem
        except Exception as e:
            print(e)
            return None

    except Exception as e:
        print(e)
        return None




# Enquanto a listacopy contiver enderecos de imagens para processar,
# o último dos seus elementos e usado para criar uma cópia da imagem
# com watermark

def tWatermark():
    
    global listacopy
    global path
    
    # Enquanto a listacopy contiver enderecos de imagens para processar,
    # a Thread continua ativa
    
    while len(listacopy)>0:
        
        # O último dos seus elementos é usado 
        
        imagem= listacopy.pop()

        if not os.path.exists(path+"/Watermark-dir/"+imagem):
            print("watermark de "+imagem.split(".")[0]+": nao encontrado")
            watermark(path+"/"+imagem).save(path+ "/Watermark-dir/"+imagem, "PNG")
        else:
            print("watermark de "+imagem.split(".")[0]+": encontrado")
    return




# Para cada imagem criada com watermark é criada uma cópia com diferente 
# tamanho

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



        
# Para cada imagem criada com watermark e criada uma copia para originar 
# uma thumbnail

def tThumbnail():
    
    global tamanho
    global lista
    global path
    
    for imagem in lista:
        if not os.path.exists(path+"/Thumbnail-dir/"+imagem):
            print("thumbnail de "+imagem.split(".")[0]+": nao encontrado")
            thumbnail(path+ "/Watermark-dir/" + imagem, tamanho).save(path + "/Thumbnail-dir/" +imagem, "PNG")
        else:
            print("thumbnail de "+imagem.split(".")[0]+": encontrado")
    return



ap_paralelo_2()
end= time()
print(end-start)