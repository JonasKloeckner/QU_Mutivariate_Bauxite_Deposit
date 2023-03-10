
import Python_Module.io_module as io

import matplotlib.pyplot as plt
import numpy as np

import math

def weighted_avg_and_std(values, weights):
    """
    Return the weighted average and standard deviation.

    values, weights -- Numpy ndarrays with the same shape.
    """
    average = np.average(values, weights=weights)
    variance = np.average((values-average)**2, weights=weights)  # Fast and numerically precise
    return average, math.sqrt(variance)


def Plot_Histogram(data, name, fig_name):
    plt.figure(figsize=(6, 6))
    weights = np.zeros_like(data) + 1.0 / len(data)
    n, bins, patches = plt.hist(data, 20, weights=weights, facecolor='green', alpha=0.75,
                                edgecolor='k', zorder=2
                                )
    mean = np.mean(data)
    std_dev = np.std(data)

    # plt.title('Projection 2D', fontsize=15)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.xlabel(f'{name} (%)', fontsize=15)
    plt.ylabel('Frequency', fontsize=15)
    plt.xlim(np.min(data), np.max(data))
    plt.grid(True, which='major', linestyle='--')
    ax = plt.gca()
    plt.text(x=0.10, y=0.85, s='Mean = {:.2f}\nStd. Dev = {:.2f}'.format(mean, std_dev), transform=ax.transAxes,
             fontsize=15)

    plt.savefig(fig_name, dpi=600, facecolor='w', edgecolor='w', format=None,
                transparent=False, bbox_inches='tight', pad_inches=0.1,
                frameon=None)

    plt.close()
    return None


def Plot_Histogram_decl(data, name, decl_weights, fig_name):
    plt.figure(figsize=(6, 6))

    weights = decl_weights / np.sum(decl_weights)

    n, bins, patches = plt.hist(data, 20, weights=weights, facecolor='green', alpha=0.75,
                                edgecolor='k', zorder=2
                                )

    mean, std_dev = weighted_avg_and_std(values=data, weights=decl_weights)

    # plt.title('Projection 2D', fontsize=15)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.xlabel(f'{name} (%)', fontsize=15)
    plt.ylabel('Frequency', fontsize=15)
    plt.grid(True, which='major', linestyle='--')
    ax = plt.gca()
    plt.text(x=0.10, y=0.85, s='Mean = {:.2f}\nStd. Dev = {:.2f}'.format(mean, std_dev), transform=ax.transAxes,
             fontsize=15)

    plt.savefig(fig_name, dpi=600, facecolor='w', edgecolor='w', format=None,
                transparent=False, bbox_inches='tight', pad_inches=0.1,
                frameon=None)

    plt.close()
    return None




if __name__ == '__main__':

    data_file = '1-Data/proc_data.txt'
    names = ['RCG', 'ATGc', 'AAG', 'STGc', 'SRG', 'FEGc', 'TIGc', 'PPGc']
    cols = io.get_columns_from_names(filename=data_file, names=names)

    df = io.Get_Df_From_File(data_file)
    print(df.columns.values)

    df_orig = df[names]
    df_summary = df_orig.describe()
    out_file = '2-EDA/orig_summary_statistics.csv'
    df_summary.to_csv(out_file, header=True, float_format='%.4f')



    corr_data = df_orig.corr()
    plt.figure(figsize=(6, 6))
    plt.matshow(A=corr_data, cmap='seismic', vmin=-1, vmax=1.0)
    plt.xticks(np.arange(corr_data.shape[0]), names, fontsize=12)
    plt.yticks(np.arange(corr_data.shape[1]), names, fontsize=12)
    cbar = plt.colorbar()
    cbar.set_label('Correlation', fontsize=12)

    fig_name = '2-EDA/Corrmat/corrmat_orig.png'
    plt.savefig(fig_name, dpi=500, bbox_inches='tight', pad_inches=0.1,
                frameon=None)

    plt.close()


    var = ['ATGc','STGc', 'FEGc', 'TIGc', 'PPGc', 'A1', 'A2', 'A3', 'A4']

    names_histplt = ['RCG','ATGc', 'AAG','STGc', 'SRG', 'FEGc', 'TIGc', 'PPGc', 'A1', 'A2', 'A3', 'A4', 'FR_AAG', 'FR_SRG']
    cols_histplt = io.get_columns_from_names(data_file, names_histplt)

    df_var = df[var]
    print(df_var.corr())

    mean_list = []
    weighted_mean = []

    for i in range(len(names_histplt)):

        name = names_histplt[i]

        fig_name = f'2-EDA/Hist/{name}_decl.png'
        Plot_Histogram_decl(data = df[name], name=name, decl_weights=df['DECLUS_W'], fig_name=fig_name)

        fig_name = f'2-EDA/Hist/{name}.png'
        Plot_Histogram(data=df[name], name=name, fig_name=fig_name)

        if(i < 7):

            print(name, df[name].mean(), np.average(df[name], weights=df['DECLUS_W']))




