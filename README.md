# MINTEL Ingredient List Parser

Mintel Ingredient List Parser BETA 1.11.12 [beta number.beta month.beta day] - 2021

main credit: Tristan Salord, AGIR ODYCEE INRAE 

collaborators: [Guillaume Cabanac](https://www.irit.fr/~Guillaume.Cabanac/cv.pdf), [Marie-Benoît Magrini](https://www6.toulouse.inrae.fr/agir/Les-equipes/ODYCEE/Membres/Magrini-Marie-Benoit)

[INRAE](https://www.inrae.fr/), UMR 1248 AGIR 

Code hase been submitted to INRAE registration system.
Code is available under the GNU Reneral Public License

## Started gitRepo: 20210726

This file includes a detailed description of the github and instructions to execute code made available.

## Introduction

__General Purpose__
This Food Ingredient Parser(MILP for Mintel Ingredient List Parser) is a set of python scripts for parsing ingredient lists obtained by scanning product packaging. It has been specifically developed to analyse ingredient lists extracted from the [MINTEL GNPD](https://www.mintel.com/) food innovation database, and has not yet been tested on data from other similar databases - it will be updated for this purpose later(report to section "Improvements Planification"). 

__Why a new parser?__
Data from the MINTEL GNPD Database use different sorts of grammar to reproduce ingredients lists given in products packaging. Most of classical parsers failed on parsing such heterogenuous data. 

__Utility?__
Parsing food ingredient list, i.e transofrming raw ingredient list text into a structured data type allow to perform numerous scientific operation: identify certain types of ingredient, of species used in food composition, study food product evolution, assess food product complexity, etc.

__Performance__
MILP was tested on a large dataset of about 300,000 food ingredient lists extracted from MINTEL GNPD DB. It works with a margin of errors located under 2% depending on the size of the input data. 

__Evolution__
MILP will be updated until it reaches the point in its evolution where it can become a complete python library. 

## Instruction of Use

MILP runs with python3. It can works on any OS as long as python3 is installed. 

All required libraries are listed on the next section "__Required Libraries__" and the data structure of the parser is described in section "__Data Organisation__".

Script functions are described in the "__Script Description__" section.

### Usage
Once installed all __required librairies__ simply:

- open a terminal,
- navigate to folder MILP you have downloaded
- run the MILPRun.py file with the __correct arguments__ (for now -d for dataframe usage or -f for single raw ingredient list): "python3 MILPRun.py [-d] [-f]"
- Results and Log file are automatically saved in a folder named "MILP"+date of operation located into __the user folder__ (i.e /Users/myusername on MACOS).

### Example of Use:

__Decoding simple raw ingredient list__:
- python3 MILPRun.py -f "water (50%),acidifier(salt, citric acid), wheat flour, soybean oil, coconut"
- follow your terminal information
  
  N.B: Will be soon updated for complex ingredient list
  
__Decoding full dataframe__:
- python3 MILPRun.py -d "path/to/ur/excel/or/csv/file"
- follow your terminal information


### Required Libraries

__Native Python Libraries__:

- os
- re
- time

__Libraries to be installed__:

- [thefuzz](https://github.com/seatgeek/thefuzz)
- numpy
- pandas
- - python-Levenshtein

### Data Organisation
[_TO UPDATE_]



### Script Description

[ to be populated ]

## Improvements Planification

+ User choice for output directory
+ More verbose Log File
+ MultiThreading
+ Benchmark on other FoodDB
