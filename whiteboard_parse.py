import parsecells
import imageparse
import sys
import os


if __name__ == '__main__':
    character = sys.argv[1]
    path_to_image = sys.argv[2]
    
    pwd = os.getcwd()
    
    path_to_csv = pwd + '/data'
    path_to_image_dir = pwd + '/cell_images'
    
    imageparse.parse_grid(path_to_image,pwd)
    parsecells.cell_to_csv(path_to_csv,path_to_image_dir,character)
