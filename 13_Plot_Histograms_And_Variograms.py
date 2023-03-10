import numpy as np
import matplotlib.pyplot as plt
import os
import subprocess
from Python_Module.Get_Var_String import get_var_string
import Python_Module.io_module as io
import time
import pandas as pd
import multiprocessing


plt.rcParams['mathtext.fontset'] = 'cm'


def Read_histogram_ireal(name, i_real, sufix, n_quantiles):
    hist_file = f'10-Validation/Hist_orig_z_bot_cut/{name}_{i_real}_{sufix}_num.out'
    names = ['values', 'cdf']
    df_hist = pd.read_csv(hist_file, skiprows=4, nrows=n_quantiles, names = names,    delim_whitespace=True)
    print(df_hist.columns)
    return df_hist

def Read_histogram_data(name, i_real, sufix, n_quantiles, n_data):
    hist_file = f'10-Validation/Hist_orig_z_bot_cut/{name}_{i_real}_{sufix}_num.out'
    names = ['values', 'cdf']
    df_hist = pd.read_csv(hist_file, skiprows=4+n_quantiles+1, nrows=n_data, names = names,  delim_whitespace=True )
    return df_hist

def Plot_Histogram(name, n_real, sufix, n_quantiles, loc_legend):
    data_file = '1-Data/proc_data.txt'
    df_data = io.Get_Df_From_File(data_file)
    n_data = df_data.shape[0]

    print('test')
    name_var = name
    print('var = {}'.format(name_var))

    plt.figure(figsize=(5, 5))
    plt.xlabel(f'{name_var} (%)', fontsize=18)
    plt.ylabel('CDF', fontsize=18)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.ylim(0, 1)

    xmin = df_data[name_var].min()
    xmax = df_data[name_var].max()
    plt.xlim(xmin, xmax)

    std_dev_reals = np.zeros(n_real)
    means_reals = np.zeros(n_real)

    for k in range(n_real):
        i_real = k + 1
        df_histsim = Read_histogram_ireal(name=name_var, i_real=k + 1, n_quantiles=n_quantiles, sufix=sufix)
        df_sum = io.Get_Df_From_Histplt_File(file_name=f'10-Validation/Hist_orig_z_bot_cut/{name}_{i_real}_{sufix}_sum.out')
        means_reals[k] = df_sum.iloc[0, 3]
        std_dev_reals[k] = df_sum.iloc[0, 4]

        plt.plot(df_histsim['values'], df_histsim['cdf'], 'k', label='Realizations')

    ref_mean = df_sum.iloc[1, 3]
    ref_std_dev = df_sum.iloc[1, 4]

    df_data_hist = Read_histogram_data(name=name_var, n_data=n_data, i_real=1, sufix=sufix, n_quantiles=n_quantiles)
    print('Maximum cdf of data = {:.4f}'.format(df_data_hist['cdf'].values[-1]))
    print('Maximum value of data = {:.4f}'.format(df_data_hist['values'].values[-1]))
    plt.plot(df_data_hist['values'], df_data_hist['cdf'], 'r', label='Data')

    s0 = '$n_{real}$ ' + f'= {n_real} \n'
    s1 = '$m_{ref}$ ' + '= {:.2f}'.format(ref_mean) + '\n'
    s2 = '$\sigma_{ref}$ ' + '= {:.2f}'.format(ref_std_dev) + '\n'
    s3 = '$m_{real}$ ' + '= {:.2f}'.format(np.mean(means_reals)) + '\n'
    s4 = '$\sigma_{real}$ ' + '= {:.2f}'.format(np.mean(std_dev_reals))

    string = s0 + s1 + s2 + s3 + s4

    ax = plt.gca()

    plt.text(x=loc_legend[0], y=loc_legend[1], s=string, transform=ax.transAxes, fontsize=18)

    fig_name = f'10-Validation/Hist_orig_z_bot_cut/Figs/{name_var}_{sufix}.png'
    plt.savefig(fig_name, dpi=400, bbox_inches='tight', pad_inches=0.1,
                frameon=None)

    plt.close()



    return None


