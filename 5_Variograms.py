
# CALCULATE EXPERIMENTAL VARIOGRAM

import os
import subprocess
from Python_Module.io_module import get_columns_from_names


def Run_Varcalc(name, col):
    par_path = os.path.join('4-Variograms', 'NS_Exp', f'{name}.par')
    pf = open(par_path, 'w')
    pf.write(f'''                  Parameters for VARCALC
                  **********************

START OF PARAMETERS:
3-Nscore/nscore_vario.out         -  file with data
2   3   4                         -   columns for X, Y, Z coordinates
1   {col}   {col}                 -   number of variables,column numbers (position used for tail,head variables below)
-998.0    1.0e21                  -   trimming limits
10                                -number of directions
0.0 22.5 25.0   0.0 22.5 0.50 0.0  -Dir 01: azm,azmtol,bandhorz,dip,diptol,bandvert,tilt
30  50.0  25.0                -        number of lags,lag distance,lag tolerance
22.5 22.5 25.0  0.0 22.5 0.50 0.0  -Dir 02: azm,azmtol,bandhorz,dip,diptol,bandvert,tilt
30  50.0  25.0                 -        number of lags,lag distance,lag tolerance
45.0 22.5 25.0   0.0 22.5 0.50 0.0  -Dir 03: azm,azmtol,bandhorz,dip,diptol,bandvert,tilt
30  50.0  25.0                 -        number of lags,lag distance,lag tolerance
67.5 22.5 25.0   0.0 22.5 0.50 0.0   -Dir 04: azm,azmtol,bandhorz,dip,diptol,bandvert,tilt
30  50.0  25.0                -        number of lags,lag distance,lag tolerance
90.0 22.5 25.0   0.0 22.5 0.50 0.0   -Dir 05: azm,azmtol,bandhorz,dip,diptol,bandvert,tilt
30  50.0  25.0                 -        number of lags,lag distance,lag tolerance
112.5 22.5 25.0   0.0 22.5 0.50 0.0   -Dir 06: azm,azmtol,bandhorz,dip,diptol,bandvert,tilt
30  50.0  25.0                 -        number of lags,lag distance,lag tolerance
135.0 22.5 25.0   0.0 22.5 0.50 0.0   -Dir 07: azm,azmtol,bandhorz,dip,diptol,bandvert,tilt
30  50.0  25.0                -        number of lags,lag distance,lag tolerance
157.5 22.5 25.0   0.0 22.5 0.50 0.0   -Dir 08: azm,azmtol,bandhorz,dip,diptol,bandvert,tilt
30  50.0  25.0               -        number of lags,lag distance,lag tolerance
0.00 90.0 100000.0   0.0 22.5 0.50 0.0 -Dir 09: azm,azmtol,bandhorz,dip,diptol,bandvert,tilt
30  50.0  25.0
0.00 22.5 10.00 -90.00 22.5 10.00 0.00 -Dir 10: azm,azmtol,bandhorz,dip,diptol,bandvert,tilt
20  0.50  0.25                 -        number of lags,lag distance,lag tolerance
4-Variograms/NS_Exp/{name}.out                       -file for experimental variogram points output.
1                                 -legacy output (0=no, 1=write out gamv2004 format)
1                                 -run checks for common errors
0                                 -standardize sills? (0=no, 1=yes)
1                                 -number of variogram types
1   1   1                        -tail variable, head variable, variogram type (and cutoff/category), sill
''')
    pf.close()
    exe_path = os.path.join('Gslib' ,'varcalc')
    subprocess.call([exe_path, par_path], shell=True)
    os.remove(par_path)

