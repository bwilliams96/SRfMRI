import sys
import os
import pandas as pd
import numpy as np

subject = sys.argv[1]

#Define functions for creating timing files

def timing_epoch(subject,epoch,start,end,filename,conditional=None,value=None,shiftVal=None, initLearn =False):
    
    if initLearn == True:
        subdata = data.query("Learning_event_num == 1")
        subdata = subdata.reset_index(drop=True)
    else:
        subdata = data
    
    
    #Create output file 
    output = pd.DataFrame(subdata[epoch]/1000)
    output = output.rename({epoch: 'onset'}, axis = 1)
    
    if shiftVal is not None:
        output['duration'] = (subdata[end].shift(periods=shiftVal)/1000) - (subdata[start]/1000)
    else:
        output['duration'] = (subdata[end]/1000) - (subdata[start]/1000)
    
    if conditional is not None:
        conditions_tt = [
        (subdata[conditional] == value)
        ]
        trial_type = [1]
        output['strength'] = np.select(conditions_tt, trial_type)
        output = output[output['strength']==1]
    else:
        output['strength'] = 1                
        
    #Create output file
    output_filename = f"/storage/gold/cinn/2019/SRfMRI/BIDS/{subject}/func/{subject}_{filename}_events.tsv"
    
    with open(output_filename,'w') as write_tsv:
        write_tsv.write(output.to_csv(sep='\t',index=False,header=False)) 

def PPI_epoch(subject,epoch,start,end,filename):
    
    dataPPI = data.query("Learning_event_num > 1")
    dataPPI = dataPPI.reset_index(drop=True)
    dataPPI.loc[dataPPI['Task_phase'] == 1, 'Strength'] = 1
    dataPPI.loc[dataPPI['Task_phase'] == 2, 'Strength'] = -1
    
    #Create output file 
    output = pd.DataFrame(dataPPI[epoch]/1000)
    output = output.rename({epoch: 'onset'}, axis = 1)
    output['duration'] = (dataPPI[end]/1000) - (dataPPI[start]/1000)
    output['strength'] = dataPPI['Strength']              
        
    #Create output file
    output_filename = f"/storage/gold/cinn/2019/SRfMRI/BIDS/{subject}/func/{subject}_{filename}_events.tsv"
    
    with open(output_filename,'w') as write_tsv:
        write_tsv.write(output.to_csv(sep='\t',index=False,header=False))
        
    outputPlus = output
    outputPlus.loc[outputPlus['strength'] == -1, 'strength'] = 1
    
    output_Plus = f"/storage/gold/cinn/2019/SRfMRI/BIDS/{subject}/func/{subject}_{filename}-plus_events.tsv"
    
    with open(output_Plus,'w') as write_tsv_plus:
        write_tsv_plus.write(outputPlus.to_csv(sep='\t',index=False,header=False))

# Create timing files
# Load data
os.chdir(f"/storage/gold/cinn/2019/SRfMRI/Behavioural")
    
outdir = (f"/storage/gold/cinn/2019/SRfMRI/BIDS/{subject}/func")
outdir_check = os.path.isdir(outdir)
# If folder doesn't exist, then create it.
if not outdir_check:
    os.makedirs(outdir)

data = pd.read_csv(f"{subject}.txt", delimiter='\t', header=0)
    
timing_epoch(subject,'Fractal onset - block(ms)','Fractal onset - block(ms)','Highlight onset - block(ms)','DM')
timing_epoch(subject,'Highlight onset - block(ms)','Highlight onset - block(ms)','Outcome onset - block(ms)','Ant')
PPI_epoch(subject,'Outcome onset - block(ms)','Outcome onset - block(ms)','First fixation onset - block(ms)','Fb')
timing_epoch(subject,'Outcome onset - block(ms)','Outcome onset - block(ms)','First fixation onset - block(ms)','IL',initLearn=True)
timing_epoch(subject,'Cum total onset - block(ms)','Cum total onset - block(ms)','Second fixation onset - block(ms)','Tot')