'''Python code to convert the PDF documentation for HCMST 2017 into a usable data schema'''
''' PDF documentation for HCMST 2017 has the file name HCMST_2017_fresh_Codeboodk_v1.1a.pdf'''
import camelot
import pdb
import matplotlib.pyplot as plt
import pandas as pd
from halo import Halo
#use stream setting in camelot, since pages don't have a defined table structure
#use matplotlib to map textedge, and figure out scanning dimensions

def clean_emptystrings(df):
    '''function to remove whitespace caused by text spillover from column 1, from all other columns'''
    cols = []
    new_cols = []
    ind = []
    df.columns = [x for x in range(5)]
    # print(df.shape[0])
    for i in range(df.shape[1]):
        cols.append(list(df.iloc[:,i]))
    # pdb.set_trace()    
    for i in range(df.shape[0]):
        #spillover happens when first column has text, but last column have ''
        #keep the indices where this happens, update cols[0][i+1]
        if (cols[0][i] != '') and (cols[4][i] == ''):
            cols[0][i+1] = ''.join([cols[x][i] for x in range(0,df.shape[1])])
            ind.append(i)
    #create new columns as lists, use ind to figure out which row values to NOT include
    for i in range(df.shape[1]):
        plc = [cols[i][j] for j in range(df.shape[0]) if j not in ind]
        new_cols.append(plc)
        plc = []
    new_data = pd.DataFrame({x+1:new_cols[x] for x in range(0,df.shape[1])})
    return new_data

def fix_variable_column(df):
    '''function to remove extranoeus whitespace by concatenating wrapped text in column 5'''
    new_5 = []
    counter = 0
    #if row variable column has wrapped text, concatenate it with previous row
    #start from the bottom, make sure range includes 0
    for i in range(df.shape[0]-1,-1,-1):
            if df[2].iloc[i] == '':
                counter += 1
            else:
                plc = ''.join([(f'{df[5].iloc[i+j]} ') for j in range(counter+1)])
                # print(plc)
                new_5.append(plc)
                counter = 0
    new_5 = new_5[len(new_5)::-1]
    #remove all extraneous whitespaces from df using column 2
    df = df[df[2]!='']
    #set new_5 list as df[5]
    df[5] = new_5
    return df

raw_data = pd.DataFrame()
tables = camelot.read_pdf('HCMST_2017_fresh_Codeboodk_v1.1a.pdf', pages='1-11', table_areas=['63,720,550,60'], columns=['70,155,200,250,305']
    , flavor='stream', split_text=True)
for table in tables:
    raw_data= pd.concat([raw_data, table.df], ignore_index=True)

#data is demarcated using dashes, use df.str.contains() to figure out indices of demarcating dashes
demarc_dashes = raw_data.index[raw_data[1].str.contains('---')].tolist()
raw_data = raw_data.iloc[demarc_dashes[0]+1:demarc_dashes[1]].reset_index(drop=True)
#drop extraneous empty column 0
raw_data = raw_data.drop(columns=[0])
# print(raw_data.iloc[:,0])
new_data = clean_emptystrings(raw_data)
cleaned_schema = fix_variable_column(new_data)
#rename all columns to appropriately named parameters
cleaned_schema.columns = ['variable_name', 'storage_type','display_format', 'value_label', 'variable_label']
#export to csv
cleaned_schema.to_csv('cleaned_HCMST_2017_schema.csv',index=False)
