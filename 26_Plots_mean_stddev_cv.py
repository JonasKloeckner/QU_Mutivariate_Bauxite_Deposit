import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
import subprocess
import Python_Module.io_module as io
import time
import pandas as pd
import multiprocessing



#def Plot_Scatter_Mean_2017(i_var, sufix, names_x):
#
#    input_file = f'12-From_polygons/VAR_{i_var}_Mean_Of_Polygons_{sufix}_p.out'
#    df = io.Get_Df_From_File(input_file)
#    Polygon_ID = df['Polygon_ID']
#    E_Type_Polygons = df['E_Type_Polygons']
#    plt.xlabel('Polygon ID')
#    plt.ylabel('EType Polygons')
#    plt.title('{names_x} (%)'.format(**locals()))
#    #'EType from Polygons Variable {}'format(i) for i in names[i])
#
#
#    colors = np.where(df["Polygon_ID"]%2==0,'g','r')
#    groups = ('Unwashed')
#
#    plt.xlim(2017000, 2017125)
#
#    ax = plt.gca()
#    ax.legend(groups)   
#    ax.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x))))
#
#    plt.scatter(Polygon_ID, E_Type_Polygons, c=colors, alpha=0.80, rasterized=True, zorder=2, marker='o', label=groups)
#    plt.legend(fontsize=12)
#    plt.grid(axis='both', linestyle='--')
#    fig_name_2017 = f'12-From_polygons/Hist_Sim/VAR_{i_var}_{names_x}_Mean_Of_Polygons_{sufix}_2017.png'
#    plt.savefig(fig_name_2017, dpi=500, bbox_inches='tight', pad_inches=0.1, frameon=None)
#
#    plt.close()
#     
#
#    return None

def Plot_Scatter_Mean_2017(i_var, sufix):

    input_file = f'12-From_polygons/VAR_{i_var}_Mean_Of_Polygons_{sufix}_p.out'
    df = io.Get_Df_From_File(input_file)
    Polygon_ID = df['Polygon_ID']
    E_Type_Polygons = df['E_Type_Polygons']
    plt.xlabel('Polygon ID')
    plt.ylabel('EType Polygons')
    plt.title('EType from Polygons Variable ')

    colors = np.where(df["Polygon_ID"]%2==0,'g','r')
    groups = ('Unwashed')

    plt.xlim(2017000, 2017125)

    ax = plt.gca()
    ax.legend(groups)   
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x))))

    plt.scatter(Polygon_ID, E_Type_Polygons, c=colors, alpha=0.80, rasterized=True, zorder=2, marker='o', label=groups)
    plt.legend(fontsize=12)
    plt.grid(axis='both', linestyle='--')
    fig_name_2017 = f'12-From_polygons/Hist_Sim/VAR_{i_var}_Mean_Of_Polygons_{sufix}_2017.png'
    plt.savefig(fig_name_2017, dpi=500, bbox_inches='tight', pad_inches=0.1, frameon=None)

    plt.close()
     

    return None

def Plot_Scatter_Mean_2018(i_var, sufix):

    input_file = f'12-From_polygons/VAR_{i_var}_Mean_Of_Polygons_{sufix}_p.out'
    df = io.Get_Df_From_File(input_file)
    Polygon_ID = df['Polygon_ID']
    E_Type_Polygons = df['E_Type_Polygons']
    plt.xlabel('Polygon ID')
    plt.ylabel('EType Polygons')
    plt.title('EType from Polygons Variable ')

    colors = np.where(df["Polygon_ID"]%2==0,'g','r')
    groups = ('Unwashed')

    plt.xlim(2018000, 2018125)

    ax = plt.gca()
    ax.legend(groups)   
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x))))

    plt.scatter(Polygon_ID, E_Type_Polygons, c=colors, alpha=0.80, rasterized=True, zorder=2, marker='o', label=groups)
    plt.legend(fontsize=12)
    plt.grid(axis='both', linestyle='--')
    fig_name_2018 = f'12-From_polygons/Hist_Sim/VAR_{i_var}_Mean_Of_Polygons_{sufix}_2018.png'
    plt.savefig(fig_name_2018, dpi=500, bbox_inches='tight', pad_inches=0.1, frameon=None)

    plt.close()
     

    return None