def Run_Vargplt(name):
    parfile = os.path.join('4-Variograms', 'NS_Plot', f'{name}_v.par')
    f = open(parfile, 'w')
    f.write('''
START OF PARAMETERS:
4-Variograms/NS_Plot/{name}_v.ps                -file for PostScript output
2                         -number of variograms to plot
0.0   5.0                 -distance  limits (from data if max<min)
0.0    1.3                -variogram limits (from data if max<min)
1      1.0                -plot sill (0=no,1=yes,2+=multiple), sill value(s))
Vertical             -Title for variogram
4-Variograms/NS_Exp/{name}.out               -1 file with variogram data
10   0    3  0   1        -variogram #, dash #, pts?, line?, color [pts(0=no,1=yes,2=number,3=bars,4=bars+num,make negitive=remove first point), line(integer >1 for thicker lines)]
4-Variograms/NS_Model/{name}.var               -2 file with variogram data
1   0    0  1   10         -variogram #, dash #, pts?, line?, color [pts(0=no,1=yes,2=number,3=bars,4=bars+num,make negitive=remove first point), line(integer >1 for thicker lines)]

    '''.format(**locals()))
    f.close()
    exe_file = os.path.join('Gslib', 'vargplt2008')
    subprocess.call([exe_file, parfile], shell=True)
    os.remove(parfile)

    parfile = os.path.join('4-Variograms', 'NS_Plot', '{name}_h_dir.par'.format(**locals()))
    f = open(parfile, 'w')
    f.write('''
START OF PARAMETERS:
4-Variograms/NS_Plot/{name}_h_dir.ps                -file for PostScript output
9                         -number of variograms to plot
0.0   2000.0                 -distance  limits (from data if max<min)
0.0    1.3                -variogram limits (from data if max<min)
1      1.0                -plot sill (0=no,1=yes,2+=multiple), sill value(s))
Horizontal Directional             -Title for variogram
4-Variograms/NS_Exp/{name}.out              -1 file with variogram data
1   0   0  1   7        -variogram #, dash #, pts?, line?, color [pts(0=no,1=yes,2=number,3=bars,4=bars+num,make negitive=remove first point), line(integer >1 for thicker lines)]
4-Variograms/NS_Exp/{name}.out              -2 file with variogram data
2   1    0  1   7        -variogram #, dash #, pts?, line?, color [pts(0=no,1=yes,2=number,3=bars,4=bars+num,make negitive=remove first point), line(integer >1 for thicker lines)]
4-Variograms/NS_Exp/{name}.out              -3 file with variogram data
3   0    0  1   5        -variogram #, dash #, pts?, line?, color [pts(0=no,1=yes,2=number,3=bars,4=bars+num,make negitive=remove first point), line(integer >1 for thicker lines)]
4-Variograms/NS_Exp/{name}.out              -4 file with variogram data
4   1    0  1   5        -variogram #, dash #, pts?, line?, color [pts(0=no,1=yes,2=number,3=bars,4=bars+num,make negitive=remove first point), line(integer >1 for thicker lines)]
4-Variograms/NS_Exp/{name}.out              -5 file with variogram data
5   0    0  1   2        -variogram #, dash #, pts?, line?, color [pts(0=no,1=yes,2=number,3=bars,4=bars+num,make negitive=remove first point), line(integer >1 for thicker lines)]
4-Variograms/NS_Exp/{name}.out              -6 file with variogram data
7   1    0  1   2        -variogram #, dash #, pts?, line?, color [pts(0=no,1=yes,2=number,3=bars,4=bars+num,make negitive=remove first point), line(integer >1 for thicker lines)]
4-Variograms/NS_Exp/{name}.out              -7 file with variogram data
8   0    0  1   1        -variogram #, dash #, pts?, line?, color [pts(0=no,1=yes,2=number,3=bars,4=bars+num,make negitive=remove first point), line(integer >1 for thicker lines)]
4-Variograms/NS_Exp/{name}.out              -8 file with variogram data
9   1    0  1   1        -variogram #, dash #, pts?, line?, color [pts(0=no,1=yes,2=number,3=bars,4=bars+num,make negitive=remove first point), line(integer >1 for thicker lines)]
4-Variograms/NS_Model/{name}.var               -9 Variogram model
2   0    0  1   10         -variogram #, dash #, pts?, line?, color [pts(0=no,1=yes,2=number,3=bars,4=bars+num,make negitive=remove first point), line(integer >1 for thicker lines)]

BLOCK FOR USER DEFINED LEGEND:
1  1  -0.2                -plot a legend for these shapes (1=yes),x,y between (-1,1) -1=left 1=right
N0              -label for variogram 1
N22E            -label for variogram 2
N45E             -label for variogram 3
N67E              -  label for variogram 4
N90E            -label for variogram 5
N112E
N135E
N157E
Variogram model

    '''.format(**locals()))
    f.close()
    exe_file = os.path.join('Gslib', 'vargplt2008')
    subprocess.call([exe_file, parfile], shell=True)
    os.remove(parfile)

    parfile = os.path.join('4-Variograms', 'NS_Plot', '{name}_h_Omni.par'.format(**locals()))
    f = open(parfile, 'w')
    f.write('''
START OF PARAMETERS:
4-Variograms/NS_Plot/{name}_h_Omni.ps                -file for PostScript output
2                         -number of variograms to plot
0.0   2000.0                 -distance  limits (from data if max<min)
0.0    1.3                -variogram limits (from data if max<min)
1      1.0                -plot sill (0=no,1=yes,2+=multiple), sill value(s))
Horizontal Omni             -Title for variogram
4-Variograms/NS_Exp/{name}.out              -1 file with variogram data
9   0   3  0   7        -variogram #, dash #, pts?, line?, color [pts(0=no,1=yes,2=number,3=bars,4=bars+num,make negitive=remove first point), line(integer >1 for thicker lines)]
4-Variograms/NS_Model/{name}.var               -2 file with variogram data
2   0    0  1   10         -variogram #, dash #, pts?, line?, color [pts(0=no,1=yes,2=number,3=bars,4=bars+num,make negitive=remove first point), line(integer >1 for thicker lines)]


BLOCK FOR USER DEFINED LEGEND:
0  1 0.2                -plot a legend for these shapes (1=yes),x,y between (-1,1) -1=left 1=right

    '''.format(**locals()))
    f.close()
    exe_file = os.path.join('Gslib', 'vargplt2008')
    subprocess.call([exe_file, parfile], shell=True)
    os.remove(parfile)




