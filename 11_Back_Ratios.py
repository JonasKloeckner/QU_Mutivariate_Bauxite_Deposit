import numpy as np
import os
import Python_Module.io_module as io
import time
import pandas as pd

import multiprocessing



def Back_Ratios(i_real, sufix):
    input_names = ['RCG', 'A1', 'A2', 'A3', 'A4', 'PPGc', 'FR_AAG', 'FR_SRG']
    names_out = ['RCG', 'ATGc', 'STGc', 'FEGc', 'TIGc', 'PPGc', 'AAG', 'SRG']
    cols = np.arange(1, 9)

    start = time.time()
    input_file = f'8-Simulation_Ratios/{i_real}_{sufix}.out'
    output_file = f'9-Simulation_Orig_Units/{i_real}_{sufix}.out'

    print(f'start reading real {i_real}')
    data_array = io.get_array_gslib_pd(filename=input_file, list_of_cols=cols)
    print(f'finish reading real {i_real}')

    df = pd.DataFrame(data=data_array, columns=input_names)

    mask = df['RCG'] > -98.0

    df['RCG'] = np.where(mask, df['RCG'], -99)

    df['SUM_BACK'] = (df['A1'] + df['A2'] + df['A3'] + df['A4'] + 1.00)

    df['ATGc'] = np.where(mask, (df['A1'] * 100.00) / df['SUM_BACK'], -99)
    df['STGc'] = np.where(mask, (df['A2'] * 100.00) / df['SUM_BACK'], -99)
    df['FEGc'] = np.where(mask, (df['A3'] * 100.00) / df['SUM_BACK'], -99)
    df['TIGc'] = np.where(mask, (df['A4'] * 100.00) / df['SUM_BACK'], -99)
    df['PPGc'] = np.where(mask, df['PPGc'], -99)

    df['AAG'] = np.where(mask, df['FR_AAG'] * df['ATGc'], -99)
    df['SRG'] = np.where(mask, df['FR_SRG'] * df['STGc'], -99)

    df_out = df[names_out]
    print(f'start writing real {i_real}')
    test = io.to_Gslib(output_file=output_file, dataframe=df_out, float_format='%.4f')
    print(f'finish writing real {i_real}')

    finish = time.time()
    print('time for one realization = {:.4f} seconds'.format(finish - start))

    # Remove simulation ratios to free space
    if (i_real != 1):
        os.remove(f'8-Simulation_Ratios/{i_real}_{sufix}.out')


    return None

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


if __name__ == '__main__':

    n_real = 40
    sufix = 'end'

    dic_grid = io.get_grid_dict('6-Grid/grid_fine_inf.txt')
    grid_size = dic_grid['nx'] * dic_grid['ny'] * dic_grid['nz']


    for i in range(n_real):
        i_real = i + 1

        zipped_params_1 = zip([i_real], [sufix])
        with multiprocessing.Pool(processes=1) as p:
            p.starmap(func=Back_Ratios, iterable=zipped_params_1)


