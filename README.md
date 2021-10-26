# Food_Ingredient_Parser
version 1.0 20211031 - bêta version

main credit: Tristan Salord, AGIR ODYCEE INRAE 

collaborators: [Guillaume Cabanac](https://www.irit.fr/~Guillaume.Cabanac/cv.pdf), [Marie-Benoît Magrini](https://www6.toulouse.inrae.fr/agir/Les-equipes/ODYCEE/Membres/Magrini-Marie-Benoit)

[INRAE](https://www.inrae.fr/), UMR 1248 AGIR 

Code hase been submitted to INRAE registration system.
Code is available under the GNU Reneral Public License

## Started gitRepo: 20210726

This file includes a detailed description of the github and instructions to execute code made available.

## Introduction

__General Purpose__
The Food Ingredient Parser(FIP) is a set of python scripts for parsing ingredient lists obtained by scanning product packaging. It has been specifically developed to analyse ingredient lists extracted from the [MINTEL GNPD](https://www.mintel.com/) food innovation database, and has not yet been tested on data from other similar databases - it will be updated for this purpose later(report to section "Improvements Planification"). 

__Why a new parser?__
Data from the MINTEL GNPD Database use different sorts of grammar to reproduce ingredients lists given in products packaging. Most of classical parsers failed on parsing such heterogenuous data. 

__Utility?__
Parsing food ingredient list, i.e transofrming raw ingredient list text into a structured data type allow to perform numerous scientific operation: identify certain types of ingredient, of species used in food composition, study food product evolution, assess food product complexity, etc.

__Performance__
FIP was tested on a large dataset of about 300,000 food ingredient lists extracted from MINTEL GNPD DB. It works with a margin of errors located under 2% depending on the size of the input data. 

__Evolution__
FIP will be updated until it reaches the point in its evolution where it can become a complete python library. 

## Instruction of Use

FIP runs with python3. It can works on any OS as long as python3 is installed. 

All required libraries are listed on the next section "__Required Libraries__" and the data structure of the parser is described in section "__Data Organisation__".

Script functions are described in the "__Script Description__" section. 


### Required Libraries

__Native Python Libraries__:

- os
- re
- time

__Libraries to be installed__:

- [thefuzz](https://github.com/seatgeek/thefuzz)
- numpy
- pandas

### Data Organisation

FIP must be downloaded or cloned respecting its tree structure.

The functional scripts are located under the "__Scripts__" folder and data to be parsed under the folder "__RawData__". Outputs of the scripts will be generated into a folder called "__ResultsYYYYMMDD__".

"Scripts" folder contains two main files, "__FIPFunc.py__" and "__FIPRun.py__". First file contains all python functions needed by FIP. File must not be deleted. "FIPRun.py" allows to launch the parser.

To start parsing a set of ingredient lists simply launch from your favorite IDE, or from terminal, the "FIPRun.py" file. 


### Script Description

[ to be populated ]

## Improvements Planification

+ Automatic recognition of input data
+ Structured Log File
+ MultiThreading
+ Benchmark on other FoodDB
