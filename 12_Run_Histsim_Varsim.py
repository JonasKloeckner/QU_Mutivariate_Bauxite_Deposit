import numpy as np
import matplotlib.pyplot as plt
import os
import subprocess
from Python_Module.Get_Var_String import get_var_string
import Python_Module.io_module as io
import time
import pandas as pd
import multiprocessing


#def filter_sim_file(i_real, grid_size, sufix):
#    input_sim_file = f'9-Simulation_Orig_Units/{i_real}_{sufix}.out'
#    out_sim_file = f'9-Simulation_Orig_Units/{i_real}_{sufix}_f.out'
#
#    cols = np.arange(1, 9)
#    names_sim = ['VAR_{}'.format(i) for i in cols]
#
#    print('filtering real test = {}'.format(i_real))
#    sim_array_ireal = io.get_ireal_pd(filename=input_sim_file, list_of_cols=cols, grid_size=grid_size, ireal=1)
#    df_sim = pd.DataFrame(data=sim_array_ireal, columns=names_sim)
#    df_sim_f = df_sim[df_sim['VAR_1'] > -98.00]
#
#    test = io.to_Gslib(output_file=out_sim_file, dataframe=df_sim_f, float_format='%.4f')
#
#    return None

def Histpltsim(name, col_data,  col_sim, i_real, n_nodes_f, sufix, n_quantiles):
    par_path = f'{name}_{i_real}.par'
    pf = open(par_path, 'w')
    pf.write(f'''                  Parameters for HISTPLTSIM
                  *************************

START OF PARAMETERS:
../data/lithology.dat        -file with lithology information
0   0    0                    -   lithology column (0=not used), code
1-Data/proc_data.txt      -file with data
{col_data}   19                        -   columns for reference variable and weight
9-Simulation_Orig_Units/Simulation_z_bot_cut/{i_real}_{sufix}_z.out          -file with data
{col_sim}   0                        -   columns for variable and weight
0     1                      -   data (0=simulation, 1=multi columns), numeric output
1  1                        -   start and finish histograms (usually 1 and nreal)
{n_nodes_f}   1   1                 -   nx, ny, nz
-1.0     1.0e21              -   trimming limits
10-Validation/Hist_orig_z_bot_cut/{name}_{i_real}_{sufix}.ps                -file for PostScript output
10-Validation/Hist_orig_z_bot_cut/{name}_{i_real}_{sufix}_sum.out       -file for summary output (always used)
10-Validation/Hist_orig_z_bot_cut/{name}_{i_real}_{sufix}_num.out       -file for numeric output (used if flag set above)
0.0      -20.0               -attribute minimum and maximum
-1.0                         -frequency maximum (<0 for automatic)
20                           - number of classes
0                            -0=arithmetic, 1=log scaling
1                            -0=frequency, 1=cumulative histogram
{n_quantiles}                -number of cum. quantiles (<0 for all)
2                            -number of decimal places (<0 for auto.)
{name}               -title
1.5                          -positioning of stats (L to R: -1 to 1)
-1.1e21                      -reference value for box plot
''')
    pf.close()
    exe_path = os.path.join('Gslib', 'histpltsim')
    subprocess.call([exe_path, par_path], shell=True)
    os.remove(par_path)

def Read_histogram_ireal(name, i_real, sufix, n_quantiles):
    hist_file = f'10-Validation/Hist_orig_z_bot_cut/{name}_{i_real}_{sufix}_num.out'
    names = ['values', 'cdf']
    df_hist = pd.read_csv(hist_file, skiprows=4, nrows=n_quantiles, names = names,    delim_whitespace=True)
    return df_hist

def Read_histogram_data(name, i_real, sufix, n_quantiles, n_data):
    hist_file = f'10-Validation/Hist_orig_z_bot_cut/{name}_{i_real}_{sufix}_num.out'
    names = ['values', 'cdf']
    df_hist = pd.read_csv(hist_file, skiprows=4+n_quantiles+1, nrows=n_data, names = names,  delim_whitespace=True )
    return df_hist

