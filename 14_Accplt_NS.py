
import os
import subprocess
import Python_Module.io_module as io
from scipy.stats import norm

import numpy as np
import matplotlib.pyplot as plt


def Run_kt3d(name, col, gamma_name):
    par_path = f'10-Validation/Accplt/kt3d_xval_{name}.par'
    pf = open(par_path, 'w')
    pf.write(f'''                  Parameters for KT3D
                  *******************

START OF PARAMETERS:
5-Ppmt/ppmt.out              -file with data
1  2  3  4  {col}  0                 -   columns for DH,X,Y,Z,var,sec var
-98.00   1.0e21                 -   trimming limits
1                                -option: 0=grid, 1=cross, 2=jackknife
xvk.dat                          -file with jackknife data
1   2   0    3    0              -   columns for X,Y,Z,vr and sec var
3                                -debugging level: 0,1,2,3
10-Validation/Accplt/kt3d_xval_{name}.dbg                         -file for debugging output
10-Validation/Accplt/kt3d_xval_{name}.out                         -file for kriged output
50   0.5    1.0                  - nx,xmn,xsiz
50   0.5    1.0                  - ny,ymn,ysiz
1    0.5    1.0                  - nz,zmn,zsiz
1    1      1                    - x,y and z block discretization
1    32                           - min, max data for kriging
4                                - max per octant (0-> not used)
2000.0  2000.0  20.0             - maximum search radii
 0.0   0.0   0.0                 - angles for search ellipsoid
0     0.00                      - 0=SK,1=OK,2=non-st SK,3=exdrift
0 0 0 0 0 0 0 0 0                - drift: x,y,z,xx,yy,zz,xy,xz,zy
0                                - 0, variable; 1, estimate trend
extdrift.dat                     - gridded file with drift/mean
4                                -  column number in gridded file \n''')
    vmodel_file = f'4-Variograms/Ns_Model/{gamma_name}.par'
    var_string = io.get_var_string(vmodel_file)
    pf.write(var_string)
    pf.close()
    exe_path = os.path.join('Gslib','kt3d')
    subprocess.call([exe_path, par_path], shell=True)



def Plot_accplt(X, Y, name):



    plt.figure(figsize=(6, 6))
    plt.scatter(x = X, y=Y, c='black', s=50, rasterized=True)

    x = [0, 1]
    y = [0, 1]

    plt.plot(x , y, 'r-')
    plt.title(name, fontsize=15)
    plt.xlabel('Probability interval', labelpad=+10, fontsize=15)
    plt.ylabel('Fraction of true values', labelpad=+10, fontsize=15)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.axis('equal')
    plt.ylim(0.00, 1.00)
    plt.xlim(0.00, 1.00)
    plt.grid(axis='both', linestyle='--')
    fig_name = f'10-Validation/Accplt/Figs/{name}_gamma_ns_orig.png'
    plt.savefig(fig_name, dpi=400, bbox_inches='tight', pad_inches=0.1,
                frameon=None)

    plt.close()
    return None





if __name__ == '__main__':
    names = ['PPMT_RCG', 'PPMT_A1', 'PPMT_A2', 'PPMT_A3', 'PPMT_A4', 'PPMT_PPGc', 'PPMT_FR_AAG', 'PPMT_FR_SRG']
    cols = np.arange(21, 29)

    names_ppmt = ['PPMT_{}'.format(i) for i in np.arange(1,9)]

    gamma_names = ['NS_RCG', 'NS_ATGc', 'NS_STGc', 'NS_FEGc', 'NS_TIGc', 'NS_PPGc',
                   'NS_AAG', 'NS_SRG']


    n_var = len(names)

    prob_intervals = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90]
    n_intervals = len(prob_intervals)

    for i in range(n_var):
        name, col, gamma_name = names[i], cols[i], gamma_names[i]

        Run_kt3d(name=name, col=col, gamma_name=gamma_name)

        df = io.Get_Df_From_File(file_name=f'10-Validation/Accplt/kt3d_xval_{name}.out')
        True_array = df['True'].values
        Estimate_array = df['Estimate'].values
        Variance_array = df['EstimationVariance'].values
        Std_dev_array = np.sqrt(Variance_array)
        n_data = df.shape[0]

        true_fraction = np.zeros(n_intervals)

        for k in range(n_intervals):
            prob_interval = prob_intervals[k]
            min_prob = np.full(shape=n_data,fill_value= (1.00-prob_interval)/2.00)

            max_prob =  1- min_prob


            min_val = norm.ppf(q=min_prob, loc=Estimate_array, scale=Std_dev_array)
            max_val = norm.ppf(q=max_prob, loc=Estimate_array, scale=Std_dev_array)

            ind_acc = np.where( (True_array >=min_val) & (True_array <= max_val), 1.00, 0.00 )


            true_fraction[k] = np.mean(ind_acc)



        Plot_accplt(X=prob_intervals, Y=true_fraction, name=names_ppmt[i])








