#! /usr/bin/env python3
# coding: utf-8
### Mintel Ingredient List Parser BETA 1.11.12 [beta number.beta month.beta day] - 2021
### coding: TriX [tristan.salord[at]inrae.fr]
### Original Work under Licence Creative Common CC-BY-NC https://creativecommons.org/licenses/by-nc/4.0/deed.en
### Work was registered at INRAE 04/10/2021

from collections import deque
from enum import Flag
from functools import reduce
from thefuzz import fuzz
from numpy import e
import pandas as pd
import re



##### -------------- 0. Static Informations -------------- #####

additivescatlist=['acidity regulator','acidifier','anti-caking agent','antifoaming agents','acidifying agent','antioxidant','bulking agent','carbonating agent','carrier','clarifying agent','cloudifier','colour retention agent','emulsifier','emulsifying salts','firming agent','flavour enhancer','flour treatment agent','foaming agent','food acid','food colour','gelling agent','glazing agent','humectant','modified starche','packaging gase','preservative','propellant','raising agent','sequestrant','stabilizer','sweetener','thickener']

extractedadds={'l(+)-tartaric acid':'E334','L+ tartaric acid':'E334', "sodium 5'-inosinate":'E631','L (+)-tartaric acid':'E334','L(+)-tartaric acid':'E334','L+-tartaric acid':'E334',
            "disodium 5'-ribonucleotide":'E635','monosodium glutamate':'E621',
            'sodium d-isoascorbate':'E316'}



##### ==============  A. Generic Function ============== #####

def getIndex(s, i):
    ''' Generic Function returning for a given opening parenthese the 
    index of the related closing parenthese. 
    All Credit: https://www.geeksforgeeks.org/find-index-closing-bracket-given-opening-bracket-expression/'''
    # 
    if s[i] != '(':
        return -1
    # Create a deque to use it as a stack.
    d = deque() 
    # Traverse through all elements
    # starting from i.
    for k in range(i, len(s)): 
        # Pop a starting bracket
        # for every closing bracket
        if s[k] == ')':
            d.popleft()
        # Push all starting brackets
        elif s[k] == '(':
            d.append(s[i])
        # If deque becomes empty
        if not d:
            return k
    return -1



def orphanremover(listofelements: list):
    '''Generic function that return a balanced bracketed list
    from an unbalanced one. Here Function track only bad closing bracket.
    It was designed for the addscategoryextract function'''
    newlist=listofelements
    opening=[]
    badpos=[]
    for rk,el in enumerate(newlist):
        if el == '(':
            opening.append(rk)
        elif el == ')':
            if len(opening) == 0:
                badpos.append(rk)
            else:
                opening.pop()

    for ix,rk in enumerate(badpos):
        newlist.pop(rk-ix)
    #return badpos
    return newlist


def researchlist(pattern,searchedlist):
    ''' Generic function allowing to apply on a given list a regular expression.'''
    r = re.compile(pattern)
    result = list(filter(r.search, searchedlist)) # Read Note
    return result[0] if len(result) >= 1 else 0 

def dictremover(dic,longchain):
    updated = longchain
    for key in dic:
        if key in updated:
            #print(key)
            updated = updated.replace(key, dic[key])
    return updated



##### ==============  B. Analytical Function ============== #####
# ~~~~~> general objective: determine grammar

def casechecker(string):
    ''' returns whether the product list examined is a compound product 
    (multiple sub-products) : False case  // or if it is a 'simple' product :
    True case.
    returns a boolean'''

    is_simple=False 
    if re.search('\n',string):
        full=[x.strip() for x in re.split('\n',string) if len(x)>0 and re.search('(^\°)|(^\^)|(^\#)|(^\*)|(^\d=)',x) is None]        
        is_simple = False if len(full) > 1 else True

    else:
        is_simple = True
    return is_simple

