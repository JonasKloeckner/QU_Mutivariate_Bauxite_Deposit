import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
import subprocess
import Python_Module.io_module as io
import time
import pandas as pd
import multiprocessing
import IPython
import seaborn as sns



def Box_Plot_AAG(n_real, polygons, sufix):

    polygons_used = []
    for i in range(len(polygons)):
        polygon_ID = str(polygons[i])
        if(sufix=='washed'):
            if(polygon_ID.endswith('1')):
                polygons_used.append(polygons[i])
        if(sufix=='unwashed'):
            if(polygon_ID.endswith('0')):
                polygons_used.append(polygons[i])

    input_file_real = f'12-From_polygons/VAR_7_Mean_Of_Polygons_end_p.out'
    df_all_data = io.Get_Df_From_File(input_file_real)
    df_f = df_all_data[df_all_data['Polygon_ID'].isin(polygons_used)]

    names = ['Real_{}_Polygon'.format(i) for i in range(1, n_real + 1)]
    df_real = df_f[names]

    input_file_actual = f'12-From_polygons/Alcoa_measured/AAG_Actual.txt'
    df_actual = io.Get_Df_From_File(input_file_actual)
    df_actual_f =  df_actual[ df_actual['Polygon_ID'].isin(polygons_used)]

    Polygon_ID_actual = df_actual_f['Polygon_ID']
    Actual_Mean = df_actual_f['Actual_Mean']
    Kriged_Mean = df_actual_f['Kriged_Mean']

    len_poly = len(polygons_used)
    #IPython.embed()
    box_plot_data = df_real.values
    print(len(df_real), len(polygons_used))
    plt.boxplot(box_plot_data.T,patch_artist=True,labels=polygons_used, zorder=1, whis='range')
    plt.scatter(range(1, len_poly + 1), Actual_Mean, marker='o', c='#2ca02c', label='AAG Measured', zorder=3)
    plt.scatter(range(1, len_poly + 1), Kriged_Mean, marker='o', c='#17becf', label='Kriged_Mean', zorder=2)
    plt.legend(frameon=False, loc='best')
    plt.xticks(rotation = 90)


    fig_name_AAG = f'12-From_polygons/Box_Plot_Sim/Box_Plot_AAG_{sufix}.png'
    plt.savefig(fig_name_AAG, dpi=600, bbox_inches='tight', pad_inches=0.1, frameon=False)

    plt.close()
     

    return None


def Box_Plot_SRG(n_real, polygons, sufix):

    polygons_used = []
    for i in range(len(polygons)):
        polygon_ID = str(polygons[i])
        if(sufix=='washed'):
            if(polygon_ID.endswith('1')):
                polygons_used.append(polygons[i])
        if(sufix=='unwashed'):
            if(polygon_ID.endswith('0')):
                polygons_used.append(polygons[i])

    input_file_real = f'12-From_polygons/VAR_8_Mean_Of_Polygons_end_p.out'
    df_all_data = io.Get_Df_From_File(input_file_real)
    df_f = df_all_data[df_all_data['Polygon_ID'].isin(polygons_used)]

    names = ['Real_{}_Polygon'.format(i) for i in range(1, n_real + 1)]
    df_real = df_f[names]

    input_file_actual = f'12-From_polygons/Alcoa_measured/SRG_Actual.txt'
    df_actual = io.Get_Df_From_File(input_file_actual)
    df_actual_f =  df_actual[ df_actual['Polygon_ID'].isin(polygons_used)]

    Polygon_ID_actual = df_actual_f['Polygon_ID']
    Actual_Mean = df_actual_f['Actual_Mean']
    Kriged_Mean = df_actual_f['Kriged_Mean']

    len_poly = len(polygons_used)
    #IPython.embed()
    box_plot_data = df_real.values
    print(len(df_real), len(polygons_used))
    plt.boxplot(box_plot_data.T,patch_artist=True,labels=polygons_used, zorder=1, whis='range')
    plt.scatter(range(1, len_poly + 1), Actual_Mean, marker='o', c='#2ca02c', label='AAG Measured', zorder=3)
    plt.scatter(range(1, len_poly + 1), Kriged_Mean, marker='o', c='#17becf', label='Kriged_Mean', zorder=2)
    plt.legend(frameon=False, loc='best')
    plt.xticks(rotation = 90)


    fig_name_SRG = f'12-From_polygons/Box_Plot_Sim/Box_Plot_SRG_{sufix}.png'
    plt.savefig(fig_name_SRG, dpi=600, bbox_inches='tight', pad_inches=0.1, frameon=False)

    plt.close()
     

    return None

