import subprocess
list_of_scripts = [
"1_Declus_data.py",
"2_Prepare_The_Data.py",
"3_EDA.py",
"4_Nscore_Vario.py",
"5_Variograms.py",
"5B_Variograms_Originals.py",
"5C_Plot_Variograms_Originals.py",
"6_PPMT_Transform.py",
"7_Check_Grid.py",
"8_Create_Keyout.py",
"9_Simulation_Y_Space.py",
"10_Merge_Simulations_And_Back_PPMT.py",
"11_Back_Ratios.py",
"11B_Correct_Extrapolation.py",
"11C_Filter_Simulation.py",
"12_Run_Histsim_Varsim.py",
"13_Plot_Histograms_And_Variograms.py",
"14_Accplt_NS.py",
"15_Check_Scatter_Plots.py",
"16_Check_Minimum_And_Maximum.py",
"17_Check_Sum_Constraint.py",
"18_Check_Fraction_Cosntraint.py",
"19_Check_Coefficients_Correlation.py",
"20_Export_First_Realization.py",
"21_Export_Variogram_Models_Table.py",
"22_Locmap_Data.py",
"23_Biplot_PPMT_Data.py",
"24_Hist_from_polygons.py"
]

for script in list_of_scripts:
	subprocess.call(['python', script], shell=True)

