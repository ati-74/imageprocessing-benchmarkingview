import csv
import pandas as pd
import numpy as np
import os



def ProcessData(input_file, interval_time):

    # Parsing CellProfiler output
    dataFrame = pd.read_csv(input_file)
    # remove Nan lables and zero MajorAxisLength
    dataFrame = dataFrame.loc[
        (dataFrame["TrackObjects_Label_50"].isnull())
    ].reset_index(drop=True)
    dataFrame = dataFrame.reset_index(drop=True)

    # process the tracking data
    num_incorrect_tracking = dataFrame.shape[0]
    print(num_incorrect_tracking)
    return num_incorrect_tracking


if __name__ == "__main__":

    datasets = ["E.coli_chamber","E.coli_mono_agarose","E.coli_mono_agarose_skipTimeSteps2","E.coli_mono_agarose_skipTimeSteps",
                "E.coli_mono_agarose_noisy","Pseudomonas_agarose","Pseudomonas_chamber",
                "SuperSegger sample images set","Xanthomonase_agarose","Xanthomonase_chamber"]
    modes = ['1. Raw Images','2. Ilastik Output']

    interval_time =[1.5, 1.5 , 30 ,15, 1.5, 1.5, 1.5, 1, 1.5, 1.5]

    final_datasets = []
    final_modes = []
    incorrect_tracking = []

    for i , dataset in enumerate(datasets):
        for mode in modes:
            input_file = "../../../"+dataset+"/"+mode+"/CP outputs/MyExpt_IdentifySecondaryObjects.csv"
            interval_time_value = interval_time[i]
            print("dataset:" + dataset)
            print(mode)
            #print("interval time: "+str(interval_time_value))
            
            if mode == '1. Raw Images':
                if dataset != 'E.coli_mono_agarose_skipTimeSteps' and dataset !="E.coli_mono_agarose_skipTimeSteps2":
                        num_incorrect_tracking = ProcessData(input_file, interval_time_value)
                        final_datasets.append(dataset)
                        final_modes.append(mode)
                        incorrect_tracking.append(num_incorrect_tracking)
            else:
                if dataset != "E.coli_chamber" and dataset != "E.coli_mono_agarose_noisy":
                    num_incorrect_tracking = ProcessData(input_file, interval_time_value)
                    final_datasets.append(dataset)
                    final_modes.append(mode)
                    incorrect_tracking.append(num_incorrect_tracking)
                    
                    
    # write to csv
    #create new df 
    df = pd.DataFrame({'dataset':final_datasets , 'mode':final_modes , 'Number_of_incorrect_tracking': incorrect_tracking})
    df.to_csv('Number_of_incorrect_tracking.csv', index=False)








