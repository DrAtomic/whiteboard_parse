import cv2
import numpy as np
import os


#example!

#img = cv2.imread('image0.jpg')


def display_image(img):
    """displays an image
    
    Args:
       img: image to be displayed
    
    
    """

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#display_image(img)



def analyze_cells(img,pwd):
    """takes an image and analyze_cells the cells, saves the cells in a folder
    
    Args:
       img: image
       pwd: path to working directory
    
    """
    TARGET = 100 #number of cells
    kernels = [x for x in range(3,249) if x%2 != 0]
    kernel = kernels[round(len(kernels)/2)]

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    heirarchy = [[],[]]
    while (len(heirarchy[0]) != TARGET + 1):
        blur = cv2.GaussianBlur(gray, (kernel,kernel), 0)
        thresh = cv2.threshold(blur,127,255,cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        cnts, heirarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        
        if (len(heirarchy[0]) < TARGET + 1):
            kernels = [x for x in range(kernels[0], kernel) if x%2 !=0]
            kernel = kernels[round(len(kernels)/2)]
        else:
            kernels = [x for x in range(kernel, kernels[-1])]
            kernel = kernels[round(len(kernels)/2)]
        

    count = 0
    for i in range(len(cnts)):
        if (heirarchy[0][i][3] != -1):
            x,y,w,h = cv2.boundingRect(cnts[i])
            cropped = img[y:y+h, x:x+w]
            try:
                os.remove(pwd + '/cell_images/cell' + str(count) + '.jpg')
            except:
                pass
            cv2.imwrite(pwd+'/cell_images/cell' + str(count) + '.jpg',cropped)
            count +=1

def parse_grid(path_to_image,pwd):
    """takes a path to an image writes all the cells in a folder called cell_images

    Args:
       path_to_image: the path to an image


    """
    img = cv2.imread(path_to_image)  
    analyze_cells(img,pwd)


#parse_grid("image0.jpg",os.getcwd())