def Run_Vmodel_NS_RCG():
    parfile = os.path.join('4-Variograms', 'NS_Model', 'NS_RCG.par')
    f = open(parfile, 'w')
    f.write('''            Parameters for VMODEL
                  *********************

START OF PARAMETERS:
4-Variograms/NS_Model/NS_RCG.var                   -file for variogram output
2   400                       -number of directions and lags
0.0   -90.0    0.1            - azm, dip, lag distance (vertical direction)
0.0   0.0      5.0            - azm, dip, lag distance (horizontal direction)
3    0.0                     -nst, nugget effect
1    0.60  0.0   0.0   0.0    -it,cc,ang1,ang2,ang3
         60.0   60.0  1.75    -a_hmax, a_hmin, a_vert
1    0.10  0.0   0.0   0.0    -it,cc,ang1,ang2,ang3
         170.0   170.0  1.80    -a_hmax, a_hmin, a_vert
1    0.30  0.0   0.0   0.0    -it,cc,ang1,ang2,ang3
         3000.0   3000.0  1.85    -a_hmax, a_hmin, a_vert
''')
    f.close()
    exe_file = os.path.join('Gslib', 'vmodel')
    subprocess.call([exe_file, parfile], shell=True)



def Run_Vmodel_NS_A1():
    parfile = os.path.join('4-Variograms', 'NS_Model', 'NS_A1.par')
    f = open(parfile, 'w')
    f.write('''            Parameters for VMODEL
                  *********************

START OF PARAMETERS:
4-Variograms/NS_Model/NS_A1.var                   -file for variogram output
2   400                       -number of directions and lags
0.0   -90.0    0.1            - azm, dip, lag distance (vertical direction)
0.0   0.0      5.0            - azm, dip, lag distance (horizontal direction)
2    0.28                     -nst, nugget effect
1    0.40  0.0   0.0   0.0    -it,cc,ang1,ang2,ang3
         100.0   100.0  10   -a_hmax, a_hmin, a_vert
1    0.32  0.0   0.0   0.0    -it,cc,ang1,ang2,ang3
         1200.0   1200.0  18    -a_hmax, a_hmin, a_vert         

''')
    f.close()
    exe_file = os.path.join('Gslib', 'vmodel')
    subprocess.call([exe_file, parfile], shell=True)


