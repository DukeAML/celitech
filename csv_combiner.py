import os
import glob
import pandas as pd

def read_and_parse(f):
    #get rid of first row and concatenate
    df = pd.read_csv(f)
    return df

os.chdir("sample_data")

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
#combine all files in the list
sample_data = pd.concat([read_and_parse(f) for f in all_filenames ])
#export to csv
sample_data.to_csv( "sample_data.csv")