def fuzzysearch(term: str, lookedlist: list):
    '''Function returns if term examined is in list or if it's approaching based on
    fuzzy matching.
    All Credit : https://chairnerd.seatgeek.com/fuzzywuzzy-fuzzy-string-matching-in-python/'''
    term=term.lower().strip() 
    if term in lookedlist:
        return term
    else:
        vals=[(element,fuzz.ratio(element,term)) for element in additivescatlist if fuzz.ratio(element,term) > 90]
        if vals:
            maxval=max([x[1] for x in vals])
            return [x[0] for x in vals if x[1] == maxval][0]
        else:
            return 0

def fuzzaddchecker(lexedinglist):
    ''' Function check if in lexed ingredient list element are additives categories
    returns a boolean'''    
    
    presence = False
    for rk,exp in enumerate(lexedinglist):
        cond1=rk+1<len(lexedinglist) and lexedinglist[rk+1] in ['(',')']
        if re.search(':',exp):
            splitexp=exp.split(':')
            if fuzzysearch(splitexp[0],additivescatlist) != 0:
                presence = True
                break
        elif cond1:
            search=fuzzysearch(exp,additivescatlist)
            if search != 0:
                presence=True
                break
    return presence

def complexfuzzaddchecker(lexedinglist):
    ''' Useful variant of fuzzaddchecker. Used for complexe ingredient list.
    returns a boolean'''
    presence= False
    for part in lexedinglist:
        if fuzzaddchecker(part) is True:
            presence = True
            break
    return presence

def commentchecker(string):
    ''' Function check if raw ingredient list contains comments, i.e marked extra-
    informations.
    returns a boolean'''
    
    isTrue = False
    if re.search('(\°)|(\^)|(\#)|(\*)|(\d=)',string):
        # stripping parts is necessary: we can find space just after line break. Stripping avoid mistakens.
        full=[x.strip() for x in re.split('\n',string) if len(x)>0 and re.search('(^\°)|(^\^)|(^\#)|(^\*)|(^\d=)',x)]
        isTrue = True if len(full) >=1 else False
    return isTrue


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

##### ==============  C. Normalising Function ============== #####
# ~~~~~> general objective: normalised grammar variations


def simpleformater(rawing):
        '''First normalisation of raw ingredient lists based on a simple set of regular expression. '''
        
        formatedchain = rawing
        rules=(('\[','('),('\{','('),('\]',')'),('\}',')'),(';',','))

        for rule in rules:
            formatedchain = re.sub(rule[0],rule[1],formatedchain)         
        
        for k in extractedadds:
            if k in formatedchain:
                formatedchain = formatedchain.replace(k,extractedadds[k])

        cleaned = dictremover(extractedadds,formatedchain)
        return cleaned


def commentextract(rawinglist):

    ''' Function extracts comments from raw ingredient list.
    Comment markings are normalised (*). 
    Function returns two lists:
    + a cleaned ingredient list from comments,
    + list of the extracted comments.'''
    
    ### nested function called to normalised comments markings by
    # alternate signs
     
    def alternatereplacement(referencepoint: int, lookedchain: str, commentlist: list) -> str:
        alternatemarks=['°','#','\d=']
        #comlist = commentlist
        cleanedchain = lookedchain
        if referencepoint == 0:
            referencepoint += 1
        for sign in alternatemarks:
            for comment in commentlist:
                if re.search(sign, comment):
                    referencepoint += 1
                    prefix='*'*referencepoint+' '
                    commentlist.append((prefix+re.sub(sign,'',comment)).strip())
                    commentlist.pop(commentlist.index(comment))
                    cleanedchain=cleanedchain.replace(sign,(' '+prefix))
                
        return cleanedchain

    comments=[]
    uncomment=[]
    
    ### A comment is a sentence starting at a new line (\n) and prefixed
    # by a given sign observed as suffix in formula list.

    parts=re.split('\n',rawinglist)
    parts=[x.strip() for x in parts if len(x)>0]
    
    ### store comments in a dedicated list that will be returned
    for splitel in parts:
        if re.search('^\s{0,1}\*|^\s{0,1}°|^\s{0,1}#|^\s{0,1}\d', splitel):
            comments.append(splitel.strip())
        else:
            uncomment.append(splitel)
    ### get a reference point(max number of stars taken as default comment sign)
    #  if we have to deal with alternative marks 
    starscount=0
    for com in comments:
        if com.count('*') >= starscount:
            starscount == com.count('*')
    
    
    ### dealing with alternate signs in simple case config, there is no meta-compound:
    if len(uncomment) == 1:
        chain=uncomment[0]
        r=alternatereplacement(starscount,chain,comments)
        return [r,comments]
        ### dealing with alternate signs in complex case config:
    else:
        treated=[]
        for part in uncomment:
            treated.append(alternatereplacement(starscount,part,comments))
        result='\n'.join(treated)
        return [result,comments]


