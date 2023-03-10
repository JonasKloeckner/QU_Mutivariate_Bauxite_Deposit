
import pandas as pd
import numpy as np

from Python_Module.Get_Var_String import get_var_string

if __name__ == '__main__':


    names_ns = ['NS_RCG', 'NS_ATGc', 'NS_STGc', 'NS_FEGc', 'NS_TIGc', 'NS_PPGc', 'NS_AAG', 'NS_SRG']

    n_var = len(names_ns)

    varname_list = []
    structure_list = []

    variance_structure_list = []
    range_ns_list = []
    range_ew_list = []
    range_vert_list = []

    for i in range(n_var):
        name = names_ns[i]

        name_leg = names_ns[i]

        vmodel_file = f'4-Variograms/NS_Model/{name}.par'

        string_var = get_var_string(vmodel_file_name=vmodel_file).splitlines()

        first_line = string_var[0]

        n_st = int(first_line.split()[0])
        nugget_effect = float(first_line.split()[1])

        varname_list.append(name_leg)
        structure_list.append('Nugget Effect')

        variance_structure_list.append(nugget_effect)

        range_ns_list.append(0.00)
        range_ew_list.append(0.00)
        range_vert_list.append(0.00)

        string_structures = string_var[1:]

        iterator = iter(string_structures)

        for k in range(n_st):
            varname_list.append(name_leg)
            line_1 = next(iterator)
            line_1_list = line_1.split()
            st_type = int(line_1_list[0])
            if (st_type == 1):
                structure_list.append('Spherical')
            if (st_type == 2):
                structure_list.append('Exponential')
            if (st_type == 3):
                structure_list.append('Gaussian')

            if (st_type not in [1, 2, 3]):
                print('ERROR STRUCTURE TYPE')

            variance_structure_list.append(float(line_1_list[1]))

            line_2 = next(iterator)
            line_2_list = line_2.split()

            range_ns_list.append(float(line_2_list[0]))
            range_ew_list.append(float(line_2_list[1]))
            range_vert_list.append(float(line_2_list[2]))

    columns = ['Variable', 'Structure', 'Contribution', 'Range NS', 'Range EW', 'Range vertical']

    df = pd.DataFrame(data=np.column_stack((varname_list, structure_list, variance_structure_list,
                                            range_ns_list, range_ew_list, range_vert_list)),

                      columns=columns
                      )

    output_file = '4-Variograms/table_ns_models.csv'

    df.to_csv(output_file, index=False, header=True, float_format='%.2f')

    # save in excel
#    output_file = '4-Variograms/table_ns_models.xlsx'
#
#    df.to_excel(output_file, index=False, header=True, float_format='%.2f')

