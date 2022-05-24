import math
import statistics
from collections import Counter
import numpy as np
import pandas as pd
import sys


def lineageBacteriaAfterThisTimeStep(dataFrame, Bacteria):
    dataFrameOfLineage = dataFrame.loc[
        (dataFrame["TrackObjects_Label_50"] == Bacteria["TrackObjects_Label_50"])
        & (dataFrame["ImageNumber"] >= Bacteria["ImageNumber"])
    ]
    return dataFrameOfLineage


def divisionOccurrence(dataFrameOfLineage, Bacteria, Bacid):
    Parent_time_step_of_cell=Bacteria["ImageNumber"]
    Parent_index_of_cell=Bacteria["ObjectNumber"]
    division_occ=False
    lifehistoryIndex=[]
    
    Bacteriaindex=Bacid
    lifehistoryIndex.append(Bacteriaindex)
    incorrectBacteriumIndex=0
    LastTimeStep=dataFrameOfLineage["ImageNumber"].iloc[-1]
    
    while (division_occ==False) and (LastTimeStep != Parent_time_step_of_cell):
        reletive_Bacteria_in_next_timestep=dataFrameOfLineage.loc[(dataFrameOfLineage["TrackObjects_ParentImageNumber_50"]==Parent_time_step_of_cell) & (dataFrameOfLineage["TrackObjects_ParentObjectNumber_50"]==Parent_index_of_cell)]

        Number_of_reletive_bacteria=reletive_Bacteria_in_next_timestep.shape[0]

        if  Number_of_reletive_bacteria==1 :
                       Parent_index_of_cell=reletive_Bacteria_in_next_timestep.iloc[0]["ObjectNumber"]
                       Parent_time_step_of_cell=reletive_Bacteria_in_next_timestep.iloc[0]["ImageNumber"]
                       Bacteriaindex=reletive_Bacteria_in_next_timestep.index.tolist()[0]
                       lifehistoryIndex.append(Bacteriaindex)
        elif Number_of_reletive_bacteria==2:
                   division_occ=True
                   last_timestep_before_division=Parent_time_step_of_cell
                   
        elif Number_of_reletive_bacteria==0: #interupt
                   last_timestep_before_division=Parent_time_step_of_cell
                   break
        else:
            Length=reletive_Bacteria_in_next_timestep["AreaShape_MajorAxisLength"].values
            minLength=min(reletive_Bacteria_in_next_timestep["AreaShape_MajorAxisLength"].values)
            incorrectBacterium=np.where(Length == minLength)
            incorrectBacteriumIndex=reletive_Bacteria_in_next_timestep.index.values[incorrectBacterium][0]
            division_occ=True
            last_timestep_before_division=Parent_time_step_of_cell
            #print("Warning: Three cells are produced from a single cell!")
            #print("Lable:" + str(dataFrameOfLineage["TrackObjects_Label_50"].iloc[0]))

    if division_occ==False and LastTimeStep == Parent_time_step_of_cell:
               last_timestep_before_division=dataFrameOfLineage["ImageNumber"].iloc[-1]

    division_status={"division_occ":division_occ,"last_timestep_before_division":last_timestep_before_division,"lifeHistoryIndex":lifehistoryIndex,"incorrectBacteriumIndex":incorrectBacteriumIndex}

    return division_status


def LifeHistory(dataFrameOfLineage, lifehistoryIndex):
    dfLifehistory = dataFrameOfLineage.loc[lifehistoryIndex]

    return dfLifehistory


def AverageGrowthRate(divisionLength, birthLength, t):
    elongation_rate = round((math.log(divisionLength) - math.log(birthLength)) / t, 3)
    return elongation_rate


