import cv2
import numpy as np
import matplotlib.pyplot as plt
import fis_segment
import os
import pickle


dosya = "rfc_model2.rfc"
rfc = pickle.load(open(dosya,"rb"))

sinifs = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10,
          'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18, 'J': 19, 'K': 20,
          'L': 21, 'M': 22, 'N': 23, 'O': 24, 'P': 25, 'Q': 26, 'R': 27, 'S': 28, 'T': 29, 'U': 30,
          'V': 31, 'W': 32, 'X': 33, 'Y': 34, 'Z': 35, 'arkaplan': 36}



index = list(sinifs.values())
siniflar = list(sinifs.keys())    




def modify_after_n(char_list):
    for i in range(len(char_list) - 1):  # Son elemandan sonra gelen olmadığı için -1
        if char_list[i] == 'N':  # Eğer eleman 'n' ise
            # Sonraki eleman bir harf mi?
                char_list[i + 1] = 'O'  # Sonraki harfi 'O' yap
    return char_list


def islem(img):
    yeni_boy = img.reshape((1600,5,5))
    orts = []
    for parca in yeni_boy:
        ort = np.mean(parca)
        orts.append(ort)
    orts = np.array(orts)
    
    orts = orts.reshape(1600,)
    return orts



def harf_tanima(path):
     fis_no=[]
     charlist=fis_segment.segment_fis(path)
     for chr in charlist:
        gray=cv2.cvtColor(chr, cv2.COLOR_BGR2GRAY)
    
        char = gray/255
        char = cv2.resize(char, (200, 200), interpolation=cv2.INTER_CUBIC)
        #plt.figure(); plt.imshow(char,cmap="gray");plt.title("200");plt.show()  
        oznitelikler=islem(char)
          
        karakter = rfc.predict([oznitelikler])[0]
       
        ind = index.index(karakter)
        sinif = siniflar[ind]
        fis_no.append(sinif)
     fis_no=modify_after_n(fis_no)
     return fis_no 
#harf_tanima("../fisler/fis.png")






