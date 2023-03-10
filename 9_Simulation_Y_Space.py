import numpy as np
import Python_Module.io_module as io
import time
import multiprocessing
from SGS_functions import Create_list_of_seeds, Run_Usgsim_single



if __name__ == '__main__':


    start = time.time()
    start_global = time.time()
    dic_grid = io.get_grid_dict('6-Grid/grid_fine_inf.txt')
    grid_size = dic_grid['nx'] * dic_grid['ny'] * dic_grid['nz']
    n_real = 40
    i_real_list = np.arange(1, n_real + 1)

    # Create list of seeds for simulation
    np.random.seed(69069)
    names_ns = ['NS_RCG', 'NS_ATGc', 'NS_STGc', 'NS_FEGc', 'NS_TIGc', 'NS_PPGc', 'NS_AAG', 'NS_SRG']

    #names_ns_ratios = ['NS_RC', 'NS_A1', 'NS_A2', 'NS_A3', 'NS_A4', 'NS_FR_AA', 'NS_FR_SR']

    names = ['PPMT_RCG', 'PPMT_A1', 'PPMT_A2', 'PPMT_A3', 'PPMT_A4', 'PPMT_PPGc', 'PPMT_FR_AAG', 'PPMT_FR_SRG']
    cols = np.arange(21, 29)


    n_var = len(names_ns)
    seeds = Create_list_of_seeds(n_real=n_real*n_var)
    seeds = np.reshape(seeds, newshape=(n_real, n_var))
    grid_file = '6-Grid/grid_fine_inf.txt'
    sufix = 'end'




    for i in range(n_var):
#
        seed_list = seeds[:, i]
        name = names[i]
        name_list = [name]*n_real
#
        name_gamma = names_ns[i]
        name_gamma_list = [name_gamma]*n_real
#
        col = cols[i]
        col_list = [col]*n_real
#
#
        grid_file_list = [grid_file]*n_real
        sufix_list = [sufix]*n_real
        zipped_params = zip(seed_list, name_list, name_gamma_list, col_list, i_real_list, grid_file_list, sufix_list)
        with multiprocessing.Pool(processes=5) as p:
            p.starmap(func=Run_Usgsim_single, iterable=zipped_params)
#



