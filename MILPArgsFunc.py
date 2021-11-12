#! /usr/bin/env python3
# coding: utf-8
### Mintel Ingredient List Parser BETA 1.11.12 [beta number.beta month.beta day] - 2021
### coding: TriX [tristan.salord[at]inrae.fr]
### Original Work under Licence Creative Common CC-BY-NC https://creativecommons.org/licenses/by-nc/4.0/deed.en
### Work was registered at INRAE 04/10/2021



from datetime import date
import logging
from MILPCoreFunc import *
import numpy as np
import os

#### Global Variables
dftoparse=''
coltoparse=''
idstouse=''
stringGrammar=''
stringCom=''
lexedstring=''

#### General Variables
todayrun = date.today()
todaycode = todayrun.strftime("%Y%m%d")
workingdir = os.getcwd()

## for output folder and logging directories creation
splitedtreedirectory = workingdir.split('/')
savelocation = '/'.join(splitedtreedirectory[:3])
outputdirname = 'MILP_Out_'+str(todaycode)
savefolder = os.path.join(savelocation,outputdirname)
savexist = os.path.exists(savefolder)
if savexist is False:
    os.makedirs(savefolder)

## Generate logger file
logging.basicConfig(filename=os.path.join(savefolder,'FiPInf.log'),
                    format='%(asctime)s %(levelname)s %(message)s',
                    filemode='w',
                    level=logging.INFO)
logger=logging.getLogger()




## Raw string Operation

def stringprocess(rawingredientlist):
    global stringGrammar
    global lexedstring
    global stringCom
    cleanedinglist = simpleformater(rawingredientlist)
    comp = casechecker(cleanedinglist)
    commented = commentchecker(cleanedinglist)
    lexedinglist = []
    if commented is True:
        stringCom = commentextract(cleanedinglist)
        lexedinglist = inglexer(stringCom[0])
    else:
        lexedinglist = inglexer(cleanedinglist)
    lexedstring = lexedinglist
    adds = fuzzaddchecker(lexedinglist)
    grammar=(comp,commented,adds)
    stringGrammar = grammar
    interpreterdict = {(True,True,True): 'Formula is a oneline ingredient list, containing comment(s) and additive(s) category(ies)',
     (True,True,False): 'Formula is a oneline ingredient list  containing comment(s) with no additive category',
     (True,False,True): 'Formula is a oneline ingredient list with no comment containing additive(s) category(ies)',
     (True,False,False): 'Formula is a oneline ingredient list with no comment or additive(s) category(ies)',
     (False,False,False): 'Formula is a multi line ingredient list with no comment and no additive category',
     (False,True,False): 'Formula is a multi line ingredient list containing comment(s) with no additive category',
     (False,False,True): 'Formula is a multi line ingredient list with no comment containing additive(s) category(ies)',
     (False,True,True): 'Formula is a multi line ingredient list containing comment(s) and additive(s) category(ies)'}
    r=interpreterdict[grammar]
    print(interpreterdict[grammar])
    print('Would you like to display lexed ingredient list? Enter [Y] or [N]')
    answear = input("")
    parsephase = 'N'
    if answear not in ['Y','N']:
        print('\t'+'*** Please answear \"Y\" or \"N\" ***')
        answear = input("")
    else:
        if answear == 'Y':
            print(lexedstring)
            print('Do u want to parse ingredient list: [Y] or [N] ?')
            parsephase = input("")
        else:
            print('U can either directly parse ingredient list: [Y] or [N] ?')
            parsephase = input("")
    if parsephase == 'Y':
        return stringparser(lexedstring)


