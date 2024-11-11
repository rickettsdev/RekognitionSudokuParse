import json
import sys
import pygame
from pygame.locals import *

WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Based off of results, ['Geometry']['BoundingBox'] and ['DetectedText'] attributes from Rekognition Text Analysis.
# 
# 1st - create list of elements by approximate row- only adding ones with more than 1 feature +-10 units away.
# 2nd - create list of elements by approximate column- only adding ones with more than 1 feature +-10 units away, AND greater than the average of the 1st row in previous step.
# 3rd - to fill for 9x9 grid, for each cell, check if there is a single common feature between row list and column list. 


bounding_boxes = []
with open('./sudoku_easy_response.json', 'r') as file:
    data = json.load(file)

    for detected in sorted(data['TextDetections'], key=lambda x: x['Geometry']['BoundingBox']['Left']):
        if detected['Confidence'] < 85.0 or detected['Type'] == 'LINE':
            continue
        map = {}
        map['box'] = detected['Geometry']['BoundingBox']
        map['text'] = detected['DetectedText']

        bounding_boxes.append(map)


screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Draw a Square")
pygame.init()

# Load the background image
background = pygame.image.load('test.jpg').convert()
background = pygame.transform.scale(background, (screen_width, screen_height))
screen.blit(background, (0, 0))

for box in  sorted(bounding_boxes, key=lambda x: x['box']['Top']):
    square_position2 = (screen_width * box['box']["Left"], screen_height * box['box']["Top"])
    square_size2 = (screen_width * box['box']["Width"], screen_height * box['box']["Height"])

    print("Box coords: x, y: " + str(square_position2) + " size: " + str(square_size2))

    pygame.draw.rect(screen, RED, (*square_position2, *square_size2), 2)

    font = pygame.font.Font(None, 36)
    word = box['text']
    print("Text: " + box['text'])
    text = font.render(word, True, WHITE)

    text_rect = text.get_rect(center=square_position2)
    
    screen.blit(text, text_rect)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()


pygame.quit()
sys.exit()