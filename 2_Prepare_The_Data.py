

import Python_Module.io_module as io
import numpy as np


if __name__ == '__main__':

    EPSON = 0.001
    np.random.seed(69069)

    data_file = '1-Data/declus_3D.out'

    df = io.Get_Df_From_File(data_file)
    print(df.columns)

    n_data = df.shape[0]

    df['CLOSURE'] = 100.00
    df['SUM'] = df['ATG'] + df['STG'] + df['FEG'] + df['TIG'] + df['PPG']
    df['DIFFERENCE'] = df['CLOSURE'] - df['SUM']

    df['ATGc'] = df['ATG'] + (df['DIFFERENCE']*(df['ATG']/df['SUM']))
    df['STGc'] = df['STG'] + (df['DIFFERENCE']*(df['STG']/df['SUM']))
    df['FEGc'] = df['FEG'] + (df['DIFFERENCE']*(df['FEG']/df['SUM']))
    df['TIGc'] = df['TIG'] + (df['DIFFERENCE']*(df['TIG']/df['SUM']))
    df['PPGc'] = df['CLOSURE'] - df['ATGc'] - df['STGc'] - df['FEGc'] - df['TIGc']

    df['Random_EPSON'] = np.random.uniform(0.01, 0.99, n_data)*EPSON
    print(df['Random_EPSON'].min(), )

    df['AAG'] = np.where(df['AAG'] > df['ATGc'], df['ATGc'] - df['Random_EPSON'], df['AAG'])
    df['SRG'] = np.where(df['SRG'] > df['STGc'], df['STGc'] - df['Random_EPSON'], df['SRG'])

    df['A1'] = df['ATGc'] /  df['PPGc']
    df['A2'] = df['STGc'] /  df['PPGc']
    df['A3'] = df['FEGc'] /  df['PPGc']
    df['A4'] = df['TIGc'] /  df['PPGc']


    df['FR_AAG'] = df['AAG']/df['ATGc']
    df['FR_SRG'] = df['SRG']/df['STGc']

    df['ROCK'] = 1
    df['DECLUS_W'] = df['Decl_w']



    var_to_keep = ['BHID', 'X', 'Y', 'Z_STRAT_TOP', 'RCG', 
                   'ATGc', 'AAG', 'STGc', 'SRG', 'FEGc', 'TIGc', 'PPGc',
                   'A1', 'A2', 'A3', 'A4', 'FR_AAG', 'FR_SRG',
                   'DECLUS_W', 'ROCK']

    df_out = df[var_to_keep]


    out_file = '1-Data/proc_data.txt'
    test = io.to_Gslib(output_file= out_file, dataframe=df_out, float_format='%.10f')

    out_file = '1-Data/proc_data.csv'
    df_out.to_csv(out_file, index=False)