def Run_Varcalc(name, col):
    par_path = os.path.join('4-Variograms', 'Orig_Exp', f'{name}.par')
    pf = open(par_path, 'w')
    pf.write(f'''                  Parameters for VARCALC
                  **********************

START OF PARAMETERS:
1-Data/proc_data.txt         -  file with data
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
4-Variograms/Orig_Exp/{name}.out                       -file for experimental variogram points output.
0                                 -legacy output (0=no, 1=write out gamv2004 format)
1                                 -run checks for common errors
1                                 -standardize sills? (0=no, 1=yes)
1                                 -number of variogram types
1   1   1  ?                       -tail variable, head variable, variogram type (and cutoff/category), sill
''')
    pf.close()
    exe_path = os.path.join('Gslib', 'varcalc')
    subprocess.call([exe_path, par_path], shell=True)
    os.remove(par_path)

    return None



def Run_Varsim( name_var, col, sufix, i_real):

    par_path = os.path.join(f'{name_var}_{i_real}_{sufix}.par')
    pf = open(par_path, 'w')
    pf.write(f'''                Parameters for GAMSIM_AVE
                *************************
START OF PARAMETERS:
../data/lithology.dat        -file with lithology information
0   7                        -   lithology column (0=not used), code
9-Simulation_Orig_Units/{i_real}_{sufix}.out      -file with data
1  {col}      {col}             -   number of variables, column numbers
-97.0     1.0e21    -   trimming limits
10-Validation/Vario/{name_var}_{i_real}_{sufix}.out        -output file for variograms of realizations
10-Validation/Vario/{name_var}_{i_real}_{sufix}_avg.out        -output file for average variogram
1604   584728.125    6.25                  -nx,xmn,xsiz
684   9722528.125   6.25                  -ny,ymn,ysiz
17    -8.25    0.5                  -nz,zmn,zsiz    
1                         - number of realizations
2  500                 -number of directions, number of lags
 1  0  0              -ixd(1),iyd(1),izd(1)
 0  0  1              -ixd(2),iyd(2),izd(2)
1                     -standardize sill? (0=no, 1=yes)
1                     -number of variograms
1   1   1             -tail variable, head variable, variogram type
type 1 = traditional semivariogram
     2 = traditional cross semivariogram
     3 = covariance
     4 = correlogram
     5 = general relative semivariogram
     6 = pairwise relative semivariogram
     7 = semivariogram of logarithms
     8 = semimadogram
     9 = indicator semivariogram - continuous
     10= indicator semivariogram - categorical
    ''')
    pf.close()
    exe_path = os.path.join('Gslib', 'varsim')
    subprocess.call([exe_path, par_path], shell=True)
    os.remove(par_path)

    return None


if __name__ == '__main__':


    start = time.time()

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
    df_temp = io.Get_Df_From_File(file_name = '9-Simulation_Orig_Units/Simulation_z_bot_cut/1_end_z.out')
    n_nodes_f = df_temp.shape[0]
    n_quantiles = 200000
    n_data = 7609
    sufix = 'end'

    i_real_list = np.arange(1, n_real + 1)
    n_nodes_f_list = [n_nodes_f] * n_real
    sufix_list = [sufix] * n_real
    n_quantiles_list = [n_quantiles] * n_real



    names = ['RCG', 'ATGc', 'STGc', 'FEGc', 'TIGc', 'PPGc', 'AAG', 'SRG']
    n_var = len(names)

    data_file = '1-Data/proc_data.txt'
    cols_data = io.get_columns_from_names(data_file, names)

    # Experimental for the data
 #   for i in range(len(names)):
 #       name = names[i]
 #       col_data = cols_data[i]
 #       Run_Varcalc(name=name, col=col_data)
 #       print ('Running varcalc')



    for i in range(n_var):

        name = names_orig[i]
        col_data = cols_data[i]
        col_sim = cols_sim[i]

        name_list = [name]*n_real
        col_data_list = [col_data]*n_real
        col_sim_list = [col_sim]*n_real


        zipped_params = zip(name_list, col_data_list, col_sim_list, i_real_list, n_nodes_f_list, sufix_list,
                            n_quantiles_list)
        with multiprocessing.Pool(processes=5) as p:
            p.starmap(func=Histpltsim, iterable=zipped_params)

#        zipped_params = zip(name_list, col_sim_list, sufix_list, i_real_list)
#        with multiprocessing.Pool(processes=5) as p:
#            p.starmap(func=Run_Varsim, iterable=zipped_params)



    finish = time.time()
    print('Check histogram and variogram time = {:.2f} seconds'.format(finish-start))