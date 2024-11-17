# RekognitionSudokuParse
Takes json data generated from Rekognition of an image with a Sudoku board on it. Displays
to terminal the solution for the scanned board. Please make sure board is clean.

Python was managed using a virtual environment.

example command:

python Main.py examples/sudoku_easy.jpg -d examples/sudoku_easy.json

should generate

Detected Matrix
------------------
2 0 0 8 6 0 4 1 0 

0 0 4 3 0 1 5 0 0 

0 1 0 0 0 2 7 0 0 

3 0 6 0 5 0 0 0 0 

5 0 0 1 0 4 0 0 6 

0 0 0 0 8 0 9 0 4 

0 0 7 4 0 0 0 3 0 

0 0 1 9 0 6 2 0 0 

0 6 3 0 2 8 0 0 5 


Solved Matrix
------------------
2 3 5 8 6 7 4 1 9 

7 8 4 3 9 1 5 6 2 

6 1 9 5 4 2 7 8 3 

3 4 6 2 5 9 8 7 1 

5 9 8 1 7 4 3 2 6 

1 7 2 6 8 3 9 5 4 

9 2 7 4 1 5 6 3 8 

8 5 1 9 3 6 2 4 7 

4 6 3 7 2 8 1 9 5 

We use hard coded response and image pairs to avoid cost of multiple invocation to AWS. Here is 
an example of the response: https://docs.aws.amazon.com/rekognition/latest/dg/text-detecting-text-procedure.html#text-response