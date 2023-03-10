
import Python_Module.io_module as io

import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':

    n_nodes_f = 5531184
    names = ['RCG', 'ATGc', 'STGc', 'FEGc', 'TIGc', 'PPGc', 'AAG', 'SRG']
    n_var = len(names)

    data_file = '1-Data/proc_data.txt'
    df_data = io.Get_Df_From_File(file_name=data_file)
    df_data_f = df_data[names]

    sim_file = '9-Simulation_Orig_Units/1_end_f.out'
    df_sim = io.Get_Df_From_Sim_File(file_name=sim_file, grid_size=n_nodes_f)
    df_sim.columns = names

    X = np.arange(1, n_var+1)

    plt.figure(figsize=(8, 6))

    plt.xticks(X, names, fontsize=15)
    plt.yticks(fontsize=15)
    plt.xlabel('Variable', fontsize=15)
    plt.ylabel('Minimum and maximum (%)', fontsize=15)
    plt.title('Realization 1')

    plt.scatter(X, df_data_f.max(), c='b' ,marker='o' ,s=70)
    plt.scatter(X, df_data_f.min(), c='b' ,marker='o' ,s=70, label='Data')

    plt.plot(X, df_data_f.max(), 'k' )
    plt.plot(X, df_data_f.min(), 'k', label='Simulation')
    plt.legend(fontsize=12)

    fig_name = '10-Validation/Min_Max/check_min_max_real_1.png'

    plt.savefig(fig_name, dpi=300, bbox_inches='tight', pad_inches=0.1,
                frameon=None)
    plt.close()

