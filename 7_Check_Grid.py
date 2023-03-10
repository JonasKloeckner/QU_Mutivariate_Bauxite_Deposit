

import pandas as pd
import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import Python_Module.io_module as io
from scipy.spatial import KDTree


def Plot_Estimates(name, x_data, y_data,  estimates, dict_grid):

    xo = dict_grid['xo']
    yo = dict_grid['yo']
    nx = dict_grid['nx']
    ny = dict_grid['ny']
    xsize = dict_grid['x_size']
    ysize = dict_grid['y_size']

    array_map = np.reshape(estimates, newshape=(ny, nx))

    # END OF GRID DEFINITION
    xmin = xo - xsize / 2.00
    ymin = yo - ysize / 2.00
    x_grid = [xmin + i * xsize for i in range(nx + 1)]
    y_grid = [ymin + i * ysize for i in range(ny + 1)]
    xx, yy = np.meshgrid(x_grid, y_grid)

    plt.figure()


    plt.pcolormesh(xx, yy, array_map, cmap='jet', alpha=0.50)

    ax = plt.gca()
    ax.set_aspect('equal')
    #cbar = plt.colorbar(orientation='horizontal')
    #cbar.set_label(f'{name} (m)')
    plt.title(f'{name}')
    plt.scatter(x_data, y_data,s=3, c='k', zorder=2)
    plt.xlabel('X (m)')
    plt.ylabel('Y (m)')
    #plt.xlim(np.min(x_grid), np.max(x_grid))
    #plt.ylim(np.min(y_grid), np.max(y_grid))
    fig_name = f'11-Estimates/{name}.png'
    plt.savefig(fig_name, dpi=300, facecolor='w', edgecolor='w',
                orientation='portrait', papertype=None, format=None,
                transparent=False, bbox_inches='tight', pad_inches=0.1,
                frameon=None)
    plt.close()



def downscale_grid(dict_grid_coarse, x_disc, y_disc, z_disc):
    dict_grid_fine = {}

    xo = dict_grid_coarse['xo']
    yo = dict_grid_coarse['yo']
    zo = dict_grid_coarse['zo']

    nx = dict_grid_coarse['nx']
    ny = dict_grid_coarse['ny']
    nz = dict_grid_coarse['nz']

    x_size = dict_grid_coarse['x_size']
    y_size = dict_grid_coarse['y_size']
    z_size = dict_grid_coarse['z_size']

    x_size_sim = x_size/x_disc
    xo_sim = xo - (x_size/2.0) + (x_size_sim/2.0)
    nx_sim = nx*x_disc

    dict_grid_fine['xo'] = xo_sim
    dict_grid_fine['nx'] = nx_sim
    dict_grid_fine['x_size'] = x_size_sim

    y_size_sim = y_size / y_disc
    yo_sim = yo - (y_size / 2.0) + (y_size_sim / 2.0)
    ny_sim = ny * y_disc

    dict_grid_fine['yo'] = yo_sim
    dict_grid_fine['ny'] = ny_sim
    dict_grid_fine['y_size'] = y_size_sim

    z_size_sim = z_size / z_disc
    zo_sim = zo - (z_size / 2.0) + (z_size_sim / 2.0)
    nz_sim = nz * z_disc

    dict_grid_fine['zo'] = zo_sim
    dict_grid_fine['nz'] = nz_sim
    dict_grid_fine['z_size'] = z_size_sim

    return dict_grid_fine


if __name__ == '__main__':


    df_data = io.Get_Df_From_File('1-Data/proc_data.txt')
    print(df_data.columns)

    x_disc, y_disc, z_disc = 4, 4, 1

    x_size, y_size, z_size = 25.0, 25.0, 1.0
    xo_data = df_data['X'].min()
    x_max_data = df_data['X'].max()
    yo_data = df_data['Y'].min()
    y_max_data = df_data['Y'].max()


    centroids_file = '6-Grid/centroids_bx_2D.csv'
    df = pd.read_csv(centroids_file)
    n_points = df.shape[0]

    grid_points = np.zeros(shape=(n_points,1))

    grid_points[:, 0] = df['X'].values
    kdtree = KDTree(grid_points)
    dist, index_nearest = kdtree.query(x=[xo_data], k=1)
    xo_grid = grid_points[index_nearest,:][0]
    while(xo_grid > xo_data):
        xo_grid = xo_grid - x_size
    print(xo_grid,xo_data)

    dist, index_nearest = kdtree.query(x=[x_max_data], k=1)
    xend_grid = grid_points[index_nearest, :][0]
    while (xend_grid < xo_data):
        xend_grid = xend_grid + x_size
        print('test')
    print(xend_grid, x_max_data)

    nx = int((xend_grid - xo_grid)/x_size) + 1
    print(nx)

    grid_points[:, 0] = df['Y'].values
    kdtree = KDTree(grid_points)
    dist, indey_nearest = kdtree.query(x=[yo_data], k=1)
    yo_grid = grid_points[indey_nearest, :][0]
    while (yo_grid > yo_data):
        yo_grid = yo_grid - y_size
    print(yo_grid, xo_data)

    dist, indey_nearest = kdtree.query(x=[y_max_data], k=1)
    yend_grid = grid_points[indey_nearest, :][0]
    while (yend_grid < yo_data):
        yend_grid = yend_grid + y_size
        print('test')
    print(yend_grid, y_max_data)

    ny = int((yend_grid - yo_grid) / y_size) + 1
    print(ny)

    zo_grid = -8.25
    nz = 17
    z_size = 0.50

    dict_grid_coarse = {'xo': xo_grid, 'nx': nx, 'x_size':x_size,
                        'yo': yo_grid, 'ny': ny, 'y_size': y_size,
                        'zo': zo_grid, 'nz': nz, 'z_size': z_size}

    grid_coarse_file = '6-Grid/grid_coarse_inf.txt'
    with open(grid_coarse_file, 'w') as f:
        f.write('''{nx}   {xo}    {x_size}                  -nx,xmn,xsiz
{ny}   {yo}   {y_size}                  -ny,ymn,ysiz
{nz}    {zo}    {z_size}                  -nz,zmn,zsiz    '''.format(**dict_grid_coarse))

    dict_grid_fine = downscale_grid(dict_grid_coarse, x_disc, y_disc, z_disc)
    grid_size = dict_grid_fine['nx']*dict_grid_fine['ny']*dict_grid_fine['nz']
    print(grid_size)

    grid_fine_file = '6-Grid/grid_fine_inf.txt'
    with open(grid_fine_file, 'w') as f:
        f.write('''{nx}   {xo}    {x_size}                  -nx,xmn,xsiz
{ny}   {yo}   {y_size}                  -ny,ymn,ysiz
{nz}    {zo}    {z_size}                  -nz,zmn,zsiz    '''.format(**dict_grid_fine))