import linecache
import numpy as np
import pandas as pd
import os

def get_float_column_from_gslib_file(filename, col):
    '''

    :param filename: string which contains the path of the ascii file in GSLIB format
    :param col: integer which specifies the column to be extracted
    :return:
    '''

    col = col - 1
    l_nvar = linecache.getline(filename, 2)
    l_nvar = l_nvar.lstrip()
    nvar = int(l_nvar.split()[0])

    f = open(filename, 'r')

    count = 0
    var = []
    for line in f:
        if(count > (nvar+1) ):
            line_clean = line.lstrip()

            raw_row = line_clean.split()

            var.append(float(raw_row[col]))
        
        count = count + 1

    f.close()
    return var


def get_int_column_from_gslib_file(filename, col):

    col = col - 1
    l_nvar = linecache.getline(filename, 2)
    l_nvar = l_nvar.lstrip()
    nvar = int(l_nvar.split()[0])

    f = open(filename, 'r')

    count = 0
    var = []
    for line in f:
        if(count > (nvar+1) ):
            line_clean = line.lstrip()

            raw_row = line_clean.split()

            var.append(int(raw_row[col]))

        count = count + 1

    f.close()
    return var


def get_np_array_from_gslib_file(filename, list_of_cols):
    '''
    :param filename: string, path of the gslib file
    :param list_of_cols: list of integers, contains the columns which will be stored in the array
    :return: numpy array type = float. Each column of numpy array is contains the variables
    '''
    list_of_vars = []
    for col in list_of_cols:
        var_ppmt = get_float_column_from_gslib_file(filename, col)
        list_of_vars.append(var_ppmt)

    array_of_variables = np.array(list_of_vars)
    array_of_variables_T = np.transpose(array_of_variables)

    return array_of_variables_T

def get_array_gslib(filename, list_of_cols):
    '''
    :param filename: string, path of the gslib file
    :param list_of_cols: list of integers, contains the columns which will be stored in the array
    :return: numpy array type = float. Each column of numpy array is contains the variables
    '''
    line_nvar = linecache.getline(filename = filename, lineno = 2)
    n_var = int(line_nvar.split()[0])
    numpy_index_list = list_of_cols - 1
    array = np.genfromtxt(fname = filename, dtype=float, skip_header=n_var+2, usecols=numpy_index_list,
                          autostrip=True
                          )

    return array

def get_array_gslib_from_names_pd(filename, list_of_names):

    columns = get_columns_from_names(filename=filename, names=list_of_names)
    array = get_array_gslib_pd(filename, columns )


    return array

def get_array_gslib_pd(filename, list_of_cols):
    line_nvar = linecache.getline(filename=filename, lineno=2)

    n_var = int(line_nvar.split()[0])
    numpy_index_list = list_of_cols - 1

    n_lines_header = n_var + 2

    names = [str(i) for i in np.arange(len(list_of_cols))]
    df = pd.read_csv(filepath_or_buffer = filename, header=None , skiprows=n_lines_header, usecols=numpy_index_list,delim_whitespace=True)

    array = df.values



    return array




def get_first_real_pd(filename, list_of_cols, grid_size):
    line_nvar = linecache.getline(filename=filename, lineno=2)
    n_var = int(line_nvar.split()[0])
    numpy_index_list = list_of_cols - 1

    n_lines_header = n_var + 2

    names = [str(i) for i in np.arange(len(list_of_cols))]
    df = pd.read_csv(filepath_or_buffer = filename, header=None , skiprows=n_lines_header,
                     usecols=numpy_index_list,delim_whitespace=True, nrows=grid_size)
    array = df.values


    return array


def Get_Df_From_Sim_File(file_name, grid_size):
    list_of_names = []
    with open(file_name, 'r') as f:
        f.readline()  # skip first line
        n_var = int(f.readline().split()[0])

        for i in range(n_var):
            string_name = f.readline().split()[0]
            list_of_names.append(string_name)

    n_lines_header = n_var + 2

    df = pd.read_csv(filepath_or_buffer = file_name, names = list_of_names, header=None, skiprows=n_lines_header,
                      delim_whitespace=True, nrows=grid_size)

    return df





def get_ireal_pd(filename, list_of_cols, grid_size, ireal):
    line_nvar = linecache.getline(filename=filename, lineno=2)


    n_var = int(line_nvar.split()[0])
    numpy_index_list = list_of_cols - 1

    n_lines_header = n_var + 2

    n_reals_to_skip = ireal - 1
    n_lines_to_skip = n_lines_header + (grid_size*n_reals_to_skip)


    df = pd.read_csv(filepath_or_buffer = filename, header=None , skiprows = n_lines_to_skip,
                     usecols=numpy_index_list,delim_whitespace=True, nrows=grid_size, dtype = float)
    array = df.values


    return array


