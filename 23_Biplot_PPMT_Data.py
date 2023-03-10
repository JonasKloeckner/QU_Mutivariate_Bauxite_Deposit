
import Python_Module.io_module as io
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['mathtext.fontset'] = 'cm'
import pandas as pd
import math
from scipy.stats import gaussian_kde

def weighted_avg_and_std(values, weights):
    """
    Return the weighted average and standard deviation.

    values, weights -- Numpy ndarrays with the same shape.
    """
    average = np.average(values, weights=weights)

    variance = np.average((values-average)**2, weights=weights)  # Fast and numerically precise

    return average, math.sqrt(variance)



def Plot_Histogram(data, name):
    plt.figure(figsize=(6, 6))
    weights = np.zeros_like(data) + 1.0 / len(data)
    n, bins, patches = plt.hist(data, 20, weights=weights, facecolor='green', alpha=0.75,
                                edgecolor='k', zorder=2
                                )
    mean = np.mean(data)
    std_dev = np.std(data)

    #plt.title('Projection 2D', fontsize=15)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.xlabel(f'{name} ', fontsize=15)
    plt.ylabel('Frequency', fontsize=15)
    plt.grid(True, which='major', linestyle='--')
    ax = plt.gca()
    plt.text(x=0.10, y=0.90, s='Mean = {:.2f}\nStd. Dev = {:.2f} '.format(mean, std_dev), transform=ax.transAxes, fontsize=12)
    fig_name = f'2-EDA/Hist_PPMT/{name}.png'
    plt.savefig(fig_name, dpi=600, facecolor='w', edgecolor='w', format=None,
                transparent=False, bbox_inches='tight', pad_inches=0.1,
                frameon=None)

    plt.close()



def Plot_Histogram_decl(data, name, decl_weights, fig_name):
    plt.figure(figsize=(6, 6))

    weights = decl_weights/np.sum(decl_weights)


    n, bins, patches = plt.hist(data, 20, weights=weights, facecolor='green', alpha=0.75,
                                edgecolor='k', zorder=2
                                )

    mean, std_dev = weighted_avg_and_std(values = data, weights=decl_weights)

    #plt.title('Projection 2D', fontsize=15)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.xlabel(f'{name} ', fontsize=15)
    plt.ylabel('Frequency', fontsize=15)
    plt.xlim(-4.0, 4.0)


    plt.grid(True, which='major', linestyle='--')
    ax = plt.gca()
    plt.text(x=0.10, y=0.90, s='Mean = {:.2f}\nStd. Dev = {:.2f} '.format(mean, std_dev), transform=ax.transAxes, fontsize=12)

    plt.savefig(fig_name, dpi=600, facecolor='w', edgecolor='w', format=None,
                transparent=False, bbox_inches='tight', pad_inches=0.1,
                frameon=None)

    plt.close()

    return None





def Biplot_Data(X, Y, name_x, name_y, fig_name):





    values = np.vstack((X, Y))
    z = gaussian_kde(values)(values)

    plt.figure(figsize=(7, 6))

    plt.scatter(X, Y, c=z, vmin=np.min(z), vmax=np.max(z), cmap='seismic', alpha=0.80, s=20, rasterized=True, zorder=2)
    cbar = plt.colorbar(orientation='vertical')


    cbar.set_label('Probability density', labelpad=+10, fontsize=15)
    cbar.solids.set_edgecolor("face")
    #plt.title('Dados originais', fontsize=15)
    plt.xlabel('{name_x}'.format(**locals()), labelpad=+10, fontsize=15)
    plt.ylabel('{name_y}'.format(**locals()), labelpad=+10, fontsize=15)
    plt.xlim(-4.0, 4.0)
    plt.ylim(-4.0, 4.0)
    #plt.axis('equal')
    plt.grid(axis='both')
    ax = plt.gca()

    correlation = abs(np.corrcoef(x=X, y=Y)[0][1])
    plt.text(x=0.10, y=0.90, size=15, s=r'$\rho = {:.2f}$'.format(correlation), transform=ax.transAxes)
    #fig_name = os.path.join('6-Check_Biplot' ,'{name_x}_{name_y}.png'.format(**locals()))
    plt.savefig(fig_name, dpi=300, bbox_inches='tight', pad_inches=0.1,
                frameon=None)
    plt.close()

    return None


if __name__ == '__main__':



    names = ['weights','PPMT_1', 'PPMT_2', ]
    cols = np.array([19, 21, 22])
    data_file = '5-Ppmt/ppmt.out'
    data_array = io.get_array_gslib_pd(filename=data_file, list_of_cols=cols)

    df = pd.DataFrame(data=data_array, columns=names)


    Plot_Histogram_decl(data=df['PPMT_1'], name='PPMT_1' ,decl_weights=df['weights'], fig_name='2-EDA/Hist_ppmt/PPMT_RCG_new.png')
    Plot_Histogram_decl(data=df['PPMT_2'], name='PPMT_2' ,decl_weights=df['weights'], fig_name='2-EDA/Hist_ppmt/PPMT_ATGc_new.png')

    Biplot_Data(X=df['PPMT_1'], Y=df['PPMT_2'], name_x='PPMT_1', name_y='PPMT_2', fig_name='2-EDA/Biplot/PPMT_RCG_PPMT_ATGc.png')




