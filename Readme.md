# Implementation of Electre Iv MCDA Method
## Created based on: *https://github.com/tesserato/Electre_I_Python* project

Method is described (using provided data) in polish in:

Cabała, P. Wykorzystanie metod ELECTRE w projektowaniu złożonych systemów organizacyjnych, Zeszyty Naukowe UEK 2013, 905: 5-20

Data is provided in data.csv file:
* second row contains weights for each of grading funcions;
* third row contains veto rate for each of grading funcions;
* next rows contains grades for given decision variant for each of grading funcions;

c | g1 | g2 | g3 | g4
--- | --- | --- | --- | ---
w | 0.25 | 0.15 | 0.35 | 0.25
v | 1 | 2 | 3 | 2
a1 | 3 | 2 | 4 | 5
a2 | 2 | 5 | 2 | 3
a3 | 2 | 3 | 5 | 2
a4 | 4 | 4 | 2 | 4
a5 | 4 | 3 | 1 | 5
