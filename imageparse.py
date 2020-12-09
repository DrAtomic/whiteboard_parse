import cv2
import numpy as np
import os
import csv

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

def cells_to_csv(cell, pwd, character):
    """takes a current cell and a character outputs a csv file of the key
    
    Args:
       cell: 2d array of cell
       pwd: path to working directory
       character: label of cell
    
    
    """
    
    flatten_list = [int(item) for sublist in cell for item in sublist]
    flatten_list.insert(0,character)

    with open(pwd + '/data/gathered_data.csv', 'a', newline='',encoding='utf-8') as fd:
        writer = csv.writer(fd)
        writer.writerow(flatten_list)
                

def analyze_cells(img,pwd,character):
    """takes an image and analyze_cells the cells, saves the cells in a folder
    
    Args:
       img: image
       pwd: path to working directory
       character: label for character
     
    """
    TARGET = 100 #number of cells
    percentage = 15
    percentage = percentage / 200
    
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
            cropped = gray[y:y+h, x:x+w]
            thresh = cv2.threshold(cropped, 127,255,cv2.THRESH_BINARY_INV)[1]
            mask = np.zeros((cropped.shape[0], cropped.shape[1]))
            x1 = cropped.shape[0]
            x2 = round(x1 * percentage)
            y1 = cropped.shape[1]
            y2 = round(y1 * percentage)
            mask[x2:x1-x2, y2:y1-y2] = 1
            masked_image = thresh * mask
            
            masked_image = cv2.resize(masked_image, (28,28))
            try:
                os.remove(pwd + '/cell_images/cell' + str(count) + '.jpg')
            except:
                pass
            cv2.imwrite(pwd+'/cell_images/cell' + str(count) + '.jpg',masked_image)
            count +=1
            
            cells_to_csv(masked_image, pwd, character)

def parse_grid(path_to_image,pwd,character):
    """takes a path to an image writes all the cells in a folder called cell_images
    
    Args:
       path_to_image: the path to an image
       pwd:           path to current working directory
       character:     label to character
    
    """
    img = cv2.imread(path_to_image)  
    analyze_cells(img,pwd,character)


#parse_grid("image0.jpg",os.getcwd(),'(')