def Plot_Variogram(name, n_real, sufix):
    name_var = name
    print('var = {}'.format(name_var))

    df_data_vario = io.Get_Df_From_Variogram_File(f'4-Variograms/Orig_Exp/{name_var}.out')
    df_data_vario['Index'] = df_data_vario['Variogram Index']
    df_data_vario['Dist'] = df_data_vario['Lag Distance']
    df_data_vario['Gamma'] = df_data_vario['Variogram Value']

    ih_sim = 1
    iv_sim = 2

    ih_data = 9
    iv_data = 10

    iv_vmodel = 1
    ih_vmodel = 2

    # PREPARE THE HORIZONTAL PLOT
    plt.figure(figsize=(8, 6))
    plt.xlabel('Distance (m)', fontsize=15)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    print(i)
    plt.title(f'{name_var} horizontal', fontsize=15)
    plt.ylabel(r'$\gamma$', fontsize=80, rotation=0, labelpad=25)
    plt.ylim(0.0, 1.30)
    plt.xlim(0, 2000)
    # LOOP OVER THE SIMULATION VARIOGRAMS
    for k in range(n_real):
        i_real = k + 1
        print('    real = {}'.format(i_real))

        df_sim_vario = io.Get_Df_From_Variogram_File(f'10-Validation/Vario/{name_var}_{i_real}_{sufix}.out')
        df_sim_vario['Index'] = df_sim_vario['Variogram Index']
        df_sim_vario['Dist'] = df_sim_vario['Lag Distance']
        df_sim_vario['Gamma'] = df_sim_vario['Variogram Value']
        df_sim_vario_filter = df_sim_vario[df_sim_vario['Index'] == ih_sim]
        plt.plot(df_sim_vario_filter['Dist'].values, df_sim_vario_filter['Gamma'].values, 'grey')
    # ADD LEGEND
    plt.plot([0, 0], [-1, -1], 'k', label='Realizations')
    # ADD VARIOGRAM OF DATA
    df_data_vario_filter = df_data_vario[df_data_vario['Index'] == ih_data]
    plt.plot(df_data_vario_filter['Dist'].values, df_data_vario_filter['Gamma'].values, 'r', label='Data')
    plt.plot([0, 2000], [1, 1], 'k', linewidth=2)
    # plt.legend()
    fig_name = f'10-Validation/Vario/Figs/{name_var}_h_{sufix}.png'
    plt.savefig(fig_name, dpi=400, bbox_inches='tight', pad_inches=0.1,
                frameon=None)
    plt.close()

    # PREPARE THE VERTICAL PLOT
    plt.figure(figsize=(8, 6))
    plt.xlabel('Distance (m)', fontsize=15)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.title(f'{name_var} vertical', fontsize=15)
    plt.ylabel(r'$\gamma$', fontsize=80, rotation=0, labelpad=25)
    plt.ylim(0.0, 1.30)
    plt.xlim(0, 5.50)

    # LOOP OVER THE SIMULATION VARIOGRAMS
    for k in range(n_real):
        i_real = k + 1
        df_sim_vario = io.Get_Df_From_Variogram_File(f'10-Validation/Vario/{name_var}_{i_real}_{sufix}.out')
        df_sim_vario['Index'] = df_sim_vario['Variogram Index']
        df_sim_vario['Dist'] = df_sim_vario['Lag Distance']
        df_sim_vario['Gamma'] = df_sim_vario['Variogram Value']
        df_sim_vario_filter = df_sim_vario[df_sim_vario['Index'] == iv_sim]

        plt.plot(df_sim_vario_filter['Dist'].values, df_sim_vario_filter['Gamma'].values, 'grey')
    # ADD LEGEND
    plt.plot([0, 0], [-1, -1], 'k', label='Realizations')
    # ADD VARIOGRAM OF DATA
    df_data_vario_filter = df_data_vario[(df_data_vario['Index'] == iv_data)&(df_data_vario['Gamma'] > -98.00)]
    print(df_data_vario_filter)
    plt.plot(df_data_vario_filter['Dist'].values, df_data_vario_filter['Gamma'].values, 'r', label='Data')
    plt.plot([0, 2000], [1, 1], 'k', linewidth=2)
    # plt.legend()
    fig_name = f'10-Validation/Vario/Figs/{name_var}_v_{sufix}.png'
    plt.savefig(fig_name, dpi=400, bbox_inches='tight', pad_inches=0.1,
                frameon=None)
    plt.close()

    return None


if __name__ == '__main__':


    start = time.time()
    start_global = time.time()
    dic_grid = io.get_grid_dict('6-Grid/grid_fine_inf.txt')
    grid_size = dic_grid['nx'] * dic_grid['ny'] * dic_grid['nz']
    n_real = 40



    ##############################################################
    # START CHECKING HISTOGRAM REPRODUCTION
    ###########################################################

    names_orig = ['RCG', 'ATGc', 'STGc', 'FEGc', 'TIGc', 'PPGc', 'AAG', 'SRG']

    n_var = len(names_orig)
    cols_data = io.get_columns_from_names(filename='1-Data/proc_data.txt', names=names_orig)
    cols_sim = np.arange(1, 9)
    n_nodes_f = 5531184
    n_quantiles = 200000
    n_data = 7609
    sufix = 'end'

    loc_legend_list = [
        [0.05, 0.60],
        [0.05, 0.60],
        [0.55, 0.10],
        [0.55, 0.10],
        [0.55, 0.10],
        [0.05, 0.60],
        [0.55, 0.10],
        [0.55, 0.10]

    ]



    for i in range(n_var):
        name = names_orig[i]
        col_data = cols_data[i]
        col_sim = cols_sim[i]
        loc_legend = loc_legend_list[i]
        print('Ploting histogram = {}'.format(name))
        Plot_Histogram(name=name, n_real=n_real, sufix=sufix, n_quantiles=n_quantiles, loc_legend=loc_legend)
#        print('Ploting Variogram = {}'.format(name))
#        Plot_Variogram(name=name, n_real=n_real, sufix=sufix)


    finish = time.time()
    print('total time = {} seconds'.format(finish - start))