def Run_Vmodel_NS_A2():
    parfile = os.path.join('4-Variograms', 'NS_Model', 'NS_A2.par')
    f = open(parfile, 'w')
    f.write('''            Parameters for VMODEL
                  *********************

START OF PARAMETERS:
4-Variograms/NS_Model/NS_A2.var                   -file for variogram output
2   400                       -number of directions and lags
0.0   -90.0    0.1            - azm, dip, lag distance (vertical direction)
0.0   0.0      5.0            - azm, dip, lag distance (horizontal direction)
3    0.0                     -nst, nugget effect
1    0.45  0.0   0.0   0.0    -it,cc,ang1,ang2,ang3
         40.0   40.0  2.20    -a_hmax, a_hmin, a_vert
1    0.18  0.0   0.0   0.0    -it,cc,ang1,ang2,ang3
         250.0   250.0  2.30    -a_hmax, a_hmin, a_vert
1    0.37  0.0   0.0   0.0    -it,cc,ang1,ang2,ang3
    1300.0   1300.0  2.40    -a_hmax, a_hmin, a_vert
''')
    f.close()
    exe_file = os.path.join('Gslib', 'vmodel')
    subprocess.call([exe_file, parfile], shell=True)


def Run_Vmodel_NS_A3():
    parfile = os.path.join('4-Variograms', 'NS_Model', 'NS_A3.par')
    f = open(parfile, 'w')
    f.write('''            Parameters for VMODEL
                  *********************

START OF PARAMETERS:
4-Variograms/NS_Model/NS_A3.var                   -file for variogram output
2   400                       -number of directions and lags
0.0   -90.0    0.1            - azm, dip, lag distance (vertical direction)
0.0   0.0      5.0            - azm, dip, lag distance (horizontal direction)
2    0.05                     -nst, nugget effect
1    0.55  0.0   0.0   0.0    -it,cc,ang1,ang2,ang3
         65.0   65.0  1.65    -a_hmax, a_hmin, a_vert
1    0.40  0.0   0.0   0.0    -it,cc,ang1,ang2,ang3
         2600.0   2600.0  2.00    -a_hmax, a_hmin, a_vert
''')
    f.close()
    exe_file = os.path.join('Gslib', 'vmodel')
    subprocess.call([exe_file, parfile], shell=True)


def Run_Vmodel_NS_A4():
    parfile = os.path.join('4-Variograms', 'NS_Model', 'NS_A4.par')
    f = open(parfile, 'w')
    f.write('''            Parameters for VMODEL
                  *********************

START OF PARAMETERS:
4-Variograms/NS_Model/NS_A4.var                   -file for variogram output
2   400                       -number of directions and lags
0.0   -90.0    0.1            - azm, dip, lag distance (vertical direction)
0.0   0.0      5.0            - azm, dip, lag distance (horizontal direction)
3    0.00                     -nst, nugget effect
1    0.47  0.0   0.0   0.0    -it,cc,ang1,ang2,ang3
         80.0   80.0  3.00    -a_hmax, a_hmin, a_vert
1    0.20  0.0   0.0   0.0    -it,cc,ang1,ang2,ang3
         500.0   500.0  3.40    -a_hmax, a_hmin, a_vert
1    0.33  0.0   0.0   0.0    -it,cc,ang1,ang2,ang3
         4000.0   4000.0  3.70    -a_hmax, a_hmin, a_vert
''')
    f.close()
    exe_file = os.path.join('Gslib', 'vmodel')
    subprocess.call([exe_file, parfile], shell=True)


def Run_Vmodel_NS_PPGc():
    parfile = os.path.join('4-Variograms', 'NS_Model', 'NS_PPGc.par')
    f = open(parfile, 'w')
    f.write('''            Parameters for VMODEL
                  *********************

START OF PARAMETERS:
4-Variograms/NS_Model/NS_PPGc.var                   -file for variogram output
2   400                       -number of directions and lags
0.0   -90.0    0.1            - azm, dip, lag distance (vertical direction)
0.0   0.0      5.0            - azm, dip, lag distance (horizontal direction)
3    0.0                     -nst, nugget effect
1    0.62  0.0   0.0   0.0    -it,cc,ang1,ang2,ang3
         50.0   50.0  1.20    -a_hmax, a_hmin, a_vert
1    0.23  0.0   0.0   0.0    -it,cc,ang1,ang2,ang3
         500.0   500.0  3.50    -a_hmax, a_hmin, a_vert
1    0.15  0.0   0.0   0.0    -it,cc,ang1,ang2,ang3
         10000.0   10000.0  6.00    -a_hmax, a_hmin, a_vert
''')
    f.close()
    exe_file = os.path.join('Gslib', 'vmodel')
    subprocess.call([exe_file, parfile], shell=True)


