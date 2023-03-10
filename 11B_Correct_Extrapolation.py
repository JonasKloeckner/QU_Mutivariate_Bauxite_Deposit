
import os
import subprocess
import Python_Module.io_module as io
import numpy as np
import time
import multiprocessing

def Run_mvs_sum_check(i_real):

    sim_file = f'9-Simulation_Orig_Units/{i_real}_end.out'
    names = ['ATGc', 'STGc', 'FEGc', 'TIGc', 'PPGc']
    col_sim = io.get_columns_from_names(sim_file, names)
    col_strings = ' '.join([str(col) for col in col_sim])
    n_var = len(names)

    df_data = io.Get_Df_From_File('1-Data/proc_data.txt')
    df_min =df_data[names].min()
    df_max = df_data[names].max()

    min_string = ' '.join([str(value) for value in df_min.values ])
    max_string = ' '.join([str(value) for value in df_max.values ])

    par_path = 'parfile_name.par'
    pf = open(par_path, 'w')
    pf.write(f'''   *************************************************  
                  MULTIVARIATE SIMULATION CHECK FOR SUM CONSTRAINTS   
                  ************************************************* 
START OF PARAMETERS:
9-Simulation_Orig_Units/{i_real}_end.out           - simulation file
-98.00 1.0e21               - trimming limits
1604   684    17 1          - nx, ny, nz, nreal
1 10                        - number of constraints to consider and maximum number of iterations
100.00 0.001                - maximum sum of variables and tolerance for sum constraints 
{n_var}                     - number of variables for sum constraint 1 
{col_strings}               - cols of variables  for sum constraint 1
{min_string}                - minimum of data for sum constraint 1
{max_string}                - maximum of data for sum constraint 1
Error_report_sum.out        - report of the errors for sum constraints
9-Simulation_Orig_Units/{i_real}_end_cor_temp.out          

-----------------------------------------------------------------------------------
NOTES TO HELP THE USER

Correction:
1. The algorithm corrects values outside the range of the data (min, max) to the closest boundary.
2. The algorithm corrects values if the sum of simulated values is greater than sum_parameter + tolerance
        	''')
    pf.close()
    exe_path = os.path.join('Gslib','mvs_sum_check')
    subprocess.call([exe_path, par_path], shell=True)
    return None


def Check_Fractional_Grades(i_real, min_AA, max_AA, min_SR, max_SR, grid_size):

    sim_file = f'9-Simulation_Orig_Units/{i_real}_end_cor_temp.out'
    print('reading sim file')
    df = io.Get_Df_From_Sim_File(file_name=sim_file, grid_size = grid_size)
    df.columns = ['RCG', 'ATGc', 'STGc', 'FEGc', 'TIGc', 'PPGc', 'AAG', 'SRG']
    print('finish reading sim file')



    mask = df['AAG'] > -98.00

    n_nodes = df[mask].shape[0]

    n_corr_AA_max = df[mask & (df['AAG'] > max_AA)].shape[0]
    n_corr_AA_min = df[mask & (df['AAG'] < min_AA)].shape[0]
    n_corr_AA = n_corr_AA_max + n_corr_AA_min
    prop_correction_AA = (n_corr_AA/float(n_nodes))*100.00

    df['AAG'] = np.where(mask, np.minimum( np.maximum(df['AAG'], min_AA), max_AA) , -99 )

    n_corr_SR_max = df[mask & (df['SRG'] > max_SR)].shape[0]
    n_corr_SR_min = df[mask & (df['SRG'] < min_SR)].shape[0]
    n_corr_SR = n_corr_SR_max + n_corr_SR_min
    prop_correction_SR = (n_corr_SR / float(n_nodes)) * 100.00


    df['SRG'] = np.where(mask, np.minimum(np.maximum(df['SRG'], min_SR), max_SR), -99)

    print('start writing sim file')
    out_file = f'9-Simulation_Orig_Units/{i_real}_end.out'
    test = io.to_Gslib(output_file=out_file, dataframe=df, float_format='%.4f')
    print('finish writing file')
    os.remove(sim_file)

    report_file = f'9-Simulation_Orig_Units/{i_real}_report_error_fraction_ratios.out'
    with open(report_file, 'w') as fout:
        fout.write('''Proportion of AA corrected (%) = {:.6f}
Proportion of SR corrected (%) = {:.6f}    \n'''.format(prop_correction_AA, prop_correction_SR))

    return None



if __name__ == '__main__':

    n_real = 40
#
#
#
    for i in range(n_real):
        i_real = i + 1
        Run_mvs_sum_check(i_real = i_real)


    df_data = io.Get_Df_From_File(file_name='1-Data/proc_data.txt')
#
    dic_grid = io.get_grid_dict('6-Grid/grid_fine_inf.txt')
    grid_size = dic_grid['nx'] * dic_grid['ny'] * dic_grid['nz']
    print(df_data['AAG'].max())
    start = time.time()

    for i in range(n_real):

        i_real = [i + 1]
        min_AA = [df_data['AAG'].min()]
        max_AA = [df_data['AAG'].max()]
        min_SR = [df_data['SRG'].min()]
        max_SR = [df_data['SRG'].max()]
        grid_size_list = [grid_size]
        zipped_params = zip(i_real, min_AA, max_AA, min_SR, max_SR, grid_size_list)

        with multiprocessing.Pool(processes = 1) as p:
            p.starmap(func=Check_Fractional_Grades, iterable=zipped_params)
        #Check_Fractional_Grades(i_real=i_real, min_AA = df_data['AA'].min(), max_AA=df_data['AA'].max(),
        #                        min_SR=df_data['SR'].min(), max_SR=df_data['SR'].max(), grid_size=grid_size)

    finish = time.time()
    print('Total time = {:.2f} seconds'.format(finish-start))








