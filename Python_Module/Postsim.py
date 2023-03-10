
def Calc_Total_Grade(Grade, Ratio_Perc):
    Ratio_Frac = Ratio_Perc/100.000
    Total_Grade = Grade / Ratio_Frac
    return Total_Grade

def Correct_Grade_For_Bounds(Grade, min_data, max_data, count_error):

    if (Grade > max_data):
        Grade = max_data
        count_error = count_error + 1
    if (Grade < min_data):
        Grade = min_data
        count_error = count_error + 1

    return Grade, count_error





def Post_Process_Simulation(input_sim_file, out_sim_file, out_report_error_file,
                            col_rc1, col_aa1, col_aa1_ratio, col_sr1, col_sr1_ratio, col_fe1, col_ti1,

                            col_rc3, col_aa3, col_aa3_ratio, col_sr3, col_sr3_ratio, col_fe3, col_ti3,

                            min_at1, min_st1, max_at1, max_st1,
                            min_at3, min_st3, max_at3, max_st3):
    '''
    input: sim_file, out_file, report_error_file
    columns of grades and ratios
    This function calculates the total grades, check if it is inside the boundaries of the data.

    The output file contains the simulations in this order:
    RC1, AT1, AA1, ST1, SR1, FE1, TI1
    RC3, AT3, AA3, ST3, SR3, FE3, TI3

    The report file summarizes the amount of errors for the total grades

    :return: True
    '''
    print('OPENING INPUT SIMULATION FILE')
    fout = open(out_sim_file, 'w')
    fout.write('''USGSIM using Accumulated Variables
14
RC1
AT1
AA1
ST1
SR1
FE1
TI1
RC3
AT3
AA3
ST3
SR3
FE3
TI3   \n''')

    count_error_at1 = 0
    count_error_st1 = 0
    count_error_at3 = 0
    count_error_st3 = 0

    sim_file = open(input_sim_file, 'r')
    j = 0
    count = 0
    for line in sim_file:
        if (j > 15):
            numbers = [float(i) for i in line.split()]
            if (min(numbers) < -97.000):
                fout.write('{} {} {} {} {} {} {} {} {} {} {} {} {} {} \n'.format(-99, -99, -99, -99, -99, -99,-99, -99, -99, -99, -99, -99, -99, -99 ))
            else:
                # Read Input simulation grades
                RC1 = numbers[col_rc1 - 1]
                AA1 = numbers[col_aa1 - 1]
                AA1_RATIO = numbers[col_aa1_ratio - 1]
                SR1 = numbers[col_sr1 - 1]
                SR1_RATIO = numbers[col_sr1_ratio - 1]
                FE1 = numbers[col_fe1 - 1]
                TI1 = numbers[col_ti1 - 1]

                RC3 = numbers[col_rc3 - 1]
                AA3 = numbers[col_aa3 - 1]
                AA3_RATIO = numbers[col_aa3_ratio - 1]
                SR3 = numbers[col_sr3 - 1]
                SR3_RATIO = numbers[col_sr3_ratio - 1]
                FE3 = numbers[col_fe3 - 1]
                TI3 = numbers[col_ti3 - 1]



                # Calculate total Grades
                AT1 = Calc_Total_Grade(AA1, AA1_RATIO)
                AT1, count_error_at1 = Correct_Grade_For_Bounds(AT1, min_at1, max_at1, count_error_at1)

                ST1 = Calc_Total_Grade(SR1, SR1_RATIO)
                ST1, count_error_st1 = Correct_Grade_For_Bounds(ST1, min_st1, max_st1, count_error_st1)


                AT3 = Calc_Total_Grade(AA3, AA3_RATIO)
                AT3, count_error_at3 = Correct_Grade_For_Bounds(AT3, min_at3, max_at3, count_error_at3)

                ST3 = Calc_Total_Grade(SR3, SR3_RATIO)
                ST3, count_error_st3 = Correct_Grade_For_Bounds(ST3, min_st3, max_st3, count_error_st3)

                fout.write(
                    '{RC1:.4f} {AT1:.4f} {AA1:.4f} {ST1:.4f} {SR1:.4f} {FE1:.4f} {TI1:.4f} {RC3:.4f} {AT3:.4f} {AA3:.4f} {ST3:.4f} {SR3:.4f} {FE3:.4f} {TI3:.4f} \n'.format(
                        **locals()))

            count = count + 1
            if (count % 100000 == 0):
                print('node_id = {}'.format(count))

        j = j + 1

    sim_file.close()
    fout.close()

    fout_error =open(out_report_error_file, 'w')
    fout_error.write('Variable Count_Of_Errors \n')
    fout_error.write('AT1 {} \n'.format(count_error_at1))
    fout_error.write('ST1 {} \n'.format(count_error_st1))
    fout_error.write('AT3 {} \n'.format(count_error_at3))
    fout_error.write('AT1 {} \n'.format(count_error_st3))
