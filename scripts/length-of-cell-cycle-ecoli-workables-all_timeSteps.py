import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob


def draw_dist():
    """
    Generate and save histograms comparing the distribution of the length of cell cycles across different datasets.

    This function creates histograms for several datasets to compare the distribution of cell cycle lengths.
    """

    # Determine the common bin edges for all subplots based on the data range
    bin_edges = np.linspace(min(min(ref_lifehistory), max(CP_Omnipose_lifehistory), min(DeLTA_lifehistory),
                                min(FAST_lifehistory), min(SuperSegger_lifehistory)),
                            max(max(ref_lifehistory), max(CP_Omnipose_lifehistory), max(DeLTA_lifehistory),
                                max(FAST_lifehistory), max(SuperSegger_lifehistory)) + 1, 9)

    print(bin_edges)

    # Create subplots layout
    fig, axs = plt.subplots(3, 2, figsize=(12, 8))

    # Plot histograms for each method
    axs[0, 0].hist(ref_lifehistory, bins=bin_edges, color='#DAA520', edgecolor='white', label='Ground truth')
    axs[0, 1].hist(CP_Omnipose_lifehistory, bins=bin_edges, color='red', edgecolor='white', label='CP-Omnipose')
    axs[1, 0].hist(SuperSegger_lifehistory, bins=bin_edges, color='black', edgecolor='white', label='SS-Omnipose')
    axs[1, 1].hist(DeLTA_lifehistory, bins=bin_edges, color='blue', edgecolor='white', label='DeLTA')
    axs[2, 0].hist(FAST_lifehistory, bins=bin_edges, color='#3cb44b', edgecolor='white', label='FAST')

    # Set common labels and titles for the subplots
    axs[0, 0].set_ylabel('Frequency', fontfamily='serif', fontsize=14, labelpad=10)
    axs[1, 0].set_ylabel('Frequency', fontfamily='serif', fontsize=14, labelpad=10)
    axs[2, 0].set_ylabel('Frequency', fontfamily='serif', fontsize=14, labelpad=10)

    axs[2, 0].set_xlabel('duration of cell cycle (minute)', fontfamily='serif', fontsize=14,
                         labelpad=10)  # Increase space between x label and x axis
    axs[2, 1].set_xlabel('duration of cell cycle (minute)', fontfamily='serif', fontsize=14, labelpad=10)

    # Determine the maximum and minimum y-axis limits from all subplots
    ymax_list = []
    ymin_list = []

    for ax in axs.flat:
        ymin, ymax = ax.get_ylim()
        ymax_list.append(ymax)
        ymin_list.append(ymin)

    max_ymax = int(max(ymax_list)) + 1
    min_ymin = int(min(ymin_list))

    # Standardize y-axis limits and x-tick labels across all subplots
    for ax in axs.flat:
        # Adjust the x-ticks and labels
        tick_positions = [(bin_edges[i] + bin_edges[i + 1]) / 2 for i in range(len(bin_edges) - 1)]
        ax.set_xticks(tick_positions)

        bin_labels = [f"{bin_edges[i] * 5:.0f}" for i in range(len(bin_edges) - 1)]
        # Slice tick_positions and bin_labels to show every alternate bin
        tick_positions = tick_positions[::2]
        bin_labels = bin_labels[::2]

        ax.set_xticks(tick_positions)
        ax.set_xticklabels(bin_labels, fontsize=12, fontfamily='serif')
        ax.set_xlim([min(tick_positions) - 0.6, max(tick_positions) + 1.6])

        # Get the current y-axis limits
        # Create a list of even y-ticks within the range
        ax.set_ylim([min_ymin, max_ymax])
        yticks = [i for i in range(min_ymin, max_ymax + 1) if i % 50 == 0]
        # Set the y-ticks to the even values
        ax.set_yticks(yticks, fontsize=12, fontfamily='serif')

    # Increase margin around the plot
    axs[0, 0].legend(prop={'size': 13, 'family': 'serif'})
    axs[0, 1].legend(prop={'size': 13, 'family': 'serif'})
    axs[1, 0].legend(prop={'size': 13, 'family': 'serif'})
    axs[1, 1].legend(prop={'size': 13, 'family': 'serif'})
    axs[2, 0].legend(prop={'size': 13, 'family': 'serif'})

    # Increase margin around the plot
    plt.tight_layout(pad=2.0)

    # Show the plot
    # plt.show()
    plt.savefig('distribution of length of cell cycle - ecoli babies.pdf')


