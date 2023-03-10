import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
import subprocess
import Python_Module.io_module as io
import time
import pandas as pd
import multiprocessing



def selection_polygons_area(i_real, grid_size, polygons, sufix):

    input_in_sim_file = f'9-Simulation_Orig_Units/{i_real}_{sufix}.out'
    guide_model = f'12-From_polygons/guide_model_CODE2.csv'

    n_polygons = len(polygons)
    cols_in_sim = np.arange(1, 9)
    n_var = len(cols_in_sim)

    names_out_sim = ['VAR_p_{}'.format(i) for i in cols_in_sim]
    code_guide_model = ['CODE']

    print('working on guide model')
    guide_model_array = pd.read_csv(guide_model, sep=',', header=0)
    df_code = pd.DataFrame(data=guide_model_array, columns=code_guide_model)
    code = df_code[code_guide_model[0]].astype(int)


    print('selecting polygons areas = {}'.format(i_real))
    sim_in_array_ireal = io.get_ireal_pd(filename=input_in_sim_file, list_of_cols=cols_in_sim, grid_size=grid_size, ireal=1)
    df_in_sim = pd.DataFrame(data=sim_in_array_ireal, columns=names_out_sim)

    for i in range(n_polygons):

        filter_polygons = code == polygons[i]
        polygons_value = df_in_sim[filter_polygons]
        

        out_sim_poly_file = f'12-From_polygons/{i_real}_{polygons[i]}_{sufix}_p.out'

        test = io.to_Gslib(output_file=out_sim_poly_file, dataframe=polygons_value, float_format='%.4f')

    return None


def get_etype_polygons(n_real, polygons, sufix):
    
    n_var = 8
    n_polygons = len(polygons)
    for k in range(n_var):
        i_var = k + 1
        array_mean_values = np.zeros((n_polygons, n_real))
        for j in range(n_real):
            i_real = j + 1
            for i in range(n_polygons):
                input_file = f'12-From_polygons/{i_real}_{polygons[i]}_{sufix}_p.out'
                df_polygon = io.Get_Df_From_File(input_file)
                df_polygon_f = df_polygon[df_polygon['VAR_p_1']>-98.0]
                mean_of_variable = df_polygon_f['VAR_p_{}'.format(i_var)].mean()
                array_mean_values[i, j] = mean_of_variable

        out_file = f'12-From_polygons/VAR_{i_var}_Mean_Of_Polygons_{sufix}_p.out'
        names = ['Real_{}_Polygon'.format(i) for i in range(1, n_real + 1)]
        df_out = pd.DataFrame(data=array_mean_values, columns = names)
        df_out['Polygon_ID'] = polygons
        df_out['E_Type_Polygons'] = np.mean(array_mean_values, axis=1)
        df_out['Std_Dev_Polygons'] = np.std(array_mean_values, axis=1)
        df_out['Coeffient_Variation'] = np.std(array_mean_values, axis=1)/np.mean(array_mean_values, axis=1)
        test = io.to_Gslib(output_file=out_file, dataframe=df_out, float_format='%.4f')

    return None


if __name__ == '__main__':


    start = time.time()

    dic_grid = io.get_grid_dict('6-Grid/grid_fine_inf.txt')
    grid_size = dic_grid['nx'] * dic_grid['ny'] * dic_grid['nz']

    n_real = 40
    sufix = 'end'
    names= ['RCG', 'ATGc', 'STGc', 'FEGc', 'TIGc', 'PPGc', 'AAG', 'SRG']
    i_var = len(names)
     
    polygons = [2017010, 2017020, 2017030, 2017040, 2017050, 2017060, 2017070, 2017080, 2017090, 2017100, 2017110, 2017120,
    			2017011, 2017021, 2017031, 2017041, 2017051, 2017061, 2017071, 2017081, 2017091, 2017101, 2017111, 2017121,
    			2018010, 2018020, 2018030, 2018040, 2018050, 2018060, 2018070, 2018080, 2018090, 2018100, 2018110, 2018120,
    			2018011, 2018021, 2018031, 2018041, 2018051, 2018061, 2018071, 2018081, 2018091, 2018101, 2018111, 2018121]


    for i in range(n_real):
        i_real = i + 1
        print(i_real)

        zipped_params = zip([i_real], [grid_size], [polygons], [sufix])
        with multiprocessing.Pool(processes=1) as p:
            p.starmap(func=selection_polygons_area, iterable=zipped_params)

    
    get_etype_polygons(n_real, polygons, sufix)