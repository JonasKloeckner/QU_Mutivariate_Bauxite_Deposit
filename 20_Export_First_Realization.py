
import sys
import Python_Module.io_module as io
import linecache
import numpy as np
import time
import pandas as pd
if __name__ == '__main__':
    start = time.time()

    # INPUT PARAMETERS
    real = 1

    sim_file = f'9-Simulation_Orig_Units/{real}_end.out'



    names = ['RCG', 'ATGc', 'STGc', 'FEGc', 'TIGc', 'PPGc', 'AAG', 'SRG']

    dic_grid = io.get_grid_dict('6-Grid/grid_fine_inf.txt')
    grid_size = dic_grid['nx']*dic_grid['ny']*dic_grid['nz']

    n_var = len(names)


    print('reading sim')
    df_sim = io.Get_Df_From_Sim_File(file_name=sim_file ,grid_size=grid_size)
    print('finish reading sim')

    names_out = ['RCG', 'ATGc', 'STGc', 'FEG']

    for i in range(n_var):

        name = names[i]
        print(name)
        df_out =df_sim[[name]]
        out_vtk_file = f'10-Validation/VTK/{real}_end_{name}.vtk'

        io.export_grid_into_VTK_File(dataframe=df_out, out_vtk_file=out_vtk_file, dict_grid=dic_grid)

    finish = time.time()

    print('Total time  = {:.2f} seconds'.format(finish-start))