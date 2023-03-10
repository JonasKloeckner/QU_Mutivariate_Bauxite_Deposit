

import Python_Module.io_module as io
import matplotlib.pyplot as plt
import numpy as np


def Plot_Histogram_SUM(data, name, fig_name):
    plt.figure(figsize=(6, 6))
    weights = np.zeros_like(data) + 1.0 / len(data)
    n, bins, patches = plt.hist(data, 20, weights=weights, facecolor='green', alpha=0.75,
                                edgecolor='k', zorder=2
                                )
    mean = np.mean(data)
    std_dev = np.std(data)
    min_data = np.min(data)
    max_data = np.max(data)

    # plt.title('Projection 2D', fontsize=15)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.xlabel(f'{name} (%)', fontsize=15)
    plt.ylabel('Frequency', fontsize=15)
    plt.xlim(np.min(data), np.max(data))
    plt.grid(True, which='major', linestyle='--')
    plt.title('Realization 1', fontsize=15)
    ax = plt.gca()
    plt.text(x=0.60, y=0.80, s='Min = {:.2f}\nMean = {:.2f}\nStd. Dev = {:.2f}\nMax={:.2f}'.format(min_data,mean, std_dev, max_data), transform=ax.transAxes,
             fontsize=14)

    plt.savefig(fig_name, dpi=600, facecolor='w', edgecolor='w', format=None,
                transparent=False, bbox_inches='tight', pad_inches=0.1,
                frameon=None)

    plt.close()
    return None

if __name__ == '__main__':


    n_nodes_f = 5531184
    names = ['RCG', 'ATGc', 'STGc', 'FEGc', 'TIGc', 'PPGc', 'AAG', 'SRG']
    n_var = len(names)

    sim_file = '9-Simulation_Orig_Units/1_end_f.out'
    df_sim = io.Get_Df_From_Sim_File(file_name=sim_file, grid_size=n_nodes_f)
    df_sim.columns = names

    df_sim['SUM'] = df_sim['ATGc'] + df_sim['STGc'] + df_sim['FEGc'] + df_sim['TIGc'] + df_sim['PPGc'] 

    fig_name = '10-Validation/Sum/Histogram_sum.png'

    Plot_Histogram_SUM(data=df_sim['SUM'], name='ATGc + STGc + FEGc + TIGc + PPGc', fig_name=fig_name)