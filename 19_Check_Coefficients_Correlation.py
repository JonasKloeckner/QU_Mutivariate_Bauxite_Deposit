

import Python_Module.io_module as io
import numpy as np
import matplotlib.pyplot as plt
import time

if __name__ == '__main__':

    plt.rcParams['mathtext.fontset'] = 'cm'

    start = time.time()

    names_sim = ['RCG', 'ATGc', 'STGc', 'FEGc', 'TIGc', 'PPGc', 'AAG', 'SRG']

    n_var = len(names_sim)

    # get_statistics_from_data
    data_file = '1-Data/proc_data.txt'
    df_all_data = io.Get_Df_From_File(data_file)

    df_data = df_all_data[names_sim]
    data_array = df_data.values
    corr_data = np.corrcoef(data_array, rowvar=False)

    grid_size_filter = 5531184
    sim_file = '9-Simulation_Orig_Units/1_end_f.out'
    sim_array = io.get_ireal_pd(filename=sim_file, list_of_cols=np.arange(1, 9), grid_size=grid_size_filter, ireal=1)

    sim_corr = np.corrcoef(sim_array, rowvar=False)


    corr_sim_list = []
    corr_data_list = []

    for i in range(n_var):

        for j in range(i+1, n_var):
            corr_sim_list.append(sim_corr[i, j])
            corr_data_list.append(corr_data[i, j])



    plt.figure(figsize=(6, 6))

    plt.scatter(x=corr_sim_list, y=corr_data_list, c='k',edgecolors='k', alpha=0.80, s=50, rasterized=True, zorder=2)
    x_line = [-1.10, 1.10]
    y_line = x_line
    plt.plot(x_line, y_line, c='red', zorder=1)

    correlation = np.corrcoef(corr_sim_list, corr_data_list)[0][1]
    print(correlation)
    ax = plt.gca()
    plt.text(x=0.10, y=0.90, size=20, s= r'$\rho = {:.3f}$'.format(correlation),transform=ax.transAxes)


    plt.xlabel('Coef. of correlation (realization 1)', labelpad=+10, fontsize=15)
    plt.ylabel('Coef. of correlation (data)', labelpad=+10, fontsize=15)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.axis('equal')
    plt.ylim(-1.10, 1.10)
    plt.xlim(-1.10, 1.10)

    plt.grid(axis='both', linestyle='--')
    fig_name = '10-Validation/Correlation/check_corr.png'
    plt.savefig(fig_name, dpi=400, bbox_inches='tight', pad_inches=0.1,
                    frameon=None)
    plt.close()

    finish = time.time()

    print('time = {} seconds'.format(finish - start))


