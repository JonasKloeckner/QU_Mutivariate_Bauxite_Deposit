
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

if __name__ == '__main__':
    file_name = 'D:\Marcel\Alcoa_Data\\3_Work_Files\Parfile\Vmodel\\vmodel_NSAA1.par'

    test_var_tring = get_var_string(file_name)
    print(test_var_tring)

