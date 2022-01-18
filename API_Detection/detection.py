import numpy as np
from numpy import asarray
from PIL import Image
import zipfile
import os

def segmentation(board):
    
    BORDER_SIZE = 3
    card_shape = (150,150)
    
    board = np.array(board)
    
    cards = []
    
    """border_matrix = np.empty([card_shape[0] + BORDER_SIZE , card_shape[1] + BORDER_SIZE])
    
    for x in range(card_shape[0] + BORDER_SIZE):
        for y in range(card_shape[1] + BORDER_SIZE):
            if min(x,y) < BORDER_SIZE or min(card_shape[0] - x -1,card_shape[1] - y -1) < BORDER_SIZE:
                border_matrix[x,y] = 1
            else:
                border_matrix[x,y] = 0
                
    number_border_pixel = border_matrix.sum()
    """

    vector = np.array([0 for i in range(card_shape[0] + 2*BORDER_SIZE)], dtype=float)
    vector[0:BORDER_SIZE] = 1/(2*BORDER_SIZE)
    vector[-BORDER_SIZE:] = 1/(2*BORDER_SIZE)
    
    img_board = Image.fromarray(np.array(board))
    grayscale_board = np.array(img_board.convert('L'))
    
    """print(grayscale_board[30,30])
    img = Image.fromarray(grayscale_board)
    img.show()"""
    means = []
    for column in range(0,board.shape[0] - card_shape[0] - 2*BORDER_SIZE):
        for row in range(0,board.shape[1] - card_shape[1] - 2*BORDER_SIZE ):
            subArray = grayscale_board[column:column+card_shape[0]+ 2*BORDER_SIZE,row:row+card_shape[1]+ 2*BORDER_SIZE]
            mean = np.average((np.dot(vector,subArray)+np.dot(subArray,vector))/2)
            means.append(mean)
            if mean <=20:
                cards.append(board[column + BORDER_SIZE:column + BORDER_SIZE + card_shape[0],
                                   row + BORDER_SIZE:row + BORDER_SIZE + card_shape[1]])
    return cards



def applyThreshold(image1,threshold):
    formatted_card = np.copy(image1)
    for x,column in enumerate(image1):
        for y,pixel in enumerate(column):
            formatted_card[x,y] = 0 if pixel < threshold else 255
    return formatted_card



def imageComparison(image1, image2):
    
    img1 = Image.fromarray(np.array(image1))
    grayscale_image1 = np.array(img1.convert('L'))
    #grayscale_image1 = applyThreshold(grayscale_image1,128)
    
    img2 = Image.fromarray(np.array(image2))
    grayscale_image2 = np.array(img2.convert('L'))
    #grayscale_image2 = applyThreshold(grayscale_image2,128)
    
    average_distance = np.mean(np.square(np.absolute(grayscale_image1 - grayscale_image2)))

    return average_distance < 20

def detection(board):
    background = Image.open("background.png")
    arrayBackground = asarray(background)
    
    cards = segmentation(board)
    
    return [card for card in cards if not imageComparison(background,card)]

"""
image = Image.open('board.jpg')
faceup = detection(image)

print(str(len(faceup)) + " cards face up")
for card in faceup:
    img = Image.fromarray(np.array(card))
    img.show()
    s
def zipped(image_array):
    zipf = zipfile.ZipFile('Name.zip','w', zipfile.ZIP_DEFLATED)
    for image in image_array:
        zipf.write(image.tobytes())
    zipf.close()
    return zipf

"""