#! /usr/bin/env python3
# coding: utf-8
### Mintel Ingredient List Parser BETA 1.11.12 [beta number.beta month.beta day] - 2021
### coding: TriX [tristan.salord[at]inrae.fr]
### Original Work under Licence Creative Common CC-BY-NC https://creativecommons.org/licenses/by-nc/4.0/deed.en
### Work was registered at INRAE 04/10/2021




import argparse
import numpy as np
import os.path
import sys
from MILPArgsFunc import *






if __name__ == "__main__":

#### ARGS parser part for CLI manipulation

    fiparser = argparse.ArgumentParser(prog='FIP',
                                        description='FIP is a parsing Program for food ingredint list')

    # fiparser.add_argument('Object',
    #                        metavar='object',
    #                        type=str,
    #                        help='Can be the path to dataframe to process or raw ingredient list depending on optional arguments -d or -i')

    fiparser.add_argument('-d',
                        '--dataframe',
                        action='store',
                        help='Specify dataframe path. Must be absolute Path')

    fiparser.add_argument('-f',
                        '--formula',
                        action='store',
                        help='Specify raw ingredient list to be parsed')



    args = fiparser.parse_args()

    datparser = False
    stringp = False


    if args.dataframe is None and args.formula is None:
        print('\t'+'*** Error. Must feed me with a -d dataframe or a -f formula')
        sys.exit()
    else:
        if args.dataframe and args.formula is None:
            if not os.path.isfile(args.dataframe):
                print('\t'+'*** The path specified does not exist ***')
                sys.exit()
            else:
                fileis = os.path.basename(args.dataframe)
                if not fileis[-4:] in ['.csv','.xls','xlsx']:   
                    print('\t'+'*** Wrong Dataframe extension, must be .csv, .xls or .xlsx ***')
                else:
                    datparser = True
        else:
            if args.dataframe and args.formula:
                print('\t'+'*** Error: Only accept -d or -f not both ***')
                sys.exit()
            else:
                stringp = True

    if stringp is True:
        logger.info('Start Processing raw ingredient list')
        print(stringprocess(args.formula))
        logger.info('Finished Processing raw ingredient list')
    if datparser is True:
        logger.info('Start Processing Dataframe')
        dataexplorer(args.dataframe)
        logger.info('Start Parsing Ingredient Lists')
        dataprocess()

    