def get_ireal_pd_filter(filename, list_of_cols, grid_size, ireal):
    line_nvar = linecache.getline(filename=filename, lineno=2)
    n_var = int(line_nvar.split()[0])
    numpy_index_list = list_of_cols - 1

    n_lines_header = n_var + 2

    n_reals_to_skip = ireal - 1
    n_lines_to_skip = n_lines_header + (grid_size*n_reals_to_skip)

    df = pd.read_csv(filepath_or_buffer = filename, header=None , skiprows = n_lines_to_skip,
                     usecols=numpy_index_list,delim_whitespace=True, nrows=grid_size)
    array = df.values

    array_filter = array[array[:, 0] > -98.00]


    return array_filter



def get_all_simulations(filename, list_of_cols, grid_size, n_real):
    line_nvar = linecache.getline(filename=filename, lineno=2)

    n_var = int(line_nvar.split()[0])
    numpy_index_list = list_of_cols - 1

    n_lines_header = n_var + 2

    n_lines_to_read = grid_size*n_real

    df = pd.read_csv(filepath_or_buffer=filename, header=None, skiprows = n_lines_header,
                     usecols=numpy_index_list, delim_whitespace=True, nrows = n_lines_to_read)
    array = df.values




    return array


def get_columns_from_names(filename, names):

    list_of_names = []
    with open(filename, 'r') as f:
        f.readline() #skip first line
        n_var = int(f.readline().split()[0])

        for i in range(n_var):
            string_name = f.readline().split()[0]
            list_of_names.append(string_name)

    list_of_col_numbers = []
    for name in names:
        index_of_col = list_of_names.index(name)
        list_of_col_numbers.append(index_of_col + 1) # python index starts at zero, so we have to add one

    return np.array(list_of_col_numbers)



def get_names_of_gslib_file(filename):

    list_of_names = []
    with open(filename, 'r') as f:
        f.readline() #skip first line
        n_var = int(f.readline().split()[0])

        for i in range(n_var):
            string_name = f.readline().split()[0]
            list_of_names.append(string_name)

    return list_of_names


def Get_Df_From_File(file_name):
    list_of_names = []
    with open(file_name, 'r') as f:
        f.readline()  # skip first line
        n_var = int(f.readline().split()[0])

        for i in range(n_var):
            string_name = f.readline().split()[0]
            list_of_names.append(string_name)

    n_lines_header = n_var + 2

    df = pd.read_csv(filepath_or_buffer=file_name, header=None, names = list_of_names, skiprows=n_lines_header,  delim_whitespace=True)

    return df



def Get_Df_From_Variogram_File(file_name):



    names = ['Variogram Index',
        'Lag Distance',
        'Number of Pairs',
        'Variogram Value',
        'Variogram Number',
        'Calculation Azimuth',
        'Calculation Dip',
        'Variogram Type'
    ]

    array_var = get_array_gslib_pd(filename= file_name, list_of_cols = np.arange(1, 9))

    df_var = pd.DataFrame(data = array_var, columns = names)

    return df_var



def Get_Df_From_Varmodel_File(file_name):



    names = ['Variogram Index',
        'Lag Distance',
        'Number of Pairs',
        'Variogram Value',
        'Variogram Number',
        'Calculation Azimuth',
        'Calculation Dip']

    array_var = get_array_gslib_pd(filename= file_name, list_of_cols = np.arange(1, 8))

    df_var = pd.DataFrame(data = array_var, columns = names)

    return df_var


def Get_Df_From_Histplt_File(file_name):

    names = ['realization',
'number of data',
'number of data trimmed',
'mean',
'standard deviation',
'coefficient of variation',
'maximum',
'upper quartile',
'median',
'lower quartile',
'minimum']

    array_var = get_array_gslib_pd(filename= file_name, list_of_cols = np.arange(1, 12))

    df_var = pd.DataFrame(data = array_var, columns = names)

    return df_var



def to_Gslib(output_file, dataframe, float_format):
    # Write Header
    fout = open(output_file, 'w')
    fout.write('''Gslib file
{}  \n'''.format(len(dataframe.columns)))
    for i in range(len(dataframe.columns)):
        fout.write('{}  \n'.format(dataframe.columns.values[i]))
    fout.close()
    with open(output_file, 'a') as fout:
        dataframe.to_csv(fout, index=False, sep=' ', float_format=float_format, header=False, line_terminator='\n')

    return True



