


def Convert_Gslib_To_Csv(input_gslib_file_name, output_csv_file_name):
    n_var =0
    name_list = []
    f = open(input_gslib_file_name, 'r')
    f.readline()
    nvar = int( f.readline().split()[0] )

    for i in xrange(nvar):
        var_name = f.readline().split()[0]
        name_list.append(var_name)



    # Open output_file

    sep = ','
    fout = open(output_csv_file_name, 'w')
    for i in xrange(len(name_list)):
        fout.write(name_list[i] + sep)
    fout.write('\n')

    count = 0
    for line in f:
        set_of_columns_in_line = line.split()
        for j in xrange(len(set_of_columns_in_line)):
            fout.write(set_of_columns_in_line[j] + sep)
        fout.write('\n')

    f.close()
    fout.close()

    return