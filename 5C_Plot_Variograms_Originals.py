import os
import subprocess
from Python_Module.Get_Var_String import get_var_string
import matplotlib.pyplot as plt
import Python_Module.io_module as io
import numpy as np

plt.rcParams['mathtext.fontset'] = 'cm'


def Run_Varmodel(name):
    par_path = f'4-Variograms/Ns_Model/{name}_varmodel.par'


    string_gamma = get_var_string(vmodel_file_name=f'4-Variograms/Ns_Model/{name}.par')
    pf = open(par_path, 'w')
    pf.write(f'''                  Parameters for VARMODEL
                  ***********************
 
START OF PARAMETERS:
4-Variograms/Ns_Model/{name}_varmodel.var                 -file for modeled variogram points output
2                            -number of directions to model points along
0.0   -90.0  500   0.1      -  azm, dip, npoints, point separation 
0.0   0.0  1000   4.0      -  azm, dip, npoints, point separation
{string_gamma} 0   100000                   -fit model (0=no, 1=yes), maximum iterations
1.0                          -  variogram sill (can be fit, but not recommended in most cases)
1                            -  number of experimental files to use
test.out                  -    experimental output file 1
1   1   4                    -      # of variograms (<=0 for all), variogram #s
0   1   10                   -  # pairs weighting, inverse distance weighting, min pairs
0     10.0                   -  fix Hmax/Vert anis. (0=no, 1=yes)
0      1.0                   -  fix Hmin/Hmax anis. (0=no, 1=yes)
test.var              -  file to save fit variogram model
        	''')
    pf.close()
    exe_path = os.path.join('Gslib','varmodel')
    subprocess.call([exe_path, par_path], shell=True)
    return None







def Run_Varcalc_New_Format(name, col):
    par_path = os.path.join('4-Variograms', 'NS_Exp', f'{name}_new.par')
    pf = open(par_path, 'w')
    pf.write(f'''                  Parameters for VARCALC
                  **********************

START OF PARAMETERS:
3-Nscore/nscore_orig_vario.out         -  file with data
2   3   4                         -   columns for X, Y, Z coordinates
1   {col}   {col}                 -   number of variables,column numbers (position used for tail,head variables below)
-998.0    1.0e21                  -   trimming limits
10                                -number of directions
0.0 22.5 25.0   0.0 22.5 0.50 0.0  -Dir 01: azm,azmtol,bandhorz,dip,diptol,bandvert,tilt
30  50.0  25.0                -        number of lags,lag distance,lag tolerance
22.5 22.5 25.0  0.0 22.5 0.50 0.0  -Dir 02: azm,azmtol,bandhorz,dip,diptol,bandvert,tilt
30  50.0  25.0                 -        number of lags,lag distance,lag tolerance
45.0 22.5 25.0   0.0 22.5 0.50 0.0  -Dir 03: azm,azmtol,bandhorz,dip,diptol,bandvert,tilt
30  50.0  25.0                 -        number of lags,lag distance,lag tolerance
67.5 22.5 25.0   0.0 22.5 0.50 0.0   -Dir 04: azm,azmtol,bandhorz,dip,diptol,bandvert,tilt
30  50.0  25.0                -        number of lags,lag distance,lag tolerance
90.0 22.5 25.0   0.0 22.5 0.50 0.0   -Dir 05: azm,azmtol,bandhorz,dip,diptol,bandvert,tilt
30  50.0  25.0                 -        number of lags,lag distance,lag tolerance
112.5 22.5 25.0   0.0 22.5 0.50 0.0   -Dir 06: azm,azmtol,bandhorz,dip,diptol,bandvert,tilt
30  50.0  25.0                 -        number of lags,lag distance,lag tolerance
135.0 22.5 25.0   0.0 22.5 0.50 0.0   -Dir 07: azm,azmtol,bandhorz,dip,diptol,bandvert,tilt
30  50.0  25.0                -        number of lags,lag distance,lag tolerance
157.5 22.5 25.0   0.0 22.5 0.50 0.0   -Dir 08: azm,azmtol,bandhorz,dip,diptol,bandvert,tilt
30  50.0  25.0               -        number of lags,lag distance,lag tolerance
0.00 90.0 100000.0   0.0 22.5 0.50 0.0 -Dir 09: azm,azmtol,bandhorz,dip,diptol,bandvert,tilt
30  50.0  25.0
0.00 22.5 10.00 -90.00 22.5 10.00 0.00 -Dir 10: azm,azmtol,bandhorz,dip,diptol,bandvert,tilt
20  0.50  0.25                 -        number of lags,lag distance,lag tolerance
4-Variograms/NS_Exp/{name}_new.out                       -file for experimental variogram points output.
0                                 -legacy output (0=no, 1=write out gamv2004 format)
1                                 -run checks for common errors
0                                 -standardize sills? (0=no, 1=yes)
1                                 -number of variogram types
1   1   1                        -tail variable, head variable, variogram type (and cutoff/category), sill
''')
    pf.close()
    exe_path = os.path.join('Gslib' ,'varcalc')
    subprocess.call([exe_path, par_path], shell=True)
    os.remove(par_path)




