import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def plot(df,df2,lable,min_val,max_val):

    # set a grey background (use sns.set_theme() if seaborn version 0.11.0 or above)
    plt.style.use('seaborn-deep')

    sns.histplot(df, x="birth Length", color="red", label=lable, bins=30, binrange=(min_val, max_val))
    sns.histplot(df2, x="birth Length", color="black", label="Schnitzcells sample data", bins=30, binrange=(min_val, max_val))
    plt.suptitle('test title', fontsize=20)
    plt.legend(loc='upper right')
    plt.show()




if __name__=="__main__":

    #csv files
    mono_culture_file = "Mono Culture/post-processing/results/Oufti_LifeHistory_based_Analysis.csv"
    Schnitzcells_sample_data = "Schnitzcells sample images set/post-processing/results/Oufti_LifeHistory_based_Analysis.csv"
    SuperSegger_sample_data = "SuperSegger sample images set/post-processing/results/Oufti_LifeHistory_based_Analysis.csv"

    #read csv files
    df_mono=pd.read_csv(mono_culture_file)
    df_schnitzcells =pd.read_csv(Schnitzcells_sample_data)
    df_supersegger = pd.read_csv(Schnitzcells_sample_data)

    #draw plot
    print(df_mono["birth Length"].values.max())
    max_val = max(df_mono["birth Length"].values.max(),df_schnitzcells["birth Length"].values.max())
    min_val = max(df_mono["birth Length"].values.min(),df_schnitzcells["birth Length"].values.min())
    plot(df_mono , df_schnitzcells,"mono Culture" , min_val , max_val)