def growthRate(dfLifehistory, interval_time):
    LifeHistoryLength = dfLifehistory.shape[0]
    # calculatation of new feature
    divisionLength = dfLifehistory.iloc[[-1]]["AreaShape_MajorAxisLength"].values[0]
    birthLength = dfLifehistory.iloc[[0]]["AreaShape_MajorAxisLength"].values[
        0
    ]  # length of bacteria when they are born
    # this condition checks the life history of bacteria
    # If the bacterium exists only one time step: NaN will be reported.
    if LifeHistoryLength > 1:
        t = LifeHistoryLength * interval_time
        elongation_rate = AverageGrowthRate(divisionLength, birthLength, t)
    else:
        elongation_rate = "NaN"  # shows: bacterium is present for only one timestep.

    return elongation_rate


def BacteriaAnalysis(dataFrame, interval_time):
    # same Bacteria features
    result_dict = {
        "CellId": [],
        "lable": [],
        "birthLength": [],
        "AverageLength": [],
        "AverageVelocity": [],
        "LifeHistory": [],
        "GrowthRate": [],
    }

    dataFrame["CellLifeId"]=""
    dataFrame["divideFlag"] = False
    dataFrame["growthRate"] = ""
    dataFrame["LifeHistory"] = ""
    dataFrame["birth_Length"] = ""
    dataFrame["lineage"] = ""
    dataFrame["AverageLength"] = ""
    dataFrame["drop"] = False

    id_of_bacteria = 1
    num_incorrect_tracking = 0
    for index, row in dataFrame.iterrows():
        if not dataFrame.iloc[index]["growthRate"]:

            dataFrameOfLineage = lineageBacteriaAfterThisTimeStep(dataFrame, row)

            division_status = divisionOccurrence(dataFrameOfLineage, row, index)

            if division_status["incorrectBacteriumIndex"] != 0:
                drop_index = division_status["incorrectBacteriumIndex"]
                num_incorrect_tracking +=1

            dfLifehistory = LifeHistory(
                dataFrameOfLineage, division_status["lifeHistoryIndex"]
            )
            elongation_rate = growthRate(
                dfLifehistory, interval_time
            )

            LifehistoryIndex = dfLifehistory.index.tolist()
            LifeHistoryLength = dfLifehistory.shape[0]
            divisionLength = dfLifehistory.iloc[[-1]][
                "AreaShape_MajorAxisLength"
            ].values[0]
            birthLength = dfLifehistory.iloc[[0]]["AreaShape_MajorAxisLength"].values[
                0
            ]  # length of bacteria when they are born

            if dataFrame.iloc[index]["drop"] == True:
                for idx in LifehistoryIndex:
                    dataFrame.at[idx, "drop"] = True
                    dataFrame.at[idx, "growthRate"] = elongation_rate
            else:
                result_dict["CellId"].append(id_of_bacteria)
                result_dict["lable"].append(
                    dfLifehistory.iloc[[0]]["TrackObjects_Label_50"].values[0]
                )
                result_dict["birthLength"].append(birthLength)
                result_dict["LifeHistory"].append(LifeHistoryLength)
                if LifeHistoryLength <=1:
                    result_dict["AverageLength"].append("NaN")              
                result_dict["GrowthRate"].append(elongation_rate)
                for idx in LifehistoryIndex:
                    dataFrame.at[idx, "CellLifeId"] = id_of_bacteria
                    dataFrame.at[idx, "growthRate"] = elongation_rate
                id_of_bacteria += 1

            if division_status["division_occ"]:
                lastTimeStepOfBacteria = LifehistoryIndex[-1]
                dataFrame.at[lastTimeStepOfBacteria, "divideFlag"] = True

                # duaghters
                divisionTime = division_status["last_timestep_before_division"] + 1
                dataFrameOfdaughters = dataFrameOfLineage.loc[
                    (dataFrameOfLineage["ImageNumber"] == divisionTime)
                ]
                daughterIndex = dataFrameOfdaughters.index.tolist()

                parent_id = id_of_bacteria

                for daughetridx in daughterIndex:
                    dataFrame.at[daughetridx, "lineage"] = parent_id
                    if dataFrame.iloc[index]["drop"] == True:
                        dataFrame.at[daughetridx, "drop"] = True

    # rename some columns
    results = pd.DataFrame.from_dict(result_dict, orient="index").transpose()
    return num_incorrect_tracking