def Plot_Directional_Variogram(name):
    df_data_vario = io.Get_Df_From_Variogram_File(f'4-Variograms/NS_Exp/{name}_new.out')
    df_data_vario['Index'] = df_data_vario['Variogram Index']
    df_data_vario['Dist'] = df_data_vario['Lag Distance']
    df_data_vario['Gamma'] = df_data_vario['Variogram Value']



    df_model_vario = io.Get_Df_From_Varmodel_File(f'4-Variograms/Ns_Model/{name}_varmodel.var')
    df_model_vario['Index'] = df_model_vario['Variogram Index']
    df_model_vario['Dist'] = df_model_vario['Lag Distance']
    df_model_vario['Gamma'] = df_model_vario['Variogram Value']



    legend_names = ['N{}°E'.format(angle) for angle in np.arange(0, 180, 22.5)]
    legend_names.append('Model')

    colors = ['b', 'b--', 'g', 'g--', 'm', 'm--', 'r', 'r--', 'k']

    # PREPARE THE HORIZONTAL PLOT
    plt.figure(figsize=(8, 6))
    plt.xlabel('Distance (m)', fontsize=15)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)

    plt.title(f'{name} horizontal directional', fontsize=15)
    plt.ylabel(r'$\gamma$', fontsize=80, rotation=0, labelpad=25)
    plt.ylim(0.0, 1.30)
    plt.xlim(0, 2000)
    # LOOP OVER THE DIRECTIONS

    for i in range(8):
        df_data_vario_filter = df_data_vario[(df_data_vario['Index'] == i+1) & (df_data_vario['Gamma'] > -98.00)]
        plt.plot(df_data_vario_filter['Dist'].values, df_data_vario_filter['Gamma'].values, colors[i], label = legend_names[i])



    df_model_vario_filter = df_model_vario[df_model_vario['Index']==2]
    plt.plot(df_model_vario_filter['Dist'].values, df_model_vario_filter['Gamma'].values, colors[-1],
             label=legend_names[-1])
    plt.plot([0, 2000], [1, 1], 'k', linewidth=2)

    plt.legend(loc='best', ncol=3, fontsize=12)
    fig_name = f'4-Variograms/NS_Plot/Figs/{name}_horizontal_dir.png'
    plt.savefig(fig_name, dpi=400, bbox_inches='tight', pad_inches=0.1,
                frameon=None)

    plt.close()



    return None





