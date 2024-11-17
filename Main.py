import sys
import pygame
import argparse
import SudokuRekognitionParser
import SudokuSolver
from pygame.locals import *

# How it works.
# starting reading numbers in rows once there are more than 1 in a row. At that point, we assume following rows are 
# part of sudoku board. We read until end of list, and truncate anything after 9 rows or columns to avoid page numbers
# or other noise. Board should be clean.
# Recommendation: make sure top of board is at top of photo.

parser = argparse.ArgumentParser(description="Sudoku Image Reader and Solver")
parser.add_argument('image', help='The image to process')
parser.add_argument('-d', '--data', required=True) # to avoid multiple calls during dev to aws.
parser.add_argument('-s', '--confidence', default=95.0, help='Rekognition Confidence')

args = parser.parse_args()

# Let us extract the response from json file here. Normally, we would make an API call for this data. Then we would filter 
# it so we only have the bounding boxes, ids, and detected number.
bounding_boxes = SudokuRekognitionParser.extractData(args.data, args.confidence)

# Pygame setup. To show the edited image
screen = pygame.display.set_mode((SudokuRekognitionParser.SCREEN_WIDTH, SudokuRekognitionParser.SCREEN_HEIGHT))
pygame.display.set_caption("Sudoku")
pygame.init()

# Load the background image
background = pygame.image.load(args.image).convert()
background = pygame.transform.scale(background, (SudokuRekognitionParser.SCREEN_WIDTH, SudokuRekognitionParser.SCREEN_HEIGHT))
screen.blit(background, (0, 0))

# debugging, and it looks kinda sick
SudokuRekognitionParser.drawBoxes(bounding_boxes, screen)

# 3rd - to fill for 9x9 grid, for each cell, check if there is a single common feature between row list and column list. 
# for column and row bunch sorted lists, for 9x9 index, eg check intersection row[x], col[y]. If none, empty.
matrix = SudokuRekognitionParser.createMatrix(bounding_boxes)

print("\nDetected Matrix")
print("------------------")
SudokuRekognitionParser.printMatrix(matrix)

solved = SudokuSolver.solveSudoku(matrix)

print("\nSolved Matrix")
print("------------------")
SudokuRekognitionParser.printMatrix(solved)

# Run loop to show display screen. This is mostly for demo purposes.
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()


pygame.quit()
sys.exit()

# Helper functions