def Box_Plot_RCG(n_real, polygons, sufix):

    polygons_used = []
    for i in range(len(polygons)):
        polygon_ID = str(polygons[i])
        if(sufix=='washed'):
            if(polygon_ID.endswith('1')):
                polygons_used.append(polygons[i])
        if(sufix=='unwashed'):
            if(polygon_ID.endswith('0')):
                polygons_used.append(polygons[i])

    input_file_real = f'12-From_polygons/VAR_1_Mean_Of_Polygons_end_p.out'
    df_all_data = io.Get_Df_From_File(input_file_real)
    df_f = df_all_data[df_all_data['Polygon_ID'].isin(polygons_used)]

    names = ['Real_{}_Polygon'.format(i) for i in range(1, n_real + 1)]
    df_real = df_f[names]

    input_file_actual = f'12-From_polygons/Alcoa_measured/RCG_Actual.txt'
    df_actual = io.Get_Df_From_File(input_file_actual)
    df_actual_f =  df_actual[ df_actual['Polygon_ID'].isin(polygons_used)]

    Polygon_ID_actual = df_actual_f['Polygon_ID']
    Actual_Mean = df_actual_f['Actual_Mean']
    Kriged_Mean = df_actual_f['Kriged_Mean']

    len_poly = len(polygons_used)
    #IPython.embed()
    box_plot_data = df_real.values
    print(len(df_real), len(polygons_used))
    plt.boxplot(box_plot_data.T,patch_artist=True,labels=polygons_used, zorder=1, whis='range')
    plt.scatter(range(1, len_poly + 1), Actual_Mean, marker='o', c='#2ca02c', label='AAG Measured', zorder=3)
    plt.scatter(range(1, len_poly + 1), Kriged_Mean, marker='o', c='#17becf', label='Kriged_Mean', zorder=2)
    plt.legend(frameon=False, loc='best')
    plt.xticks(rotation = 90)


    fig_name_RCG = f'12-From_polygons/Box_Plot_Sim/Box_Plot_RCG_{sufix}.png'
    plt.savefig(fig_name_RCG, dpi=600, bbox_inches='tight', pad_inches=0.1, frameon=False)

    plt.close()
     

    return None

if __name__ == '__main__':


    start = time.time()

    n_real = 40

    names= ['RCG', 'ATGc', 'STGc', 'FEGc', 'TIGc', 'PPGc', 'AAG', 'SRG']
    i_var = len(names)

    polygons = [2017010, 2017020, 2017030, 2017040, 2017050, 2017060, 2017070, 2017080, 2017090, 2017100, 2017110, 2017120,
                2017011, 2017021, 2017031, 2017041, 2017051, 2017061, 2017071, 2017081, 2017091, 2017101, 2017111, 2017121,
                2018010, 2018020, 2018030, 2018040, 2018050, 2018060, 2018070, 2018080, 2018090, 2018100, 2018110,
                2018011, 2018021, 2018031, 2018041, 2018051, 2018061, 2018071, 2018081, 2018091, 2018101, 2018111, 2018121]

    polygons_washed = [2017011, 2017021, 2017031, 2017041, 2017051, 2017061, 2017071, 2017081, 2017091, 2017101, 2017111, 2017121,
        2018011, 2018021, 2018031, 2018041, 2018051, 2018061, 2018071, 2018081, 2018091, 2018101, 2018111, 2018121
    ]

    polygons_unwashed = [2017010, 2017020, 2017030, 2017040, 2017050, 2017060, 2017070, 2017080, 2017090, 2017100, 2017110, 2017120,
        2018010, 2018020, 2018030, 2018040, 2018050, 2018060, 2018070, 2018080, 2018090, 2018100, 2018110, 2018120
    ]
    
    list_of_sufixes = ['washed', 'unwashed']
    for sufix in list_of_sufixes:
        Box_Plot_AAG(n_real, polygons, sufix)

    list_of_sufixes = ['washed', 'unwashed']
    for sufix in list_of_sufixes:
        Box_Plot_SRG(n_real, polygons, sufix)

    list_of_sufixes = ['washed', 'unwashed']
    for sufix in list_of_sufixes:
        Box_Plot_RCG(n_real, polygons, sufix)