def Plot_Scatter_Std_2017(i_var, sufix):

    input_file = f'12-From_polygons/VAR_{i_var}_Mean_Of_Polygons_{sufix}_p.out'
    df = io.Get_Df_From_File(input_file)
    Polygon_ID = df['Polygon_ID']
    E_Type_Polygons = df['Std_Dev_Polygons']
    plt.xlabel('Polygon ID')
    plt.ylabel('Std Dev Polygons')
    plt.title('Std Dev from Polygons Variable ')

    colors = np.where(df["Polygon_ID"]%2==0,'g','r')
    groups = ('Unwashed')

    plt.xlim(2017000, 2017125)
#    plt.ylim(-1, 1)

    ax = plt.gca()
    ax.legend(groups)
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x))))

    plt.scatter(Polygon_ID, E_Type_Polygons,c=colors, alpha=0.80, rasterized=True, zorder=2, marker='o', label=groups)
    plt.legend(fontsize=12)
    plt.grid(axis='both', linestyle='--')
    fig_name_2017 = f'12-From_polygons/Hist_Sim/VAR_{i_var}_Std_Of_Polygons_{sufix}_2017.png'
    plt.savefig(fig_name_2017, dpi=500, bbox_inches='tight', pad_inches=0.1, frameon=None)

    plt.close()
     

    return None

def Plot_Scatter_Std_2018(i_var, sufix):

    input_file = f'12-From_polygons/VAR_{i_var}_Mean_Of_Polygons_{sufix}_p.out'
    df = io.Get_Df_From_File(input_file)
    Polygon_ID = df['Polygon_ID']
    E_Type_Polygons = df['Std_Dev_Polygons']
    plt.xlabel('Polygon ID')
    plt.ylabel('Std Dev Polygons')
    plt.title('Std Dev from Polygons Variable ')

    colors = np.where(df["Polygon_ID"]%2==0,'g','r')
    groups = ('Unwashed')

    plt.xlim(2018000, 2018125)
#    plt.ylim(-1, 1)

    ax = plt.gca()
    ax.legend(groups)
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x))))

    plt.scatter(Polygon_ID, E_Type_Polygons, c=colors, alpha=0.80, rasterized=True, zorder=2, marker='o', label=groups)
    plt.legend(fontsize=12)
    plt.grid(axis='both', linestyle='--')
    fig_name_2018 = f'12-From_polygons/Hist_Sim/VAR_{i_var}_Std_Of_Polygons_{sufix}_2018.png'
    plt.savefig(fig_name_2018, dpi=500, bbox_inches='tight', pad_inches=0.1, frameon=None)

    plt.close()
     

    return None

def Plot_CV_2017(i_var, sufix):

    input_file = f'12-From_polygons/VAR_{i_var}_Mean_Of_Polygons_{sufix}_p.out'
    df = io.Get_Df_From_File(input_file)
    Polygon_ID = df['Polygon_ID']
    E_Type_Polygons = df['Coeffient_Variation']
    plt.xlabel('Polygon ID')
    plt.ylabel('CV from Polygons')
    plt.title('CV from Variable ')

    colors = np.where(df["Polygon_ID"]%2==0,'g','r')
    groups = ('Unwashed')

    plt.xlim(2017000, 2017125)
#    plt.ylim(-1, 1)

    ax = plt.gca()
    ax.legend(groups)
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x))))

    plt.scatter(Polygon_ID, E_Type_Polygons, c=colors, alpha=0.80, rasterized=True, zorder=2, marker='o', label=groups)
    plt.legend(fontsize=12)
    plt.grid(axis='both', linestyle='--')
    fig_name_2017 = f'12-From_polygons/Hist_Sim/VAR_{i_var}_CV_Polygons_{sufix}_2017.png'
    plt.savefig(fig_name_2017, dpi=500, bbox_inches='tight', pad_inches=0.1, frameon=None)

    plt.close()
     

    return None

def Plot_CV_2018(i_var, sufix):

    input_file = f'12-From_polygons/VAR_{i_var}_Mean_Of_Polygons_{sufix}_p.out'
    df = io.Get_Df_From_File(input_file)
    Polygon_ID = df['Polygon_ID']
    E_Type_Polygons = df['Coeffient_Variation']
    plt.xlabel('Polygon ID')
    plt.ylabel('CV from Polygons')
    plt.title('CV from Variable ')

    colors = np.where(df["Polygon_ID"]%2==0,'g','r')
    groups = ('Unwashed')

    plt.xlim(2018000, 2018125)
