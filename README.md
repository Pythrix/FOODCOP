# Food_Ingredient_Parser
version 1.0 20211031 - bêta version
authors: Tristan Salord, Marie-Benoît Magrini, Guillaume Cabanac

[INRAE](https://www.inrae.fr/), UMR 1248 AGIR 

Code hase been submitted to INRAE registration system.
Code is available under the GNU Reneral Public License

## Started gitRepo: 20210726

This file includes a detailed description of the github and instructions to execute code made available.

## Introduction

__General Purpose__
The Food Ingredient Parser(FIP) is a set of python scripts for parsing ingredient lists obtained by scanning product packaging. It has been specifically developed to analyse ingredient lists extracted from the [MINTEL GNPD](https://www.mintel.com/) food innovation database, and has not yet been tested on data from other similar databases - it will be updated for this purpose later. 

__Why a new parser?__
Data from the MINTEL GNPD Database use different sorts of grammar to reproduce ingredients lists given in products packaging. Most of classical parsers failed on parsing such heterogenuous data. 

__Utility?__
Parsing food ingredient list, i.e transofrming raw ingredient list text into a structured data type allow to perform numerous scientific operation: identify certain types of ingredient, of species used in food composition, study food product evolution, assess food product complexity, etc.

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



### Script Description

## Improvements Planification