def stringparser(lexedinglist: list):
    global stringGrammar
    global stringCom
    def proptest(lexedinglist: list):
        failed = False
        result = []
        try:
            r=propextract(lexedinglist)
            result = r
        except:
              failed = True
        if failed == False:
            return result
        else:
            return failed

    def addextest(lexedinglist: list):
        failed = False
        result=[]
        try:
            r=fuzzaddextract(lexedinglist)
            result = r
        except:
            failed = True
        if failed == False:
            return result
        else:
            return failed 
    
    if stringGrammar == (True,False,False):
        extractedprop=proptest(lexedinglist)
        if type(extractedprop) is bool :
            return 'Proportion Extraction Failed'
        else:
            try:
                if len(extractedprop[1]) > 0:
                    return builder(str(todaycode),extractedprop[0],extractedprop[1],None,None)
                else:
                    return builder(str(todaycode),extractedprop[0],None,None,None)
            except:
                logger.debug('Processing raw ingredient list failed')
                return 'Builder Failed'
    elif stringGrammar == (True,False,True):
        addsres = addextest(lexedinglist)
        if type(addsres) is bool:
            logger.debug('Additives Category extraction failed')
            return 'Additives Extraction Failed'
        else:
            extractedprop=proptest(addsres[0])
            if extractedprop == False:
                logger.debug('Proportion extraction failed')
                return 'Proportion Extraction Failed'
            else:
                try:
                    if len(extractedprop[1]) > 0:
                        return builder(str(todaycode),extractedprop[0],extractedprop[1],None,addsres[1])
                    else:
                        return builder(str(todaycode),extractedprop[0],None,None,addsres[1])
                except:
                    logger.debug('Processing raw ingredient list failed')
                    return 'Builder Failed'
    elif stringGrammar == (True,True,True):
        coms = stringCom[1] 
        addsres = addextest(lexedinglist)
        if type(addsres) is bool:
            logger.debug('Additives Category extraction failed')
            return 'Additives Extraction Failed'
        else:
            extractedprop=proptest(addsres[0])
            if type(extractedprop) is bool:
                logger.debug('Proportion extraction failed')
                return 'Proportion Extraction Failed'
            else:
                try:
                    if len(extractedprop[1]) > 0:
                        return builder(str(todaycode),extractedprop[0],extractedprop[1],coms,addsres[1])
                    else:
                        return builder(str(todaycode),extractedprop[0],None,coms,addsres[1])
                except:
                    logger.debug('Processing raw ingredient list failed')
                    return 'Builder Failed'
    elif stringGrammar == (True,True,False):
        coms = stringCom[1]
        extractedprop=proptest(lexedinglist)
        if type(extractedprop) is bool:
                logger.debug('Proportion extraction failed')
                return 'Proportion Extraction Failed'
        else:
            try:
                if len(extractedprop[1]) > 0:
                    return builder(str(todaycode),extractedprop[0],extractedprop[1],coms,None)
                else:
                    return builder(str(todaycode),extractedprop[0],None,coms,None)
            except:
                logger.debug('Processing raw ingredient list failed')
                return 'Builder Failed'


######## Data Frame Operation

### Minimalist Interactive Data Loader

def dataexplorer(dataframe: str):
    global coltoparse
    global dftoparse
    global idstouse
    fileis = os.path.basename(dataframe)
    print('Wait during dataframe loading.')
    logger.info('Started Dataframe import')
    if fileis[-4:] == '.csv':
        ingDf = pd.read_csv(dataframe)
    else:
        ingDf = pd.read_excel(dataframe)
    dftoparse = ingDf
    logger.info('Ended Dataframe import')
    dfcols= [x for x in ingDf.columns]
    dflgth = len(ingDf)
    nbcols = len(dfcols)
    print(f'Dataframe is composed of {nbcols} columns, contains {dflgth} rows to parse."')
    
    print('Please inform dataframe language: [en] for english or [fr] for french')
    lang = input("")
    supposedinglist = []
    supposedids = []
    if lang == 'fr':
        supposedinglist = [x for x in dfcols if x.lower().startswith('ingredient') or x.lower().startswith('ingrédient')]
        supposedids = [x for x in dfcols if x.lower().startswith('numéro') or x.lower() == 'code barre']
    elif lang == 'en':
        supposedinglist = [x for x in dfcols if x.lower().startswith('ingredients')]
        supposedids = [x for x in dfcols if x.lower() in ['record id','bar code']]
    else:
        print('Wrong language selection. Progam will interrupt')

    print(f'Are u OK with detected ingredient column,\"{supposedinglist[0]}\" [Y][N]?')
    answear = input("")
    if answear not in ['Y','N']:
        print('\t'+'*** Please answear \"Y\" or \"N\" ***')
        answear = input("")
    else:
        if answear == 'Y':
            coltoparse = supposedinglist[0]
        elif answear == 'N':
            print('Please enter correct column name to parse')
            altercol = input("")
            if altercol.replace('\\n','\n') not in dfcols:
                print('\t'+'*** Programm will quit. Invalid column name informed ***')
            else:
                coltoparse = altercol.replace('\\n','\n')
    print(supposedids)
    c1 = supposedids[0]
    c2 = supposedids[1]
    print(f'Which id number do u wish to use: db ids [D] or product bar code [P]?')
    idansw = input("")
    if idansw not in ['D','P']:
        print('\t'+'Choose between [D] for db ids, or [P] for product bar code')
        idansw = input("")
    else:
        if idansw == 'D':
            idstouse = c1
        elif idansw == 'P':
            idstouse = c2
        else:
            print('\t'+'*** You choose a wrong Ids cols, programm will quit. ***')

    print(f'Program will parse \"{coltoparse}\", containing {dflgth} ingredients list using \"{idstouse}\" as ids for ingredients dictionary building')


### Dataframe Process