def propextract(lexedinglist: list) -> list:
    ''' Function to extract proportions from ingredient list. 
    Function returns a list containing:
    + lexed ingredient list cleaned from any proportion
    + extracted proportions
    Proportion are marked by a $.'''
    
    complexprop=re.compile('(\d{1,2}(\.\d{1,2}){0,1})(kg|g|mg|µg-RE)(\/(100g|100g formula|100g prepared product|per\s{0,1}100g|100ml|per\s{0,1}100ml|10g|kg|k|L|bar|carton|pack|unit|portion|served part|per\s{0,1}serving|serving)){0,1}')
    ppm=re.compile('(>|<){0,1}\d{1,4}(\.\d{1,4}|-\d{1,4}){0,1}\s{0,1}ppm')
    propsign='$'
    ''' Première situation: cas des pourcentages'''

    firstpass=[]
    secondpass=[]
    prop=[]
    count=1
    for ix,el in enumerate(lexedinglist):
        '''cherche si pourcentage présent'''
        if re.search('(\d{1,3}%)|\d{1,3}\.\d{1,3}%',el):
            match=re.search('(\d{1,3}%)|\d{1,3}\.\d{1,3}%',el).group()
            if ix == 0 and not el.startswith(match):
                newel=el.replace(match,propsign*count)
                prop.append(match)
                firstpass.append(newel)
                count+=1
            elif ix-1 >= 0 and lexedinglist[ix - 1] != '(':
                newel=el.replace(match,propsign*count)
                prop.append(match)
                firstpass.append(newel)
                count +=1
            elif ix-1 >= 0 and lexedinglist[ix - 1] == '(':
                firstpass[-2] =firstpass[-2]+propsign*count
                prop.append(match)
                count += 1
            else:
                firstpass.append(el)
        else:
            firstpass.append(el)
    
    firstpass=[x for x in firstpass if len(x) >=1]

    for _,val in enumerate(firstpass):
        if re.search(complexprop,val) is None and re.search(ppm,el) is None:
            secondpass.append(val)
        elif re.search(complexprop,val): 
            secondpass[-2] = secondpass[-2]+propsign*count
            prop.append(val)
            count +=1
        elif re.search(ppm,el):
            secondpass[-2] = secondpass[-2]+propsign*count
            prop.append(val)
            count +=1
        else:
            secondpass.append(val)

    for i,item in enumerate(secondpass):
        if item == '(' and secondpass[i+1] == ')':
            secondpass.pop(i)
            secondpass.pop(i)
    return [secondpass,prop]



