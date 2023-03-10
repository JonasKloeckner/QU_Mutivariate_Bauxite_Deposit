

import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import Python_Module.io_module as io

import numpy as np

import time



def Biplot_Data(X, Y, name_x, name_y, fig_name):
    values = np.vstack((X, Y))
    z = gaussian_kde(values)(values)

    plt.figure(figsize=(8, 6))

    plt.scatter(X, Y, c=z, vmin=np.min(z), vmax=np.max(z), cmap='seismic', alpha=0.80, s=20, rasterized=True, zorder=2)
    cbar = plt.colorbar()


    cbar.set_label('Probability density', labelpad=+10, fontsize=15)
    cbar.solids.set_edgecolor("face")
    plt.title('Data', fontsize=15)
    plt.xlabel('{name_x} (%)'.format(**locals()), labelpad=+10, fontsize=15)
    plt.ylabel('{name_y} (%)'.format(**locals()), labelpad=+10, fontsize=15)
    ylim = plt.ylim()
    xlim = plt.xlim()
    plt.grid(axis='both')

    plt.savefig(fig_name, dpi=300, bbox_inches='tight', pad_inches=0.1,
                frameon=None)
    plt.close()

    return np.min(z), np.max(z), xlim, ylim



def Biplot_Simulation(X, name_x, Y, name_y, n_points, vmin, vmax, xlim, ylim, fig_name, sim_name):

    # filter values


    x_f = X[X > -97.00]
    y_f = Y[Y > -97.00]

    print(y_f.shape)

    np.random.seed(69069)
    index_sample = np.random.choice(a= np.arange(len(x_f)), size=n_points, replace=False)

    x_sample = x_f[index_sample]
    y_sample = y_f[index_sample]



    values = np.vstack((x_sample, y_sample))
    z =gaussian_kde(values)(values)


    plt.figure(figsize=(8,6))
    plt.grid(axis='both')
    plt.scatter(x_sample, y_sample, c=z, vmin=vmin, vmax=vmax,cmap='seismic',  alpha= 0.80, s=20, zorder=2 )
    plt.xlim(xlim)
    plt.ylim(ylim)
    cbar = plt.colorbar()


    cbar.set_label('Probability density', labelpad=+10, fontsize=15)
    cbar.solids.set_edgecolor("face")
    plt.title(sim_name, fontsize=15)
    plt.xlabel('{name_x} (%)'.format(**locals()),labelpad=+10, fontsize=15)
    plt.ylabel('{name_y} (%)'.format(**locals()),labelpad=+10, fontsize=15)


    plt.savefig(fig_name, dpi=300, bbox_inches='tight', pad_inches=0.1,
        frameon=None)
    plt.close()
    return None



if __name__ == '__main__':


    n_nodes_f = 5531184
    start = time.time()

    data_file = '1-Data/proc_data.txt'
    df_data = io.Get_Df_From_File(file_name = data_file)


    sim_file = '9-Simulation_Orig_Units/1_end_f.out'

    names= ['RCG', 'ATGc', 'STGc', 'FEGc', 'TIGc', 'PPGc', 'AAG', 'SRG']
    n_var = len(names)
    df_sim = io.Get_Df_From_Sim_File(file_name=sim_file, grid_size=n_nodes_f)
    df_sim.columns = names



    for i in range(n_var):

        for j in range(i+1, n_var):

            name_x = names[i]
            name_y = names[j]

            print(f'{name_x} {name_y}')

            X = df_data[name_x]
            Y = df_data[name_y]


            fig_name = f'10-Validation/Biplot/{name_x}_{name_y}_data.png'
            vmin, vmax, xlim, ylim = Biplot_Data(X=X, Y=Y, name_x=name_x, name_y= name_y, fig_name=fig_name)


            fig_name = f'10-Validation/Biplot/{name_x}_{name_y}_sim.png'

            X_sim = df_sim[name_x].values
            Y_sim = df_sim[name_y].values

            Biplot_Simulation(X=X_sim, name_x=name_x, Y=Y_sim, name_y=name_y, n_points=5000,
                              vmin=vmin, vmax=vmax, xlim=xlim, ylim=ylim,
                              fig_name=fig_name, sim_name= 'Realization 1')



    finish = time.time()

    print('Total time = {:.2f} seconds'.format(finish-start))