import os
import subprocess
from Python_Module.io_module import get_columns_from_names, Get_Df_From_File
from Python_Module.io_module import get_array_gslib_pd
import numpy as np
import matplotlib.pyplot as plt
import math

def Ppmt_Forward(cols, col_weight):

    string_cols_list = [str(i) for i in cols]
    string_cols = ' '.join(string_cols_list)
    str_weight = str(col_weight)
    n_var = len(cols)


    par_path = '5-Ppmt/ppmt.par'
    pf = open(par_path, 'w')
    pf.write(f'''                         Parameters for PPMT
                         *******************
START OF PARAMETERS:
1-Data/proc_data.txt             -input data file
{n_var} {string_cols} {str_weight}              -  number of variables, variable cols, and wt col
-98.0 1.0e7             -  trimming limits
25 50 50             -min/max iterations and targeted Gauss perc. (see Note 1)
0                   -spatial decorrelation? (0=no,1=yes) (see Note 2)
0 0 0                -  x, y, z columns (0=none for z)
50 25                -  lag distance, lag tolerance
3-Nscore/nscore_weigtht.out           -output data file with normal score transformed variables
5-Ppmt/ppmt.out             -output data file with PPMT transformed variables
5-Ppmt/ppmt.trn             -output transformation table (binary)

Note 1: Optional stopping criteria, where the projection pursuit algorithm will terminate
after reaching the targetted Gaussian percentile. The input percentile range is 1 (very Gaussian)
to 99 (barely Gaussian); the percentiles are calculated using random Gaussian distributions.
The min/max iterations overrides the targetted Gaussian percentile.

Note 2: Option to apply min/max autocorrelation factors after the projection pursuit algorithm
to decorrelate the variables at the specified non-zero lag distance.
    ''')
    pf.close()
    exe_path = os.path.join('Gslib','ppmt')
    subprocess.call([exe_path, par_path], shell=True)
    #os.remove(par_path)



def weighted_avg_and_std(values, weights):
    """
    Return the weighted average and standard deviation.

    values, weights -- Numpy ndarrays with the same shape.
    """
    average = np.average(values, weights=weights)
    variance = np.average((values-average)**2, weights=weights)  # Fast and numerically precise
    return average, math.sqrt(variance)

def Plot_Histogram_decl(data, name, decl_weights, fig_name):
    plt.figure(figsize=(6, 6))

    weights = decl_weights / np.sum(decl_weights)

    n, bins, patches = plt.hist(data, 20, weights=weights, facecolor='green', alpha=0.75,
                                edgecolor='k', zorder=2
                                )

    mean, std_dev = weighted_avg_and_std(values=data, weights=decl_weights)

    # plt.title('Projection 2D', fontsize=15)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.xlabel(f'{name} (%)', fontsize=15)
    plt.ylabel('Frequency', fontsize=15)
    plt.grid(True, which='major', linestyle='--')
    ax = plt.gca()
    plt.text(x=0.10, y=0.85, s='Mean = {:.2f}\nStd. Dev = {:.2f}'.format(mean, std_dev), transform=ax.transAxes,
             fontsize=15)

    plt.savefig(fig_name, dpi=600, facecolor='w', edgecolor='w', format=None,
                transparent=False, bbox_inches='tight', pad_inches=0.1,
                frameon=None)

    plt.close()
    return None



if __name__ == '__main__':

    data_file = '1-Data/proc_data.txt'

    names = ['RCG', 'A1', 'A2', 'A3', 'A4', 'PPGc', 'FR_AAG', 'FR_SRG']

    cols = get_columns_from_names(filename=data_file, names=names)

    col_weigth = get_columns_from_names(filename=data_file, names=['DECLUS_W'])[0]

    # Run ppmt forward transformation
    Ppmt_Forward(cols = cols, col_weight=col_weigth)

    names_ppmt = ['PPMT_{}'.format(i) for i in names]
    old_names = ['PPMT:{}'.format(i) for i in names]

    dict_names = dict(zip(old_names, names_ppmt))

    cols_ppmt = np.arange(21, 29, 1)

    print(cols_ppmt)
    ppmt_file = '5-Ppmt/ppmt.out'
    df_ppmt = Get_Df_From_File(ppmt_file)

    df_ppmt.rename(columns = dict_names, inplace=True)
    print(df_ppmt.columns)
    # Check Histograms of ppmt variables
    for i in range(len(names_ppmt)):
        name = names_ppmt[i]
        Plot_Histogram_decl(data=df_ppmt[name], name=name, decl_weights=df_ppmt['DECLUS_W'], fig_name=f'2-EDA/Hist_Ppmt/{name}.png')


    # check correlation of ppmt transformed variables

    array_data = get_array_gslib_pd(filename=ppmt_file, list_of_cols=cols_ppmt)

    corr_data = np.corrcoef(x=array_data, rowvar=False)
    plt.figure(figsize=(6, 6))
    plt.matshow(A=corr_data, cmap='seismic', vmin=-1, vmax=1.0)
    plt.xticks(np.arange(corr_data.shape[0]), names_ppmt, fontsize=12)
    plt.yticks(np.arange(corr_data.shape[1]), names_ppmt, fontsize=12)
    cbar = plt.colorbar()
    cbar.set_label('Correlation', fontsize=12)

    fig_name = '2-EDA/Corrmat/corrmat_ppmt.png'
    plt.savefig(fig_name, dpi=300, bbox_inches='tight', pad_inches=0.1,
                frameon=None)

    plt.close()
    