def Run_Vmodel_NS_FR_AAG():
    parfile = os.path.join('4-Variograms', 'NS_Model', 'NS_FR_AAG.par')
    f = open(parfile, 'w')
    f.write('''            Parameters for VMODEL
                  *********************

START OF PARAMETERS:
4-Variograms/NS_Model/NS_FR_AAG.var                   -file for variogram output
2   400                       -number of directions and lags
0.0   -90.0    0.1            - azm, dip, lag distance (vertical direction)
0.0   0.0      5.0            - azm, dip, lag distance (horizontal direction)
3    0.0                     -nst, nugget effect
1    0.50  0.0   0.0   0.0    -it,cc,ang1,ang2,ang3
         50.0   50.0  2.30    -a_hmax, a_hmin, a_vert
1    0.35  0.0   0.0   0.0    -it,cc,ang1,ang2,ang3
         600.0   600.0  2.80    -a_hmax, a_hmin, a_vert
1    0.15  0.0   0.0   0.0    -it,cc,ang1,ang2,ang3
         10000.0   10000.0  3.00    -a_hmax, a_hmin, a_vert
''')
    f.close()
    exe_file = os.path.join('Gslib', 'vmodel')
    subprocess.call([exe_file, parfile], shell=True)


def Run_Vmodel_NS_FR_SRG():
    parfile = os.path.join('4-Variograms', 'NS_Model', 'NS_FR_SRG.par')
    f = open(parfile, 'w')
    f.write('''            Parameters for VMODEL
                  *********************

START OF PARAMETERS:
4-Variograms/NS_Model/NS_FR_SRG.var                   -file for variogram output
2   400                       -number of directions and lags
0.0   -90.0    0.1            - azm, dip, lag distance (vertical direction)
0.0   0.0      5.0            - azm, dip, lag distance (horizontal direction)
3    0.12                     -nst, nugget effect
1    0.50  0.0   0.0   0.0    -it,cc,ang1,ang2,ang3
         50.0   50.0  3.70    -a_hmax, a_hmin, a_vert
1    0.28  0.0   0.0   0.0    -it,cc,ang1,ang2,ang3
         1200.0   1200.0  4.00    -a_hmax, a_hmin, a_vert
1    0.10  0.0   0.0   0.0    -it,cc,ang1,ang2,ang3
         2000.0   2000.0  4.20    -a_hmax, a_hmin, a_vert
''')
    f.close()
    exe_file = os.path.join('Gslib', 'vmodel')
    subprocess.call([exe_file, parfile], shell=True)



if __name__ == '__main__':

    names = ['NS_RCG', 'NS_A1', 'NS_A2', 'NS_A3', 'NS_A4', 'NS_PPGc', 'NS_FR_AAG', 'NS_FR_SRG']

    nscore_vario_file = '3-Nscore/nscore_vario.out'

    cols = get_columns_from_names(filename = nscore_vario_file, names= names)
    print(cols)

    #Run Experimental Variograms
    for i in range(len(names)):
        name = names[i]
        col = cols[i]
        Run_Varcalc(name=name, col=col)

    Run_Vmodel_NS_RCG()
    Run_Vargplt('NS_RCG')

    Run_Vmodel_NS_A1()
    Run_Vargplt('NS_A1')

    Run_Vmodel_NS_A2()
    Run_Vargplt('NS_A2')

    Run_Vmodel_NS_A3()
    Run_Vargplt('NS_A3')

    Run_Vmodel_NS_A4()
    Run_Vargplt('NS_A4')

    Run_Vmodel_NS_PPGc()
    Run_Vargplt('NS_PPGc')

    Run_Vmodel_NS_FR_AAG()
    Run_Vargplt('NS_FR_AAG')
##
    Run_Vmodel_NS_FR_SRG()
    Run_Vargplt('NS_FR_SRG')
