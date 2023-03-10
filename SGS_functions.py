
import numpy as np
import matplotlib.pyplot as plt
import os
import subprocess
from Python_Module.Get_Var_String import get_var_string
import Python_Module.io_module as io


def Create_list_of_seeds(n_real):
    list_of_seeds = []
    for i in range(n_real):
        list_of_seeds.append(np.random.randint(20000, 50000) * 2 + 1)

    return list_of_seeds

def Run_Usgsim_single(seed, name, name_gamma, col, i_real, grid_file, sufix):
    grid_string = io.read_grid_info(file_name=grid_file)

    par_path = os.path.join('7-Simulation_Y_Space', f'{i_real}_{name}.par')
    parfile = open(par_path, 'w')
    parfile.write(f'''
               Parameters for USGSIM
               *********************

START OF MAIN:
1                             -number of realizations to generate, 0=kriging
1                            -number of variables being simulated
1                             -number of rock types to consider
{seed}                         -random number seed
{grid_string}
7-Simulation_Y_Space/{i_real}_{name}_{sufix}.out                     -file for simulation output
0                             -  output format: (0=reg, 1=coord, 2=binary)
impute.out                    -file for imputed values in case of heterotopic samples
0                             -debugging level: 0,1,2,3
./Sgsim/sgsim.dbg                     -file for debugging output


START OF SRCH:
64                            - number of data to use per variable
2000.0   2000.0   20.0        - maximum search radii (hmax,hmin,vert)
0.0    0.0    0.0             -angles for search ellipsoid
1                             -sort by distance (0) or covariance (1)
1 1 1                         -if sorting by covariance, indicate variogram rock type, head, tail to use


START OF VARG:
1                            -number of variograms \n''')
    parfile.write('1 1 1  - Rock type, head variable, tail variable \n')
    vmodel_file = os.path.join('4-Variograms', 'NS_Model', f'{name_gamma}.par')
    var_string = get_var_string(vmodel_file)
    parfile.write('{} '.format(var_string))
    parfile.write(f'''

START OF DATA:
5-Ppmt/ppmt.out                -  file with primary data
2  3  4  0  20                 -  columns for X,Y,Z,wt,rock type
{col}                          -  columns for variables
0                              -  clip data to grid, 1=yes
1                              -  assign to the grid, 0=none, 1=nearest, 2=average
-98.0       1.0e21             -  trimming limits



START OF ROCK:
1                       -rock type codes
6-Grid/keyout_fine.out                    -file with rock types
1                             -column for rock type

''')
    parfile.close()
    exe_path = os.path.join('Gslib', 'usgsim.exe')
    subprocess.call([exe_path, par_path], shell=True)