def read_grid_info(file_name):



    dict_grid = {'xo':0.00, 'nx':1, 'x_size':1.00,
                'yo': 0.00, 'ny': 1, 'y_size': 1.00,
                'zo': 0.00, 'nz': 1, 'z_size': 1.00
                }

    with open(file_name, 'r') as f:
        line = f.readline().split()
        dict_grid['nx'] = int(line[0])
        dict_grid['xo'] = float(line[1])
        dict_grid['x_size'] = float(line[2])

        line = f.readline().split()
        dict_grid['ny'] = int(line[0])
        dict_grid['yo'] = float(line[1])
        dict_grid['y_size'] = float(line[2])

        line = f.readline().split()
        dict_grid['nz'] = int(line[0])
        dict_grid['zo'] = float(line[1])
        dict_grid['z_size'] = float(line[2])


    grid_string = '''{} {:.2f} {:.2f}    - nx, xo, x_size
{} {:.2f} {:.2f}    - ny, yo, y_size
{} {:.2f} {:.2f}    - nz, zo, z_size   '''.format(dict_grid['nx'],   dict_grid['xo'],    dict_grid['x_size'],
                          dict_grid['ny'], dict_grid['yo'], dict_grid['y_size'],
                          dict_grid['nz'], dict_grid['zo'], dict_grid['z_size']

                          )

    return grid_string




def get_grid_dict(file_name):



    dict_grid = {'xo':0.00, 'nx':1, 'x_size':1.00,
                'yo': 0.00, 'ny': 1, 'y_size': 1.00,
                'zo': 0.00, 'nz': 1, 'z_size': 1.00
                }

    with open(file_name, 'r') as f:
        line = f.readline().split()
        dict_grid['nx'] = int(line[0])
        dict_grid['xo'] = float(line[1])
        dict_grid['x_size'] = float(line[2])

        line = f.readline().split()
        dict_grid['ny'] = int(line[0])
        dict_grid['yo'] = float(line[1])
        dict_grid['y_size'] = float(line[2])

        line = f.readline().split()
        dict_grid['nz'] = int(line[0])
        dict_grid['zo'] = float(line[1])
        dict_grid['z_size'] = float(line[2])


    return dict_grid




def export_grid_into_VTK_File(dataframe, out_vtk_file, dict_grid):
    xo = dict_grid['xo']
    x_size = dict_grid['x_size']
    nx = dict_grid['nx']

    yo = dict_grid['yo']
    y_size = dict_grid['y_size']
    ny = dict_grid['ny']

    zo = dict_grid['zo']
    z_size = dict_grid['z_size']
    nz = dict_grid['nz']

    ncells = nx * ny * nz
    npx = nx + 1
    npy = ny + 1
    npz = nz + 1

    names = dataframe.columns.values

    n_rows = dataframe.shape[0]
    n_cols = dataframe.shape[1]

    # open output file
    with open(out_vtk_file, 'w') as fout:
        separator = ' '
        fout.write(
        '# vtk DataFile Version 4.0' + '\n' + 'Estimates' + '\n' + 'ASCII' + '\n' + 'DATASET STRUCTURED_POINTS' + '\n' +
        'DIMENSIONS' + separator + str(npx) + separator + str(npy) + separator + str(npz) + '\n' +
        'SPACING' + separator + str(x_size) + separator + str(y_size) + separator + str(z_size) + '\n' +
        'ORIGIN' + separator + str(xo) + separator + str(yo) + separator + str(zo) + '\n' +
        'CELL_DATA' + separator + str(ncells) + '\n')



        for i in range(n_cols):
            name = names[i]
            fout.write('FIELD' + separator + name + separator + '1' + '\n')
            fout.write(name + separator + '1' + separator + str(ncells) + separator + 'float' + '\n')
            # loop j designates rows and i designates columns
            for j in range(n_rows):
                fout.write('{:.4f}'.format(dataframe.iloc[j, i]) + '\n')


    return None

def get_var_string(vmodel_file_name):
    '''
    :param vmodel_file_name: string, path that contains the parfile of vmodel
    :return: string of the variogram
    '''

    f = open(vmodel_file_name, 'r')
    line = f.readline()

    while('START OF PARAMETERS' not in line):
        line = f.readline()


    # READ OUTPUT FILE
    f.readline()


    n_directions = int(f.readline().split()[0])

    # Skip directions
    for i in range(n_directions):
        f.readline()

    var_string = ''

    # read nstructures + nugget effetc
    first_line_of_variogram = f.readline()
    var_string = var_string + first_line_of_variogram

    # read n_struct
    n_struct = int(first_line_of_variogram.split()[0])

    for j in range(n_struct):
        var_string = var_string + f.readline()
        var_string = var_string + f.readline()

    f.close()

    return var_string


