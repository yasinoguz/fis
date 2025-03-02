import cv2
import numpy as np
import matplotlib.pyplot as plt
import fis_no_kesim
import os




def segment_fis(path):
    img_bgr=fis_no_kesim.fis_donder(path)
  

    h,w=img_bgr.shape[:2]
    h,w=h*3, w*3
    plaka_bgr = cv2.resize(img_bgr, (w, h))
   # plt.figure();plt.imshow(plaka_bgr),plt.show()
   
    plaka_gray = cv2.cvtColor(plaka_bgr, cv2.COLOR_BGR2GRAY)
    #plt.figure(); plt.imshow(plaka_gray,cmap="gray");plt.title("gry");plt.show()

    plakatresh = cv2.adaptiveThreshold(plaka_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    plt.figure(); plt.imshow(plakatresh,cmap="gray");plt.title("threshold");plt.show()

    kernel = np.ones((3,2),np.uint8)
    th_img = cv2.erode(plakatresh,kernel,iterations=1)
    plt.figure(); plt.imshow(th_img,cmap="gray");plt.title("erode");plt.show()

    kernel2 = np.ones((7, 4), np.uint8)
# Tekrar dilate işlemi (isteğe bağlı)
    dilated = cv2.dilate(th_img, kernel2, iterations=1)
    plt.figure(); plt.imshow(dilated,cmap="gray");plt.title("dilate");plt.show()






    counter=0
    output_dir = "harfler3"
    if not os.path.exists(output_dir):
       os.makedirs(output_dir)

    char_list=[]
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    sorted_contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])

    for contour in sorted_contours:

        x, y, w, h = cv2.boundingRect(contour)
        
        if w<60 and w>5 and h>40:

            padding = 2
            x -= padding
            y -= padding
            w += 2*padding
            h += 2*padding
            kesim = plaka_bgr[y:y+h, x:x+w].copy()
            
          
            char_list.append(kesim)
            letter_filename = os.path.join(output_dir, f"letter_{counter}.png")
            cv2.imwrite(letter_filename, kesim)
            counter += 1
            

    plt.figure(); plt.imshow(plaka_bgr);plt.title("bgr");plt.show()

    return(char_list)


