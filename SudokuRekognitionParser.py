import json
from typing import Any
from typing import Tuple
import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)

def createMatrix(bounding_boxes: list) -> list[list[int]]:
    (columnBunchSorted, rowBunchSorted) = rowColSorted(bounding_boxes)
    matrix =[[0 for _ in range(len(rowBunchSorted))] for _ in range(len(columnBunchSorted))]
    for x in range(len(columnBunchSorted)):
        for y in range(len(rowBunchSorted)):
            xgroup = columnBunchSorted[x]
            ygroup = rowBunchSorted[y]
            intersection = list(set(xgroup) & set(ygroup))
            if len(intersection) == 1: 
                matrix[x][y] = intersection[0][-1]
            elif len(intersection) > 1:
                raise Exception("Collision in matrix slot! Try a cleaner photo.");
    return matrix

def printMatrix(matrix: list[list[int]]):
    # Print out the detected matrix 
    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
            print(str(matrix[x][y]), end=" ")
        print("\n")

def extractData(response: str, confidence: float)-> list[dict]:
    bounding_boxes = []
    with open(response, 'r') as file:
        data = json.load(file)

        for detected in sorted(data['TextDetections'], key=lambda x: x['Geometry']['BoundingBox']['Left']):
            if detected['Confidence'] < confidence or detected['Type'] == 'LINE' or not detected['DetectedText'].isdigit():
                continue
            map = {}
            map['box'] = detected['Geometry']['BoundingBox']
            map['text'] = detected['DetectedText']
            map['id'] = detected['Id']

            bounding_boxes.append(map)

    return bounding_boxes

def drawBoxes(bounding_boxes: list, screen: Any):
    for box in sorted(bounding_boxes, key=lambda x: x['box']['Top']):
        square_position2 = (SCREEN_WIDTH * box['box']["Left"], SCREEN_HEIGHT * box['box']["Top"])
        square_size2 = (SCREEN_WIDTH * box['box']["Width"], SCREEN_HEIGHT * box['box']["Height"])

        pygame.draw.rect(screen, RED, (*square_position2, *square_size2), 2)

        font = pygame.font.Font(None, 36)
        word = box['text']
        text = font.render(word, True, WHITE)

        text_rect = text.get_rect(center=square_position2)
        
        screen.blit(text, text_rect)

# This is where the hacky stuff begins. a few magic numbers. ideally needs updated.
def rowColSorted(bounding_boxes: list) -> Tuple[list,list]:
    columnBunchSorted = []
    currentBunch = []
    lastTop = 0
    lowest = 0

    # 1st - create list of elements by approximate row- only adding ones with more than 1 feature +-30 units away.
    levels = 0

    for box in sorted(bounding_boxes, key=lambda x: x['box']['Top']):
        currentTop = box['box']['Top'] * 1000
        if ((currentTop) - (lastTop)) > 30:
            if len(currentBunch) > 1 or (len(columnBunchSorted) > 0 and len(currentBunch) > 0):
                if lowest == 0:
                    lowest = lastTop
                columnBunchSorted.append(currentBunch.copy())
            currentBunch.clear()
        currentBunch.append(str(box['id']) + "-" + box['text']) ## to keep it unique from others. 
        lastTop = currentTop
        levels = levels + 1
    columnBunchSorted.append(currentBunch.copy())

    columnBunchSorted = columnBunchSorted[0:9]

    rowBunchSorted = []
    currentBunch = []
    lastLeft = 0

    # 2nd - create list of elements by approximate column- only adding ones with more than 1 feature +-30 units away, AND greater than the average of the 1st row in previous step.
    levels = 0

    for box in sorted(bounding_boxes, key=lambda x: x['box']['Left']):
        currentLeft = box['box']['Left'] * 1000
        if currentLeft - lastLeft > 30:
            if len(currentBunch) > 1 or (len(rowBunchSorted) > 0 and len(currentBunch) > 0):
                rowBunchSorted.append(currentBunch.copy())
            currentBunch.clear()
        if box['box']['Top'] * 1000 > lowest - 20:
            currentBunch.append(str(box['id']) + "-" + box['text'])
            lastLeft = currentLeft
        levels = levels + 1
    rowBunchSorted.append(currentBunch.copy())

    rowBunchSorted = rowBunchSorted[0:9]

    return (columnBunchSorted, rowBunchSorted)