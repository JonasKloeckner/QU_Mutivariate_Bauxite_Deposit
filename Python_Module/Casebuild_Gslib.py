

def Casebuild_Gslib(datafile, output_file, cols):
    f = open(datafile, 'r')
    f.readline()
    nvar = int(f.readline().lstrip().split()[0])

    name_list = []
    for i in xrange(1, (nvar + 1), 1):

        line = f.readline()
        line.lstrip()
        line.rstrip()
        line = line.split()[0]

        for col in cols:
            if (i == col):
                name_list.append(line)
    f.close()

    f = open(output_file, 'w')
    f.write('names = ' + str(name_list) + '\n')
    f.write('cols = ' + str(cols) + '\n')

    f.close()
