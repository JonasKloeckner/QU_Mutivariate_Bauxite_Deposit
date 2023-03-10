import numpy as np
import os
import Python_Module.io_module as io
import time
import pandas as pd

import multiprocessing



def Simulation_z_bot_cut(i_real, grid_size, sufix):
    input_in_sim_file = f'9-Simulation_Orig_Units/{i_real}_{sufix}.out'
    guide_model = f'9-Simulation_Orig_Units/guide_model_CODE2.csv'

    z_bot = [-100]
    n_z_bot = len(z_bot)
    cols_in_sim = np.arange(1, 9)

    names_out_sim = ['VAR_z_{}'.format(i) for i in cols_in_sim]
    code_guide_model = ['CODE']

    print('working on guide model')
    guide_model_array = pd.read_csv(guide_model, sep=',', header=0)
    df_code = pd.DataFrame(data=guide_model_array, columns=code_guide_model)
    code = df_code[code_guide_model[0]].astype(int)


    print('selecting z_bot in realization = {}'.format(i_real))
    sim_in_array_ireal = io.get_ireal_pd(filename=input_in_sim_file, list_of_cols=cols_in_sim, grid_size=grid_size, ireal=1)
    df_in_sim = pd.DataFrame(data=sim_in_array_ireal, columns=names_out_sim)

    for i in range(n_z_bot):

        filter_z_bot = code != z_bot[i]
        z_bot_value = df_in_sim[filter_z_bot]

        out_sim_file_z = f'9-Simulation_Orig_Units/Simulation_z_bot_cut/{i_real}_{sufix}_z.out'

        test = io.to_Gslib(output_file=out_sim_file_z, dataframe=z_bot_value, float_format='%.4f')

    return None


def filter_sim_file(i_real, grid_size, sufix):
    input_sim_file = f'9-Simulation_Orig_Units/Simulation_z_bot_cut/{i_real}_{sufix}_z.out'
    out_sim_file = f'9-Simulation_Orig_Units/Simulation_z_bot_cut/{i_real}_{sufix}_f.out'

    cols = np.arange(1, 9)
    names_sim = ['VAR_{}'.format(i) for i in cols]

    print('filtering real test = {}'.format(i_real))
    sim_array_ireal = io.get_ireal_pd(filename=input_sim_file, list_of_cols=cols, grid_size=grid_size, ireal=1)
    df_sim = pd.DataFrame(data=sim_array_ireal, columns=names_sim)
    df_sim_f = df_sim[df_sim['VAR_1'] > -98.00]

    test = io.to_Gslib(output_file=out_sim_file, dataframe=df_sim_f, float_format='%.4f')

    return None

if __name__ == '__main__':
    n_real = 40
    sufix = 'end'

    dic_grid = io.get_grid_dict('6-Grid/grid_fine_inf.txt')
    grid_size = dic_grid['nx'] * dic_grid['ny'] * dic_grid['nz']

    for i in range(n_real):
        i_real = i + 1 
        print(i_real, 'guide model')
        zipped_params = zip([i_real], [grid_size],[sufix])
        with multiprocessing.Pool(processes=1) as p:
            p.starmap(func=Simulation_z_bot_cut, iterable=zipped_params)
        #Simulation_z_bot_cut(i_real, grid_size, sufix)

    for i in range(n_real):
        i_real = i + 1
        print('ireal filter ', i_real)
        zipped_params_2 = zip([i_real], [grid_size],[sufix])
        with multiprocessing.Pool(processes=1) as p:
            p.starmap(func=filter_sim_file, iterable=zipped_params_2)
#