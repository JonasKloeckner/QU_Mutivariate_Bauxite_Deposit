
import numpy as np
from Extract_Column_from_gslib import get_float_column_from_gslib_file
import os

def get_real(sim_file, i_real, grid_size):



    print('Start Getting Realization')
    f = open(sim_file, 'r')

    line = f.readline()

    l_nvar = f.readline()
    n_var = int(l_nvar.split()[0])

    real_array = np.zeros([grid_size, n_var])

    #skipp header
    for i in xrange(n_var):
        line = f.readline()


    for i in xrange(1, i_real + 1):
        for j in xrange(grid_size):
            line = f.readline()
            if(i==i_real):

                if(len(f.readline().split()) != n_var):
                    print('ERROR LINE {}'.format(j))
                numbers = np.array([float(k) for k in f.readline().split()])

                for k in xrange(n_var):
                    real_array[j, k] = numbers[k]
            if( (j % 100000) == 0):
                print('real {}   grid_id = {}'.format(i, j))

    f.close()

    return real_array


def pick_real(sim_file, out_file, i_real, grid_size):

    print('Start Getting Realization')
    f = open(sim_file, 'r')
    fout = open(out_file, 'w')
    line = f.readline()
    fout.write(line)
    l_nvar = f.readline()
    nvar = int(l_nvar.split()[0])
    fout.write(l_nvar)

    #Copy header
    for i in xrange(nvar):
        line = f.readline()

        fout.write(line)
    print('Finish copying header')
    print('start reading grid')
    for i in xrange(1, i_real + 1):
        for j in xrange(grid_size):
            line = f.readline()
            if(i==i_real):
                fout.write(line)

            if( (j % 100000) == 0):
                print('real {}   grid_id = {}'.format(i, j))

    f.close()
    fout.close()
    return True

def Get_Simulation(sim_file, col, grid_size, n_real):
    sim_vector = get_float_column_from_gslib_file(sim_file, col)
    sim_array = np.reshape(sim_vector, (grid_size, n_real), order='F')
    return sim_array