if __name__ == '__main__':
    babies_folder = 'G:/ecoli babies/done'
    tools = ['reference-mask', 'CP_Omnipose', 'DeLTA', 'FAST', 'SuperSegger']

    ref_lifehistory = []
    CP_Omnipose_lifehistory = []
    DeLTA_lifehistory = []
    FAST_lifehistory = []
    SuperSegger_lifehistory = []

    for tool in tools:
        for folder in glob.glob(babies_folder + '/*'):
            if tool == 'reference-mask':
                bacteria_properties_path = folder + '/' + tool + '/post-processing/ref_mask_bacteria_feature_analysis.csv'
                bacteria_properties_df = pd.read_csv(bacteria_properties_path)

                time_steps_list = list(set(bacteria_properties_df['TimeStep'].values.tolist()))
                filter_conditions = bacteria_properties_df['TimeStep'].isin([time_steps_list[-1], 1])
                bacteria_properties_df = bacteria_properties_df.loc[filter_conditions]

                bacteria_ids = list(set(bacteria_properties_df['CellLifeId'].values.tolist()))

                bacteria_life_history_path = folder + '/' + tool + '/post-processing/ref_mask_LifeHistory_based_Analysis.csv'
                bacteria_life_history_df = pd.read_csv(bacteria_life_history_path)

                bacteria_life_history_df = bacteria_life_history_df.loc[
                    ~bacteria_life_history_df['CellId'].isin(bacteria_ids)]

                if 1 in bacteria_life_history_df['LifeHistory'].values.tolist():
                    print(folder)
                ref_lifehistory.extend(bacteria_life_history_df['LifeHistory'].values.tolist())

            elif tool == 'CP_Omnipose':
                bacteria_properties_path = folder + '/' + tool + '/processing/CP_Omnipose_bacteria_feature_analysis.csv'
                bacteria_properties_df = pd.read_csv(bacteria_properties_path)

                time_steps_list = list(set(bacteria_properties_df['TimeStep'].values.tolist()))
                filter_conditions = bacteria_properties_df['TimeStep'].isin([time_steps_list[-1], 1])
                bacteria_properties_df = bacteria_properties_df.loc[filter_conditions]

                bacteria_ids = list(set(bacteria_properties_df['CellLifeId'].values.tolist()))

                bacteria_life_history_path = folder + '/' + tool + '/processing/CP_Omnipose_LifeHistory_based_Analysis.csv'
                bacteria_life_history_df = pd.read_csv(bacteria_life_history_path)

                bacteria_life_history_df = bacteria_life_history_df.loc[
                    ~bacteria_life_history_df['CellId'].isin(bacteria_ids)]

                CP_Omnipose_lifehistory.extend(bacteria_life_history_df['LifeHistory'].values.tolist())

            elif tool == 'DeLTA':
                bacteria_properties_path = folder + '/' + tool + '/results/DeLTA_bacteria_feature_analysis.csv'
                bacteria_properties_df = pd.read_csv(bacteria_properties_path)

                time_steps_list = list(set(bacteria_properties_df['TimeStep'].values.tolist()))

                filter_conditions = bacteria_properties_df['TimeStep'].isin([time_steps_list[-1], 1])
                bacteria_properties_df = bacteria_properties_df.loc[filter_conditions]

                bacteria_ids = list(set(bacteria_properties_df['CellId'].values.tolist()))

                bacteria_life_history_path = folder + '/' + tool + '/results/DeLTA_LifeHistory_based_Analysis.csv'
                bacteria_life_history_df = pd.read_csv(bacteria_life_history_path)

                bacteria_life_history_df = bacteria_life_history_df.loc[
                    ~bacteria_life_history_df['CellId'].isin(bacteria_ids)]

                DeLTA_lifehistory.extend(bacteria_life_history_df['LifeHistory'].values.tolist())
            elif tool == 'FAST':
                bacteria_properties_path = folder + '/' + tool + '/results/FAST_bacteria_feature_analysis.csv'
                bacteria_properties_df = pd.read_csv(bacteria_properties_path)

                time_steps_list = list(set(bacteria_properties_df['TimeStep'].values.tolist()))

                filter_conditions = bacteria_properties_df['TimeStep'].isin([time_steps_list[-1], 1])
                bacteria_properties_df = bacteria_properties_df.loc[filter_conditions]

                bacteria_ids = list(set(bacteria_properties_df['CellLifeId'].values.tolist()))

                bacteria_life_history_path = folder + '/' + tool + '/results/FAST_LifeHistory_based_Analysis.csv'
                bacteria_life_history_df = pd.read_csv(bacteria_life_history_path)

                bacteria_life_history_df = bacteria_life_history_df.loc[
                    ~bacteria_life_history_df['CellId'].isin(bacteria_ids)]

                FAST_lifehistory.extend(bacteria_life_history_df['LifeHistory'].values.tolist())
            elif tool == 'SuperSegger':
                bacteria_properties_path = folder + '/' + tool + '/results/SuperSegger_bacteria_feature_analysis.csv'
                bacteria_properties_df = pd.read_csv(bacteria_properties_path)

                time_steps_list = list(set(bacteria_properties_df['TimeStep'].values.tolist()))

                filter_conditions = bacteria_properties_df['TimeStep'].isin([time_steps_list[-1], 1])
                bacteria_properties_df = bacteria_properties_df.loc[filter_conditions]

                bacteria_ids = list(set(bacteria_properties_df['CellLifeId'].values.tolist()))

                bacteria_life_history_path = folder + '/' + tool + '/results/SuperSegger_LifeHistory_based_Analysis.csv'
                bacteria_life_history_df = pd.read_csv(bacteria_life_history_path)

                bacteria_life_history_df = bacteria_life_history_df.loc[
                    ~bacteria_life_history_df['CellId'].isin(bacteria_ids)]

                SuperSegger_lifehistory.extend(bacteria_life_history_df['LifeHistory'].values.tolist())

    # filtration (remove zeros and nan)
    ref_lifehistory = [v for v in ref_lifehistory if 5 <= v < 13]
    CP_Omnipose_lifehistory = [v for v in CP_Omnipose_lifehistory if 5 <= v < 13]
    DeLTA_lifehistory = [v for v in DeLTA_lifehistory if 5 <= v < 13]
    FAST_lifehistory = [v for v in FAST_lifehistory if 5 <= v < 13]
    SuperSegger_lifehistory = [v for v in SuperSegger_lifehistory if 5 <= v < 13]

    print(len(CP_Omnipose_lifehistory))
    print(len(DeLTA_lifehistory))
    print(len(FAST_lifehistory))
    print(len(SuperSegger_lifehistory))

    df = pd.DataFrame.from_dict({
        'ref_mask': ref_lifehistory,
        'CP_Omnipose': CP_Omnipose_lifehistory,
        'DeLTA': DeLTA_lifehistory,
        'FAST': FAST_lifehistory,
        'SuperSegger': SuperSegger_lifehistory
    }, orient='index').transpose()

    # Compute bins and histograms for each column
    bin_edges = np.linspace(df.min().min(), df.max().max() + 1, num=9)
    print(np.linspace(df.min().min(), df.max().max(), 8))

    hist_data = {
        'bin_start': bin_edges[:-1],  # Start of each bin
        'bin_end': bin_edges[1:]  # End of each bin
    }

    for col in df.columns:
        freq, _ = np.histogram(df[col].dropna(), bins=bin_edges)
        hist_data[col] = freq

    # Convert histogram data to dataframe
    hist_df = pd.DataFrame(hist_data)
    print(hist_df)

    print(df.mean())
    print(df.std())

    draw_dist()
