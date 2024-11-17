# RekognitionSudokuParse
Takes json data generated from Rekognition of an image with a Sudoku board on it. 

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


We use hard coded response and image pairs to avoid cost of multiple invocation to AWS. Here is 
an example of the response: https://docs.aws.amazon.com/rekognition/latest/dg/text-detecting-text-procedure.html#text-response