def fuzzaddextract(lexedinglist: list) -> list:

    temp = []
    extractedAdds = []
    addcount = 0
    stack = []

    # étape 1: cas des additifs définis par ':'
    for _,term in enumerate(lexedinglist):
        if re.search(':',term):
            addcount+=1
            splitted=term.split(':')

            #### le terme est correctement orthographié et dans le dictionnaire 
            cond1=splitted[0].lower().strip() in additivescatlist
            if cond1 :
                temp.append(splitted[1].strip()+'@'*addcount)
                extractedAdds.append('@'*addcount+splitted[0])
            else:
                fuzzydic={}
                for key in additivescatlist:
                    fuzzydic[key]=fuzz.ratio(key,splitted[0].lower().strip())
                maxval=max(fuzzydic.values())
                if maxval > 90:
                    corrkey=list(fuzzydic.keys())[list(fuzzydic.values()).index(maxval)]
                    #print(f'Initial expression {splitted[0]} can be a mispelled of {corrkey}')
                    temp.append(splitted[1].strip()+'@'*addcount)
                    extractedAdds.append('@'*addcount+splitted[0])
                else:
                    temp.append(term.strip())
        else:
            temp.append(term.strip())

    # étape 2: cas des additifs définis par '()'
    enum_ing = enumerate(temp)    
    for rk, exp in enum_ing:
        ### conditions
        search=fuzzysearch(exp,additivescatlist)
        cond1=rk+1<len(temp) and temp[rk+1] =='('
        cond2=rk+1<len(temp) and temp[rk-1] =='(' and temp[rk+1] ==')'

        ### process
        stack.append(exp)
        if search != 0 and cond1:
            elbetweenbrackets=temp[rk+2:getIndex(temp,rk+1)]
            seq=len(temp[rk:getIndex(temp,rk+1)])
            stack.remove(exp)
            if researchlist(exp,extractedAdds) != 0:
                ### additif déjà identifié
                # print('Additives already identified')
                prefix=re.sub('[a-zA-Z]*','',researchlist(exp,extractedAdds))
                elbetweenbrackets = [x+prefix for x in elbetweenbrackets]
            else:
                ### additif non identifié
                # print('Additives unidentified')
                addcount+=1
                extractedAdds.append('@'*addcount+exp)
                elbetweenbrackets = [x+'@'*addcount for x in elbetweenbrackets]
            for x in elbetweenbrackets:
                stack.append(x)       
            for _, _ in zip(range(seq), enum_ing):
                pass
        elif search != 0 and cond2:
            stack=stack[:-2]
            if researchlist(exp,extractedAdds) != 0:
                prefix=re.sub('[a-zA-Z]*','',researchlist(exp,extractedAdds))
                stack[-1]=stack[-1]+prefix
            else:
                addcount+=1
                extractedAdds.append('@'*addcount+exp)
                stack[-1]=stack[-1]+'@'*addcount
            
    
    stack=orphanremover(stack)
        
    return stack,extractedAdds


##### ==============  D. Building Function ============== #####
# ~~~~~> general objective: building ingredients dictionary


def inglexer(processed) -> list:

    ''' Lexing Function. Function aims to split ingredient lits at commas and parenthesis.
    For that task it uses a basic "cutter" function applied distinctively if ingredient lists
    ar a whole or a list of ingredient list.
    Function return a list of splitted element.'''

    def cutter(string):
        unwanted=[None,'',',']
        res=re.split('(\(|,|\))',string)
        res=[x.lower().strip() for x in res if x not in unwanted and len(x) > 0]
        res=[x for x in res if x != '']

        return res
    
    def complexcutter(string):
        cleaned=[]
        if re.search('\n',string):
            splitted=string.split('\n')
            splitted=[x.strip() for x in splitted if re.search('^\s{0,1}\*',x) is None and len(x)>0]
            #si la grammaire de l'élement composé est de type 'macro-élément:formule'
            if re.search(':',splitted[0].split(',')[0]):
                parts=[]
                for macropart in splitted:
                    cutted=re.split('(,)',macropart)
                    for ing in cutted:
                        if cutted.index(ing) == 0 and re.search(':',ing):
                            good=re.sub(':','(',ing)
                            parts.append(macropart.replace(ing,good))
                parts=[x+')' for x in parts]
                for x in parts:
                    cleaned.append(cutter(x))
            #si la grammaire de l'élement composé est différente de 'macro-élément:formule' 
            else:
                for el in splitted:
                    cleaned.append(cutter(el))
        return cleaned

    # this part serves to determine when use the simple or the complex cutter
    
    if casechecker(processed) == True:
        return cutter(processed)
    else:
       return complexcutter(processed)



