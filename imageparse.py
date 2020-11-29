import cv2
import numpy as np
from imutils import contours
import random
import os


#example!
#img = cv2.imread(path_to_image)


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

def process_image(img, skip_dilate=False):
    """takes an image and processes it
    
    Args:
       img: image to be processed
    
    Returns:
        processed image
    
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(9,9), 0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
    thresh = cv2.bitwise_not(thresh,thresh)
    
    
    if not skip_dilate:
        kernel = np.array([[0.0, 1.0, 0.0],
                           [1.0, 1.0, 1.0],
                           [0.0, 1.0, 0.0]],np.uint8)
        
        thresh = cv2.dilate(thresh,kernel)
        
    return thresh
#display_image(process_image(img))

def find_corners(image):
    """finds the conrers of the grid
    
    Args:
       image: processed image
    
    Returns:
        corner coordinates
    
    """
    # TODO: fix this. it rotates the image
    ext_contours = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    ext_contours = ext_contours[0] if len(ext_contours) == 2 else ext_contours[1]
    ext_contours = sorted(ext_contours, key=cv2.contourArea, reverse=True)

   
    for c in ext_contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.015 * peri, True)
        if len(approx) == 4:
            return approx
#t = find_corners(process_image(img))
#print(t)
        
def sort_corners(corners):
    """sorts corners clockwise
    
    Args:
       corners: unsorted corners
    
    Returns:
        sorted corners
    
    """
    corners = [(corner[0][0], corner[0][1]) for corner in corners]
    top_right, top_left, bottom_left, bottom_right = corners[0], corners[1], corners[2],corners[3] #[x_coord, y_coord]
    return  top_left, top_right,  bottom_right, bottom_left



def crop_image(image, corners):
    """crops an image at the grid
    
    Args:
       image: original image
       corners: unsorted corners
    
    Returns:
        cropped image that you can see with display_image()
    
    """
    orderd_corners = sort_corners(corners)
    top_left, top_right, bottom_right, bottom_left = orderd_corners
    
    
    #determine the new croped image
    ## first find the greatest width between top or bottom
    bottom_width = np.sqrt(((bottom_right[0] - bottom_left[0]) ** 2) + ((bottom_right[1] - bottom_left[1]) ** 2))
    top_width = np.sqrt(((top_right[0] - top_left[0]) ** 2) + ((top_right[1] - top_left[1]) ** 2))
    width = max(int(bottom_width),int(top_width))
    
    ## find greatest height
    right_height = np.sqrt(((top_right[0] - bottom_right[0]) ** 2) + ((top_right[1] - bottom_right[1]) ** 2))
    left_height = np.sqrt(((top_left[0] - bottom_left[0]) ** 2) + ((top_left[1] - bottom_left[1]) ** 2))
    height = max(int(right_height), int(left_height))
    
    dimensions = np.array([[0, 0],
                           [width - 1, 0],
                           [width - 1, height - 1],
                           [0, height - 1]],
                          dtype="float32")
    
    orderd_corners = np.array(orderd_corners, dtype="float32")
    grid = cv2.getPerspectiveTransform(orderd_corners,dimensions)
    
    return cv2.warpPerspective(image, grid, (width, height))
#display_image(crop_image(img,find_corners(process_image(img))))

#x = crop_image(img,find_corners(process_image(img)))


def analyze_cells(img,pwd):
    """takes a croped image and analyze_cells the cells, saves pixels of cells into a row in a csv
    
    Args:
       img: croped image
       pwd: path to working directory
    
    """


    # TODO: instead of this lets just iterate through the contours
    grid = np.copy(img)
    edge_h = np.shape(grid)[0]
    edge_w = np.shape(grid)[1]
    # FIXME: when you get a better board fix the cells. you better make a 10x10 grid
    NUMBER_OF_CELLS = 7
    cell_edge_h = edge_h // NUMBER_OF_CELLS
    cell_edge_w = edge_w // NUMBER_OF_CELLS
    
    grid = cv2.cvtColor(grid, cv2.COLOR_BGR2GRAY)

    grid = cv2.bitwise_not(grid,grid)

    temp_grid = []
    for i in range(cell_edge_h, edge_h + 1, cell_edge_h):
        for j in range(cell_edge_w, edge_w + 1, cell_edge_w):
            rows = grid[i - cell_edge_h:i]
            temp_grid.append([rows[k][j - cell_edge_w:j] for k in range(len(rows))])

    final_grid = []
    for i in range(0, len(temp_grid) - (NUMBER_OF_CELLS - 1), NUMBER_OF_CELLS):
        final_grid.append(temp_grid[i:i + NUMBER_OF_CELLS])
  
    
    for i in range(NUMBER_OF_CELLS):
        for j in range(NUMBER_OF_CELLS):
            final_grid[i][j] = np.array(final_grid[i][j])

    try:
        for i in range(NUMBER_OF_CELLS):
            for j in range(NUMBER_OF_CELLS):
                np.os.remove(pwd + "/cell_images/cell" + str(i) + str(j) + ".jpg")
    except:
        pass
    for i in range(NUMBER_OF_CELLS):
        for j in range(NUMBER_OF_CELLS):
            cv2.imwrite(str(pwd + "/cell_images/cell" + str(i) + str(j) + ".jpg"), final_grid[i][j])

    return final_grid


def parse_grid(path_to_image,pwd):
    """takes a path to an image writes all the cells in a folder called cell_images

    Args:
       path_to_image: the path to an image


    """
    img = cv2.imread(path_to_image)
    
    analyze_cells(crop_image(img,find_corners(process_image(img))),pwd)