def dataprocess():
    global dftoparse
    if len(dftoparse) > 0:
        df = prepareDf(dftoparse, coltoparse)
        df['IngDict'] = df.apply(DfBuilderCondition,axis = 1)
        nberror=len(df[df.IngDict.str.contains('Failed',na=False)])+len(df[df.IngDict.isnull()])
        logger.info(f'Parsing finished with {round((nberror/len(df))*100,2)} \% of errors')
        print(f'Finished with an error rate of {round((nberror/len(df))*100,2)} \%')
        logger.info('End Parsing Ingredient Lists')
        logger.info('Saving Dataframe')
        savefilename = 'IngdictDataFrame_'+str(todaycode)+'.xlsx'
        df.to_excel(os.path.join(savefolder,savefilename))
        logger.info('Finished Processing Dataframe')
    else:
        logger.debug('No Dataframe to log')



### Core dataframe operations
def prepareDf(dataframe,rawingCol):
    dataframe['Case'] = np.vectorize(simpleformater)(dataframe[rawingCol])
    dataframe['SimpComp'] = np.vectorize(casechecker)(dataframe['Case'])
    dataframe['ComOrNot'] = np.vectorize(commentchecker)(dataframe['Case'])
    dataframe['ExtractedComs'] = np.where(dataframe['ComOrNot'] == True,dataframe['Case'].apply(commentextract).str[1], 'NA')
    dataframe['StringWoCom'] = np.where(dataframe['ComOrNot'] == True,dataframe['Case'].apply(commentextract).str[0],dataframe['Case'] )
    dataframe['Lexed'] = dataframe['StringWoCom'].apply(inglexer)
    

    return dataframe

##### Action

