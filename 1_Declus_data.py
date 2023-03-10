
import Python_Module.io_module as io
import numpy as np
import pandas as pd

import os
import subprocess

import matplotlib.pyplot as plt




def Run_Declus(data_file, out_file):
    par_path = 'declus.par'
    pf = open(par_path, 'w')
    pf.write(f'''                  Parameters for DECLUS
                      *********************

START OF PARAMETERS:
{data_file}         -file with data
2   3   0   6               -  columns for X, Y, Z, and variable
-98.0     1.0e21          -  trimming limits
1-Data/declus_AAG_2D.sum                  -file for summary output
{out_file}                  -file for output with data & weights
1.0   1.0                   -Y and Z cell anisotropy (Ysize=size*Yanis)
0                           -0=look for minimum declustered mean (1=max)
1  200.0  200.0               -number of cell sizes, min size, max size
5                           -number of origin offsets
''')
    pf.close()

    exe_path = os.path.join('Gslib', 'declus')
    subprocess.call([exe_path, par_path], shell=True)
    #os.remove(par_path)
    return None



if __name__ == '__main__':

    # Create data_file_2D
    data_file_3d = '1-Data/Bauxite_north_strat_G.dat'
    df = io.Get_Df_From_File(file_name=data_file_3d)
    df['ATG_Ac'] = df['ATG' ] *df['LENGTH']
    n_rows = df.shape[0]
    df_group = df.groupby(by='BHID', as_index=False)


    df_xy = df_group.mean()
    df_max = df_group.max()
    df_min = df_group.min()
    df_sum = df_group.sum()
    df_sum['ATG_mean'] =df_sum['ATG_Ac'] / df_sum['LENGTH']

    bhid_array = df_xy['BHID'].values

    n_rows = len(bhid_array)

    names = ['X', 'Y', 'Z', 'THICK', 'ATG_mean']

    z_array = np.zeros(n_rows)

    x_array = df_xy['X'].values
    y_array = df_xy['Y'].values
    thick_array = df_sum['LENGTH'].values
    AAG_array = df_sum['ATG_mean'].values

    data_array = np.column_stack((x_array, y_array, z_array, thick_array, AAG_array))

    df_out = pd.DataFrame(data=data_array, columns=names)
    df_out['BHID'] = bhid_array

    # Change column order
    df_out = df_out[['BHID', 'X', 'Y', 'Z', 'THICK', 'ATG_mean']]

    data_2D_file = '1-Data/Bauxite_north_strat_2D.dat'

    test = io.to_Gslib(output_file=data_2D_file, dataframe=df_out, float_format='%.4f')
    # Finish creating 2d dataset

    # Running declus into 2d dataset
    declus_file = '1-Data/declus_2D.txt'
    Run_Declus(data_file=data_2D_file, out_file=declus_file)

    # Put the weights of the 2d dataset into the 3d dataset

    df_declus_2d = io.Get_Df_From_File(declus_file)
    print(df_declus_2d.columns)

    BHID_array = df_declus_2d['BHID'].values
    declus_weight = df_declus_2d['Declustering'].values
    print(declus_weight)

    dict_declus = {}
    for i in range(len(BHID_array)):
        dict_declus[BHID_array[i]] = declus_weight[i]

    n_data = df.shape[0]
    declus_3d_array = np.zeros(n_data)
    BHID_array_3D = df['BHID'].values

    for i in range(n_data):
        declus_3d_array[i] = dict_declus[BHID_array_3D[i]]

    df['Decl_w'] = declus_3d_array
    print(df['Decl_w'].values)

    out_file = '1-Data/declus_3D.out'
    test = io.to_Gslib(output_file=out_file, dataframe=df, float_format='%.4f')










