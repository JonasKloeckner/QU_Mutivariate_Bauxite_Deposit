
import multiprocessing
import os
import subprocess
import numpy as np
import Python_Module.io_module as io
import pandas as pd
import time







def merge_simulations_fortran(i_real):
    names = ['PPMT_RCG', 'PPMT_A1', 'PPMT_A2', 'PPMT_A3', 'PPMT_A4', 'PPMT_PPGc', 'PPMT_FR_AAG', 'PPMT_FR_SRG']
    par_path = 'merge_mult.par'
    sufix = 'end'
    pf = open(par_path, 'w')
    pf.write(f'''START OF PARAMETERS:
8                                 -number of data files to merge
8                                 -total # of variable models to merge
7-Simulation_Y_Space/{i_real}_{sufix}.out                          -output file \n''')
    for i in range(len(names)):
        name = names[i]
        pf.write(f'''7-Simulation_Y_Space/{i_real}_{name}_{sufix}.out
1
1  \n''')


    pf.close()
    exe_path = os.path.join('Gslib','merge_multi.exe')
    subprocess.call([exe_path, par_path], shell=True)


    return None




def merge_simulations_fortran_2(i_real):

    par_path = 'combine.par'
    sufix = 'end'
    pf = open(par_path, 'w')
    pf.write(f'''                  Parameters for COMBINE
                  ***********************

START OF PARAMETERS:
8                              -number of files
7-Simulation_Y_Space/{i_real}_PPMT_RCG_end.out
1                              -   number of variables
1                              -   columns
7-Simulation_Y_Space/{i_real}_PPMT_A1_end.out
1
1  
7-Simulation_Y_Space/{i_real}_PPMT_A2_end.out
1
1  
7-Simulation_Y_Space/{i_real}_PPMT_A3_end.out
1
1  
7-Simulation_Y_Space/{i_real}_PPMT_A4_end.out
1
1  
7-Simulation_Y_Space/{i_real}_PPMT_PPGc_end.out
1
1 
7-Simulation_Y_Space/{i_real}_PPMT_FR_AAG_end.out
1
1  
7-Simulation_Y_Space/{i_real}_PPMT_FR_SRG_end.out
1
1
7-Simulation_Y_Space/{i_real}_end.out                    -file for output
    
    
    ''')

    pf.close()
    exe_path = os.path.join('Gslib','combine.exe')
    subprocess.call([exe_path, par_path], shell=True)


    return None




def merge_simulations_fortran_ult(i_real):
    names = ['PPMT_RCG', 'PPMT_A1', 'PPMT_A2', 'PPMT_A3', 'PPMT_A4', 'PPMT_PPGc', 'PPMT_FR_AAG', 'PPMT_FR_SRG']
    par_path = 'umerge_manip.par'
    sufix = 'end'
    pf = open(par_path, 'w')
    pf.write(f'''Parameters for UMERGE_MANIP
***************************

START OF PARAMETERS:
7-Simulation_Y_Space/{i_real}_{sufix}.out  
1604 684 17 1                     -nx, ny, nz, nreal (calculated if nx*ny*nz=0)
-98.0 1.0e21                      -trimming limits
8                            -# of gridded models to merge \n''')
    for i in range(len(names)):
        name = names[i]
        pf.write(f'''7-Simulation_Y_Space/{i_real}_{name}_{sufix}.out
1     1                -  # of variables and col #s to extract
0                      -  replicate single grid nreal times?   \n''')

    pf.close()
    exe_path = os.path.join('Gslib','umerge_manip.exe')
    subprocess.call([exe_path, par_path], shell=True)


    return None

def merge_simulations(i_real):
    names = ['PPMT_RCG', 'PPMT_A1', 'PPMT_A2', 'PPMT_A3', 'PPMT_A4', 'PPMT_PPGc', 'PPMT_FR_AAG', 'PPMT_FR_SRG']
    dic_grid = io.get_grid_dict('6-Grid/grid_fine_inf.txt')
    grid_size = dic_grid['nx'] * dic_grid['ny'] * dic_grid['nz']
    array = np.zeros(shape=(grid_size, 8))
    sufix = 'end'


    for i in range(len(names)):
        name = names[i]
        sim_file = f'7-Simulation_Y_Space/{i_real}_{name}_{sufix}.out'
        print('reading simulation')
        array_temp = io.get_ireal_pd(filename=sim_file, list_of_cols=np.array([1]), grid_size=grid_size, ireal=1)
        array[:, i] = array_temp[:, 0]

    df = pd.DataFrame(data=array, columns=names)

    out_file = f'7-Simulation_Y_Space/{i_real}_{sufix}.out'
    print('writing simulation')
    test = io.to_Gslib(output_file=out_file, dataframe=df, float_format='%.8f')

    for i in range(len(names)):
        name = names[i]
        os.remove(f'7-Simulation_Y_Space/{i_real}_{name}_{sufix}.out')
    return None


def PPMT_backtr(i_real):
    sufix = 'end'
    par_path = os.path.join('8-Simulation_Ratios', f'{i_real}.par')
    pf = open(par_path, 'w')
    pf.write(f'''                 PPMT Back Transformation
                 ************************

START OF PARAMETERS:
5-Ppmt/ppmt.trn                      -file with transformation data
7-Simulation_Y_Space/{i_real}_{sufix}.out                    -file with data to back-transform (GSB detection)
8 1 2 3 4 5 6 7 8                      - nvar, column numbers
-97.0 1.0e21                   - trimming limits
1604   684    17 1                   - nx, ny, nz, nreal (ignored if nx = 0)
8-Simulation_Ratios/{i_real}_{sufix}.out                    -file for back transformed values
0                             -enforce N(0,1)? (0=no,1=yes)
-----------------------------------------------------------------
     Disregard the following lines if not enforcing N(0,1) 
-----------------------------------------------------------------
1                             -consider local uncertainty? (0=no,1=yes)
kt3dv.out                     - local file
1 2                           -  columns for kriging variances
.2                            -  weight factor
5                             -  number of loops
    ''')
    pf.close()
    exe_path = os.path.join('Gslib', 'ppmt_b')
    subprocess.call([exe_path, par_path], shell=True)
    os.remove(par_path)

    # remove simulations on Y_space to free memory
    if(i_real != 1):
        os.remove(f'7-Simulation_Y_Space/{i_real}_{sufix}.out')

    return None




if __name__ == '__main__':

    start = time.time()



    sufix = 'end'
    n_real = 40

    for i in range(n_real):
        i_real = i + 1
        print('ireal = {}'.format(i_real))
        with multiprocessing.Pool(processes=1) as p:
            p.map(func=merge_simulations, iterable=[i_real])



#    merge_simulations_fortran_2(i_real=37)

    i_real_list = np.arange(1, n_real+1)

#
    with multiprocessing.Pool(processes=5) as p:
        p.map(func=PPMT_backtr, iterable= i_real_list)
#
#