def builder(idprod,processedlist,proplist=None,commentlist=None,addlist=None) -> dict:
    
    '''Function that build from lexed and clea,ned ingredient list the dictionary of the ingredient list.
    Returned object is of python type dictionnary but can be easily convert into json format.
    Ids/keys of the dictionaries are composed by the concatenation of the product id of the ingredient list
    and the number of the ingredient. When ingredient lists are composed ingredient lists, keys are the number
    of appearance of the meta ingredients.'''

    ingdict={}
    depth = 0
    ingnb = 0
    for _,el in enumerate(processedlist):
        if el == '(':
            depth += 1
        elif el == ')':
            depth -= 1
        else:
            ingnb += 1
            key=idprod+'_'+str(ingnb)
            ingdict[key] = {}
            if re.search('\$',el) and re.search('\*',el) is None:
                associatedprop=[]
                markcount=el.count('$')
                for i,prop in enumerate(proplist):
                    if i+1 == markcount:
                        associatedprop.append(prop)
                ingdict[key]['rawing'] =el.replace('$','')
                ingdict[key]['level'] = depth
                ingdict[key]['prop'] = associatedprop
            elif re.search('\*',el) and re.search('\$',el) is None:
                associatedcomments=[]
                asscom=re.search('\*.*',el).group().split(' ')
                asscom=[x.strip() for x in asscom]
                for x in asscom:
                    for com in commentlist:
                        if len(x) == com.count('*'):
                            associatedcomments.append(re.sub('\*','',com))
                ingdict[key]['rawing'] = re.sub('\*','',el)
                ingdict[key]['level'] = depth
                ingdict[key]['comment'] = associatedcomments
            elif re.search('\$',el) and re.search('\*',el):
                associatedprop=[]
                associatedcomments=[]
                markcount=el.count('$')
                for i,prop in enumerate(proplist):
                    if i+1 == markcount:
                        associatedprop.append(prop)
                newel = el.replace('$','')
                asscom=re.search('\*.*',newel).group().split(' ')
                asscom=[x.strip() for x in asscom]
                for x in asscom:
                    for com in commentlist:
                        if len(x) == com.count('*'):
                            associatedcomments.append(re.sub('\*','',com))

                ingdict[key]['rawing'] = re.sub('\*','',newel)
                ingdict[key]['level'] = depth
                ingdict[key]['prop'] = associatedprop
                ingdict[key]['comment'] = associatedcomments
            elif re.search('@',el):
                associatedadds=[]
                starcount=el.count('@')
                for adds in addlist:
                    if adds.count('@') == starcount:
                        associatedadds.append(re.sub('@','',adds))
                ingdict[key]['rawing'] = re.sub('@','',el)
                ingdict[key]['level'] = depth
                ingdict[key]['additives'] = associatedadds
            
            else:
                ingdict[key] = {}
                ingdict[key]['rawing'] = el
                ingdict[key]['level'] = depth
    if len(ingdict) > 0:
        return ingdict
    else:
        return 'Builder Failed'




##### ==============  E. Extra Function ============== #####
# ~~~~~> general objective: extra option, based stats,...



def charsnumbers(rawinglist):
    '''Simple Function returning the length of an ingredient list
    based on the simple count of alpha chars. Punkt and Digits are removed'''
    unwanted=['(',')','[',']','{','}',',','.',';',':','/','-','_','+','=','<','>','%','*','#','°','?','!','^',' ','\n']
    onlychars=[x for x in rawinglist if x not in unwanted and not (x >= '0' and x <= '9')]
    return len(onlychars)


def flatingdict(ingdict: dict) -> list:
    '''Function flattening the ingredients dictionaries'''
    if type(ingdict) is dict:
        flatinglist=[]
        flatdict=pd.json_normalize(ingdict,sep= ' ').to_dict(orient = 'records')
        for key,val in flatdict[0].items():
            if re.search('rawing',key):
                flatinglist.append(val)
        return flatinglist
    else:
        return 'NA'

