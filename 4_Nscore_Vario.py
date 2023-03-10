
import os
import subprocess
from Python_Module.io_module import get_columns_from_names, Get_Df_From_File
import matplotlib.pyplot as plt
import numpy as np



def Nscore(columns):

    n_var = len(columns)
    string_list_cols = [str(i) for i in columns]
    str_cols = ' '.join(string_list_cols)

    par_path = os.path.join('unscore.par')
    pf = open(par_path, 'w')
    pf.write(f'''                  Parameters for UNSCORE
                  **********************

START OF PARAMETERS:
1-Data/proc_data.txt       -file with data
{n_var}  {str_cols}                -  number of variables and columns
0                         -  column for weight, 0 if none
0                         -  column for category, 0 if none
0                         -  number of records if known, 0 if unknown
-98.00   1.0e21          -  trimming limits
0                         -transform using a reference distribution, 1=yes
../histsmth/histsmth.out  -file with reference distribution.
1   2   0                 -  columns for variable, weight, and category
0                      -maximum number of quantiles, 0 for all
3-Nscore/nscore_vario.out               -file for output
3-Nscore/nscore_vario.trn               -file for output transformation table
''')
    pf.close()
    exe_path = os.path.join('Gslib', 'unscore')
    subprocess.call([exe_path, par_path], shell=True)
    os.remove(par_path)

def Nscore_out_file(columns, out_file, out_trn):

    n_var = len(columns)
    string_list_cols = [str(i) for i in columns]
    str_cols = ' '.join(string_list_cols)

    par_path = os.path.join('unscore.par')
    pf = open(par_path, 'w')
    pf.write(f'''                  Parameters for UNSCORE
                  **********************

START OF PARAMETERS:
1-Data/proc_data.txt       -file with data
{n_var}  {str_cols}                -  number of variables and columns
0                         -  column for weight, 0 if none
0                         -  column for category, 0 if none
0                         -  number of records if known, 0 if unknown
-98.00   1.0e21          -  trimming limits
0                         -transform using a reference distribution, 1=yes
../histsmth/histsmth.out  -file with reference distribution.
1   2   0                 -  columns for variable, weight, and category
0                      -maximum number of quantiles, 0 for all
{out_file}               -file for output
{out_trn }              -file for output transformation table
''')
    pf.close()
    exe_path = os.path.join('Gslib', 'unscore')
    subprocess.call([exe_path, par_path], shell=True)
    os.remove(par_path)


def Plot_Histogram(data, name, fig_name):
    plt.figure(figsize=(6, 6))
    weights = np.zeros_like(data) + 1.0 / len(data)
    n, bins, patches = plt.hist(data, 20, weights=weights, facecolor='green', alpha=0.75,
                                edgecolor='k', zorder=2
                                )
    mean = np.mean(data)
    std_dev = np.std(data)

    # plt.title('Projection 2D', fontsize=15)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.xlabel(f'{name}', fontsize=15)
    plt.ylabel('Frequency', fontsize=15)
    plt.xlim(np.min(data), np.max(data))
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

    # NSCORE THE TRANSFORMED DATA

    data_file = '1-Data/proc_data.txt'
    names = ['RCG', 'A1', 'A2', 'A3', 'A4', 'PPGc', 'FR_AAG', 'FR_SRG']
    n_var = len(names)
    cols = get_columns_from_names(filename=data_file, names=names)

    Nscore(columns=cols)

    names_ns = ['NS_{}'.format(i) for i in names]
    ns_file = '3-Nscore/nscore_vario.out'
    df = Get_Df_From_File(ns_file)
    print(df.columns)

    names_ns = [f'NS_{name}' for name in names]

    for i in range(n_var):
        name_ns = names_ns[i]
        fig_name = f'2-EDA/Hist_Nscore_Vario/{name_ns}.png'
        Plot_Histogram(data=df[name_ns], name=name_ns, fig_name=fig_name)


    # NSCORE THE ORIGINAL GRADES
    names = ['RCG', 'ATGc', 'STGc', 'FEGc', 'TIGc', 'PPGc', 'AAG', 'SRG']
    cols = get_columns_from_names(filename=data_file, names=names)
    ns_file = '3-Nscore/nscore_orig_vario.out'
    ns_trn_file = '3-Nscore/nscore_orig_vario.trn'
    Nscore_out_file(columns=cols, out_file=ns_file, out_trn=ns_trn_file)

