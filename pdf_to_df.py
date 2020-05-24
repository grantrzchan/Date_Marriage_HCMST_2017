'''Python code to convert the PDF documentation for HCMST 2017 into a usable data schema'''
import camelot
import matplotlib.pyplot as plt
import pandas as pd
from halo import Halo
#use stream, since page doesn't have defined table structure
#use mtplotlib to map textedge
tables = camelot.read_pdf('HCMST_2017_fresh_Codeboodk_v1.1a.pdf', pages='1', table_areas=['63,620,550,60'], columns=['70,150,200,250,305']
    , flavor='stream', split_text=True)
#print(tables[0].df)
# camelot.plot(tables[0], kind='textedge')
# plt.show()