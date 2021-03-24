import os

workdir = 'D://thesisdata/plankton/cds_daily/'
os.chdir(workdir)
os.getcwd()

for folder in os.listdir():
    for file in os.listdir(folder):
        os.replace(folder+'/'+file,'D://thesisdata/plankton/cds_daily_neu/'+file)
