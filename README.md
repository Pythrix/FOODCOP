# FOODCOP

> For FOOd COmposition Parser

FOODCOP BETA 1.11.12 [beta number.beta month.beta day] - 2021

main credit: Tristan Salord, AGIR ODYCEE INRAE 

collaborators: [Guillaume Cabanac](https://www.irit.fr/~Guillaume.Cabanac/cv.pdf), [Marie-Benoît Magrini](https://www6.toulouse.inrae.fr/agir/Les-equipes/ODYCEE/Membres/Magrini-Marie-Benoit)

[INRAE](https://www.inrae.fr/), UMR 1248 AGIR 

Code hase been submitted to INRAE registration system.
Code is available under the GNU Reneral Public License

## Started gitRepo: 20210726

This file includes a detailed description of the github and instructions to execute code made available.

## Introduction

__General Purpose__
FOODCOP( for FOOd COmposition Parser) is a set of python scripts for parsing ingredient lists obtained by scanning product packaging. 

It is, actually, fully operative to analyse ingredient lists extracted from the [MINTEL GNPD](https://www.mintel.com/) food innovation database, and will be benchmarked/enhanced to work on other food Database soon (report to section "Improvements Planification"). 

__Why a new(?) parser__
Data from the MINTEL GNPD Database use different sorts of grammar to reproduce ingredients lists given in products packaging. Most of classical parsers failed on parsing such heterogenuous data. 

__Utility/Use__
Parsing food ingredient list, i.e transofrming raw ingredient list text into a structured data type allow to perform numerous scientific operation: identify certain types of ingredient, of species used in food composition, study food product evolution, assess food product complexity, etc.

__Performance__
FOODCOP was tested on a large dataset of about 300,000 food ingredient lists extracted from MINTEL GNPD DB. It works with a margin of errors located under 2% depending on the size of the input data. 

__Evolution__
FOODCOP will be updated until it reaches the point in its evolution where it can become a complete python library. 

## Instruction of Use

FOODCOP runs with python3. It can works on any OS as long as python3 is installed. 

All required libraries are listed on the next section "__Required Libraries__" and the data structure of the parser is described in section "__Data Organisation__".

Script functions are described in the "__Script Description__" section.

### Usage
Once installed all __required librairies__ simply:

- open a terminal,
- navigate to folder FOODCOP you have downloaded
- run the foodcoprun.py file with the __correct arguments__ (for now -d for dataframe usage or -f for single raw ingredient list): "python3 foodcoprun.py [-d] [-f]"
- Results and Log file are automatically saved in a folder named "FOODCOP"+date of operation located into __the user folder__ (i.e /Users/myusername on MACOS).

### Example of Use:

__Decoding simple raw ingredient list__:
- python3 foodcoprun.py -f "water (50%),acidifier(salt, citric acid), wheat flour, soybean oil, coconut"
- follow your terminal information
  
  N.B: Will be soon updated for complex ingredient list
  
__Decoding full dataframe__:
- python3 foodcoprun.py -d "path/to/ur/excel/or/csv/file"
- follow your terminal information
- fully operational 


### Required Libraries

__Libraries to be installed__:

- [thefuzz](https://github.com/seatgeek/thefuzz)
- numpy
- pandas
- openpyxl (to export as xlsx from pandas)
- python-Levenshtein

To simplify installation in your testing environment: "pip install -r requirements.txt"


### Data Organisation
[_TO UPDATE_]



### Script Description

[ to be populated ]

## Improvements Planification

+ User choice for output directory
+ More verbose Log File
+ MultiThreading
+ Benchmark on other FoodDB
