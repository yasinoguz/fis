import cv2
import numpy as np
import matplotlib.pyplot as plt



def fis_donder(path):
    img = cv2.imread(path)
 
    image=cv2.resize(img,(500,500))
    img_bgr = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    plt.figure();plt.imshow(img_bgr);plt.show()

# Gürültü azaltma
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
   # plt.figure(); plt.imshow(blurred,cmap="gray");plt.title("blur");plt.show()

# Thresholding işlemi
    _, thresholded = cv2.threshold(blurred, 144, 255, cv2.THRESH_BINARY_INV)
 #   plt.figure(); plt.imshow(dialimg,cmap="gray");plt.title("threshold");plt.show()

    kernel = np.ones((5, 7), dtype=np.uint8)
    dialimg = cv2.dilate(thresholded, kernel, iterations=3)
   # plt.figure(); plt.imshow(dialimg,cmap="gray");plt.title("dilate");plt.show()
 
 
# Konturları bul
    contours, _ = cv2.findContours(dialimg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    


    text_areas = []
    for contour in contours:
       
        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)
       
        if (w < 155 and w > 100 and h < 50 and x>y):  # Minimum alan
                  text_areas.append((x, y, w, h))
                  #cv2.rectangle(img_bgr, (x, y), (x + w, y + h), (0, 255, 0), 1)

                  fis_noimg = img_bgr[y:y+h, x:x + w].copy()
                  fis_noimg = cv2.resize(fis_noimg, (130, 30), interpolation=cv2.INTER_LINEAR)
    
    plt.figure(); plt.imshow(fis_noimg);plt.title("kesım");plt.show()  

     
    return fis_noimg