def Plot_Omnidirectional_Variogram(name):
    # Prepare omnidirectional variogram
    df_data_vario = io.Get_Df_From_Variogram_File(f'4-Variograms/NS_Exp/{name}_new.out')
    df_data_vario['Index'] = df_data_vario['Variogram Index']
    df_data_vario['Dist'] = df_data_vario['Lag Distance']
    df_data_vario['Gamma'] = df_data_vario['Variogram Value']

    df_model_vario = io.Get_Df_From_Varmodel_File(f'4-Variograms/Ns_Model/{name}_varmodel.var')
    df_model_vario['Index'] = df_model_vario['Variogram Index']
    df_model_vario['Dist'] = df_model_vario['Lag Distance']
    df_model_vario['Gamma'] = df_model_vario['Variogram Value']

    # PREPARE THE HORIZONTAL PLOT
    plt.figure(figsize=(8, 6))
    plt.xlabel('Distance (m)', fontsize=15)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)

    plt.title(f'{name} horizontal Omnidirectional', fontsize=15)
    plt.ylabel(r'$\gamma$', fontsize=80, rotation=0, labelpad=25)
    plt.ylim(0.0, 1.30)
    plt.xlim(0, 2000)

    df_data_vario_filter = df_data_vario[(df_data_vario['Index'] == 9) & (df_data_vario['Gamma'] > -98.00)]
    plt.plot(df_data_vario_filter['Dist'].values, df_data_vario_filter['Gamma'].values, 'bo',
             label='Experimental')


    df_model_vario_filter = df_model_vario[df_model_vario['Index'] == 2]
    plt.plot(df_model_vario_filter['Dist'].values, df_model_vario_filter['Gamma'].values, 'k',
             label='Model')
    plt.plot([0, 2000], [1, 1], 'k', linewidth=2)
    plt.legend(loc='best', fontsize=12)
    fig_name = f'4-Variograms/NS_Plot/Figs/{name}_horizontal_omni.png'
    plt.savefig(fig_name, dpi=400, bbox_inches='tight', pad_inches=0.1,
                frameon=None)
    plt.close()

    return None

def Plot_Vertical_Variogram(name):
    df_data_vario = io.Get_Df_From_Variogram_File(f'4-Variograms/NS_Exp/{name}_new.out')
    df_data_vario['Index'] = df_data_vario['Variogram Index']
    df_data_vario['Dist'] = df_data_vario['Lag Distance']
    df_data_vario['Gamma'] = df_data_vario['Variogram Value']

    df_model_vario = io.Get_Df_From_Varmodel_File(f'4-Variograms/Ns_Model/{name}_varmodel.var')
    df_model_vario['Index'] = df_model_vario['Variogram Index']
    df_model_vario['Dist'] = df_model_vario['Lag Distance']
    df_model_vario['Gamma'] = df_model_vario['Variogram Value']

    # PREPARE THE VERTICAL PLOT
    plt.figure(figsize=(8, 6))
    plt.xlabel('Distance (m)', fontsize=15)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.title(f'{name} vertical', fontsize=15)
    plt.ylabel(r'$\gamma$', fontsize=80, rotation=0, labelpad=25)
    plt.ylim(0.0, 1.30)
    plt.xlim(0, 5.50)

    df_data_vario_filter = df_data_vario[(df_data_vario['Index'] == 10) & (df_data_vario['Gamma'] > -98.00)]
    plt.plot(df_data_vario_filter['Dist'].values, df_data_vario_filter['Gamma'].values, 'bo',
             label='Experimental')

    df_model_vario_filter = df_model_vario[df_model_vario['Index'] == 1]
    plt.plot(df_model_vario_filter['Dist'].values, df_model_vario_filter['Gamma'].values, 'k',
             label='Model')
    plt.plot([0, 30], [1, 1], 'k', linewidth=2)
    plt.legend(loc='best', fontsize=12)
    fig_name = f'4-Variograms/NS_Plot/Figs/{name}_vertical.png'
    plt.savefig(fig_name, dpi=400, bbox_inches='tight', pad_inches=0.1,
                frameon=None)
    plt.close()

    return None



if __name__ == '__main__':






    names = ['NS_RCG', 'NS_ATGc', 'NS_STGc', 'NS_FEGc', 'NS_TIGc', 'NS_PPGc', 'NS_AAG', 'NS_SRG']
    n_var = len(names)

    nscore_vario_file = '3-Nscore/nscore_orig_vario.out '

    cols = io.get_columns_from_names(filename=nscore_vario_file, names=names)

    for i in range(n_var):
        name = names[i]
        col = cols[i]
        Run_Varmodel(name=name)
        Run_Varcalc_New_Format(name, col)
        Plot_Directional_Variogram(name)
        Plot_Omnidirectional_Variogram(name)
        Plot_Vertical_Variogram(name)