def DfBuilderCondition(row):
    global idstouse
    def proptest(lexedinglist: list):
        failed = False
        result = []
        try:
            r=propextract(lexedinglist)
            result = r
        except:
              failed = True
        if failed == False:
            return result
        else:
            return failed

    def addextest(lexedinglist: list):
        failed = False
        result=[]
        try:
            r=fuzzaddextract(lexedinglist)
            result = r
        except:
            failed = True
        if failed == False:
            return result
        else:
            return failed 

    if row['SimpComp'] == True and row['ExtractedComs'] == 'NA':
        if fuzzaddchecker(row['Lexed']) == False :
            extractedprop=proptest(row['Lexed'])
            if type(extractedprop) is bool :
                return 'Proportion Extraction Failed'
            else:
                try:
                    if len(extractedprop[1]) > 0:
                        return builder(str(row[idstouse]),extractedprop[0],extractedprop[1],None,None)
                    else:
                        return builder(str(row[idstouse]),extractedprop[0],None,None,None)
                except:
                    return 'Builder Failed'
        else: 
            addsres = addextest(row['Lexed'])
            if type(addsres) is bool:
                return 'Additives Extraction Failed'
            else:
                extractedprop=proptest(addsres[0])
                if extractedprop == False:
                    return 'Proportion Extraction Failed'
                else:
                    try:
                        if len(extractedprop[1]) > 0:
                            return builder(str(row[idstouse]),extractedprop[0],extractedprop[1],None,addsres[1])
                        else:
                            return builder(str(row[idstouse]),extractedprop[0],None,None,addsres[1])
                    except:
                        return 'Builder Failed'
   
    elif row['SimpComp'] == True and row['ExtractedComs'] != 'NA':
        if fuzzaddchecker(row['Lexed']) == False :
            extractedprop=proptest(row['Lexed'])
            if type(extractedprop) is bool:
                return 'Proportion Extraction Failed'
            else:
                try:
                    if len(extractedprop[1]) > 0:
                        return builder(str(row[idstouse]),extractedprop[0],extractedprop[1],row['ExtractedComs'],None)
                    else:
                        return builder(str(row[idstouse]),extractedprop[0],None,row['ExtractedComs'],None)
                except:
                    return 'Builder Failed'
        else:
            addsres = addextest(row['Lexed'])
            if type(addsres) is bool:
                return 'Additives Extraction Failed'
            else:
                extractedprop=proptest(addsres[0])
                if type(extractedprop) is bool:
                    return 'Proportion Extraction Failed'
                else:
                    try:
                        if len(extractedprop[1]) > 0:
                            return builder(str(row[idstouse]),extractedprop[0],extractedprop[1],row['ExtractedComs'],addsres[1])
                        else:
                            return builder(str(row[idstouse]),extractedprop[0],None,row['ExtractedComs'],addsres[1])
                    except:
                        return 'Builder Failed'
            
    elif row['SimpComp'] == False and row['ExtractedComs'] == 'NA':
        listoflist=[x for x in row['Lexed'] if type(x) is list]
        if len(listoflist) == 0:
            if fuzzaddchecker(row['Lexed']) == False :
                extractedprop=proptest(row['Lexed'])
                if type(extractedprop) is bool:
                    return 'Proportion Extraction Failed'
                else:
                    try:
                        if len(extractedprop[1]) > 0:
                            return builder(str(row[idstouse]),extractedprop[0],extractedprop[1],None,None)
                        else:
                            return builder(str(row[idstouse]),extractedprop[0],None,None,None)
                    except:
                        return 'Builder Failed'
            else: 
                addsres = addextest(row['Lexed'])
                if type(addsres) is bool:
                    return 'Additives Extraction Failed'
                else:
                    extractedprop=proptest(addsres[0])
                    if type(extractedprop) is bool:
                        return 'Proportion Extraction Failed'
                    else:
                        try:
                            if len(extractedprop[1]) > 0:
                                return builder(str(row[idstouse]),extractedprop[0],extractedprop[1],None,addsres[1])
                            else:
                                return builder(str(row[idstouse]),extractedprop[0],None,None,addsres[1])
                        except:
                            return 'Builder Failed'
        else:
            if complexfuzzaddchecker(row['Lexed']) == False:
                try: 
                    metadict={}
                    countmeta = 0
                    for part in row['Lexed']:
                        countmeta +=1
                        cleaned=propextract(part)
                        tempdict=builder(str(row[idstouse]),cleaned[0],cleaned[1],None,None)
                        metadict[countmeta] = tempdict
                    return metadict
                except:
                    return 'CompCase NoCom NoAdd Failed'
            else:
                try: 
                    metadict={}
                    countmeta = 0
                    for part in row['Lexed']:
                        countmeta +=1
                        addphase=fuzzaddextract(part)
                        cleaned=propextract(addphase[0])
                        if len(addphase[1]) > 0:
                            tempdict=builder(str(row[idstouse]),cleaned[0],cleaned[1],None,addphase[1])
                            metadict[countmeta] = tempdict
                        else:
                            tempdict=builder(str(row[idstouse]),cleaned[0],cleaned[1],None,None)
                            metadict[countmeta] = tempdict
                    return metadict
                except:
                    return 'CompCase NoCom Add Failed'
    
    elif row['SimpComp'] == False and row['ExtractedComs'] != 'NA':
        listoflist=[x for x in row['Lexed'] if type(x) is list]
        if len(listoflist) == 0:
            if fuzzaddchecker(row['Lexed']) == False :
                extractedprop=proptest(row['Lexed'])
                if type(extractedprop) is bool:
                    return 'Proportion Extraction Failed'
                else:
                    try:
                        if len(extractedprop[1]) > 0:
                            return builder(str(row[idstouse]),extractedprop[0],extractedprop[1],row['ExtractedComs'],None)
                        else:
                            return builder(str(row[idstouse]),extractedprop[0],None,row['ExtractedComs'],None)
                    except:
                        return 'Builder Failed'
            else:
                addsres = addextest(row['Lexed'])
                if type(addsres) is bool:
                    return 'Additives Extraction Failed'
                else:
                    extractedprop=proptest(addsres[0])
                    if type(extractedprop) is bool:
                        return 'Proportion Extraction Failed'
                    else:
                        try:
                            if len(extractedprop[1]) > 0:
                                return builder(str(row[idstouse]),extractedprop[0],extractedprop[1],row['ExtractedComs'],addsres[1])
                            else:
                                return builder(str(row[idstouse]),extractedprop[0],None,row['ExtractedComs'],addsres[1])
                        except:
                            return 'Builder Failed'
        else:
            if complexfuzzaddchecker(row['Lexed']) == False:
                try: 
                    metadict={}
                    countmeta = 0
                    for part in row['Lexed']:
                        countmeta +=1
                        cleaned=propextract(part)
                        tempdict=builder(str(row[idstouse]),cleaned[0],cleaned[1],row['ExtractedComs'],None)
                        metadict[countmeta] = tempdict
                    return metadict
                except:
                    return 'CompCase NoCom NoAdd Failed'
            else:
                try: 
                    metadict={}
                    countmeta = 0
                    for part in row['Lexed']:
                        countmeta +=1
                        addphase=fuzzaddextract(part)
                        cleaned=propextract(addphase[0])
                        if len(addphase[1]) > 0:
                            tempdict=builder(str(row[idstouse]),cleaned[0],cleaned[1],row['ExtractedComs'],addphase[1])
                            metadict[countmeta] = tempdict
                        else:
                            tempdict=builder(str(row[idstouse]),cleaned[0],cleaned[1],row['ExtractedComs'],None)
                            metadict[countmeta] = tempdict
                    return metadict
                except:
                    return 'CompCase NoCom Add Failed'
    else:
        return 'NA'