#    plt.ylim(-1, 1)

    ax = plt.gca()
    ax.legend(groups)
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x))))

    plt.scatter(Polygon_ID, E_Type_Polygons, c=colors, alpha=0.80, rasterized=True, zorder=2, marker='o', label=groups)
    plt.legend(fontsize=12)
    plt.grid(axis='both', linestyle='--')
    fig_name_2018 = f'12-From_polygons/Hist_Sim/VAR_{i_var}_CV_Polygons_{sufix}_2018.png'
    plt.savefig(fig_name_2018, dpi=500, bbox_inches='tight', pad_inches=0.1, frameon=None)

    plt.close()
     

    return None

#def Probability_AA_above_cutoff(n_real):
#	
#    input_file_AA = f'12-From_polygons/VAR_7_Mean_Of_Polygons_end_p.out'
#    
#    cutoff_AA = 47.43
#
##    df = io.Get_Df_From_File(input_file_AA)
#    
#
#    for i in range(n_real):
#    	i_real = i + 1
#    	names = ['Real_{}_Polygon'.format(i_real)]
#    	df_out = pd.DataFrame(data=input_file_AA, columns = names)
#    	df_out['lista_probs'] = [np.where(df_out[names]>cutoff_AA,1.0,0.0)]
#    	print(lista_probs)
##    	array_probs = np.array(lista_probs)
##    	mean_prob = array_probs.mean(axis=1)
##    	print(mean_prob)
#
#
#    out_file_AA = f'12-From_polygons/VAR_AA_Probability_above_cutoff.out'
#    
#    test_AA = io.to_Gslib(output_file=out_file_AA, dataframe=df_out, float_format='%.4f')
#
#    return None
#
#def Probability_SR_above_cutoff(n_real):
#	
#    input_file_SR = f'12-From_polygons/VAR_8_Mean_Of_Polygons_end_p.out'
#    
#    cutoff_SR = 4.15
#
#    names = ['Real_{}_Polygon'.format(i) for i in range(1, n_real + 1)]
#    array_mean_values = np.zeros((n_real))
#    df_out = pd.DataFrame(data=array_mean_values, columns = names)
#
#    df_out['Probability_SR_above_cutoff'] = [np.where(df_out[names]>cutoff_SR,1,0)].mean()
#
#    out_file_SR = f'12-From_polygons/VAR_SR_Probability_above_cutoff.out'
#    
#    test_SR = io.to_Gslib(output_file=out_file_SR, dataframe=df_out, float_format='%.4f')
#
#    return None


if __name__ == '__main__':


    start = time.time()

    dic_grid = io.get_grid_dict('6-Grid/grid_fine_inf.txt')
    grid_size = dic_grid['nx'] * dic_grid['ny'] * dic_grid['nz']
    n_real = 40
    sufix = 'end'
    names= ['RCG', 'ATGc', 'STGc', 'FEGc', 'TIGc', 'PPGc', 'AAG', 'SRG']
    i_var = len(names)
    i_real_list = np.arange(1, n_real + 1)
    
    polygons = [2017010, 2017020, 2017030, 2017040, 2017050, 2017060, 2017070, 2017080, 2017090, 2017100, 2017110, 2017120,
    			2017011, 2017021, 2017031, 2017041, 2017051, 2017061, 2017071, 2017081, 2017091, 2017101, 2017111, 2017121,
    			2018010, 2018020, 2018030, 2018040, 2018050, 2018060, 2018070, 2018080, 2018090, 2018100, 2018110, 2018120,
    			2018011, 2018021, 2018031, 2018041, 2018051, 2018061, 2018071, 2018081, 2018091, 2018101, 2018111, 2018121]


   for i in range(n_real):
       i_real = i + 1	
       get_etype_polygons(n_real, polygons, sufix)

    for i in range(n_real):
        i_real = i + 1
        Probability_AA_above_cutoff(n_real)

    for i in range(n_real):
        i_real = i + 1
        Probability_SR_above_cutoff(n_real)

#   for i in range(i_var):
#       names_x = names[i]
#       print(f'{names_x}')
#       Plot_Scatter_Mean_2017(i_var=i_var, sufix=sufix, names_x=names_x)

   for i in range(i_var):
       i_var = i + 1
       Plot_Scatter_Mean_2017(i_var, sufix)

   for i in range(i_var):
       i_var = i + 1
       Plot_Scatter_Mean_2018(i_var, sufix)

   for i in range(i_var):
       i_var = i + 1
       Plot_Scatter_Std_2017(i_var, sufix)

   for i in range(i_var):
       i_var = i + 1
       Plot_Scatter_Std_2018(i_var, sufix)

   for i in range(i_var):
       i_var = i + 1
       Plot_CV_2017(i_var, sufix)

   for i in range(i_var):
       i_var = i + 1
       Plot_CV_2018(i_var, sufix)
