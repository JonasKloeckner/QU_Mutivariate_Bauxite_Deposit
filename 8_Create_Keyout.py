

import subprocess
import os
import Python_Module.io_module as io
import numpy as np
import pandas as pd

def downscale_array(grid_coarse, x_disc, y_disc, z_disc):
    nx, ny, nz = grid_coarse.shape[0], grid_coarse.shape[1], grid_coarse.shape[2]
    grid_fine = np.zeros(shape=(nx*x_disc, ny*y_disc, nz*z_disc))

    for ix in range(nx):
        start_slice_x = ix * x_disc
        end_slice_x = start_slice_x + x_disc

        for iy in range(ny):
            start_slice_y = iy * y_disc
            end_slice_y = start_slice_y + y_disc

            for iz in range(nz):
                start_slice_z = iz * z_disc
                end_slice_z = start_slice_z + z_disc
                grid_fine[start_slice_x:end_slice_x, start_slice_y:end_slice_y, start_slice_z:end_slice_z] = grid_coarse[ix, iy, iz]

    return grid_fine



def run_kt3d(grid_file):

    dict_grid = io.get_grid_dict(grid_file)

    par_path = '11-Estimates/kt3d_RC.par'
    pf = open(par_path, 'w')
    pf.write('''                  Parameters for KT3D
                  *******************

START OF PARAMETERS:
1-Data/proc_data.txt              -file with data
0  2  3  4  5  0                 -   columns for DH,X,Y,Z,var,sec var
-98.00   1.0e21                 -   trimming limits
0                                -option: 0=grid, 1=cross, 2=jackknife
xvk.dat                          -file with jackknife data
1   2   0    3    0              -   columns for X,Y,Z,vr and sec var
1                                -debugging level: 0,1,2,3
11-Estimates/kt3d_RC.dbg        -file for debugging output
11-Estimates/kt3d_RC.out        -file for kriged output
{nx}   {xo}    {x_size}                  -nx,xmn,xsiz
{ny}   {yo}   {y_size}                  -ny,ymn,ysiz
{nz}    {zo}    {z_size}                  -nz,zmn,zsiz  
5    5      1                    -x,y and z block discretization
3    24                           -min, max data for kriging
3                                -max per octant (0-> not used)
500.0  500.0  5.0                 -maximum search radii
 0.0   0.0   0.0                 -angles for search ellipsoid
1     2.302                      -0=SK,1=OK,2=non-st SK,3=exdrift
0 0 0 0 0 0 0 0 0                -drift: x,y,z,xx,yy,zz,xy,xz,zy
0                                -0, variable; 1, estimate trend
extdrift.dat                     -gridded file with drift/mean
4                                -  column number in gridded file
1    0.2                         -nst, nugget effect
1    0.8  0.0   0.0   0.0        -it,cc,ang1,ang2,ang3
         500.0  500.0  5.0        -a_hmax, a_hmin, a_vert
        	'''.format(**dict_grid))
    pf.close()
    exe_path = os.path.join('Gslib','kt3d')
    subprocess.call([exe_path, par_path], shell=True)


if __name__ == '__main__':

    x_disc = 4
    y_disc = 4
    z_disc = 1

    grid_file = '6-Grid/grid_coarse_inf.txt'
    dict_grid = io.get_grid_dict(grid_file)

    run_kt3d(grid_file)
    cols = np.array([1, 2])

    df = io.Get_Df_From_File(file_name='11-Estimates/kt3d_RC.out')
    print(df.columns.values)

    io.export_grid_into_VTK_File(dataframe=df, out_vtk_file='11-Estimates/kt3d_RC.vtk',
                                 dict_grid=dict_grid)

    nx, ny, nz = dict_grid['nx'], dict_grid['ny'], dict_grid['nz']
    theshold_krig = 0.75

    df['MASK'] = (df['EstimationVariance'] < theshold_krig) & (df['EstimationVariance'] > -98.0)
    df['MASK'] = df['MASK'].astype(int)
    print(df['MASK'].count(), df['MASK'].sum())
    print((df['MASK'].sum()/df['MASK'].count())*100)

    out_file = '6-Grid/keyout_coarse.out'
    df_out = df[['MASK']]
    test  = io.to_Gslib(output_file=out_file, dataframe=df_out, float_format='%.4f')

    array_mask = df['MASK'].values
    mask_grid_coarse = np.reshape(array_mask, newshape=(nx, ny, nz), order='F')

    mask_grid_fine = downscale_array(grid_coarse=mask_grid_coarse, x_disc=x_disc, y_disc=y_disc, z_disc=z_disc)
    mask_array_fine = np.reshape(mask_grid_fine, newshape=( nx*ny*nz* x_disc*y_disc*z_disc ,1), order='F')
    out_file = '6-Grid/keyout_fine.out'
    df_fine = pd.DataFrame(data=mask_array_fine, columns=['MASK'])
    df_fine['MASK'] = df_fine['MASK'].astype(int)
    test = io.to_Gslib(output_file=out_file, dataframe=df_fine, float_format='%.4f')





