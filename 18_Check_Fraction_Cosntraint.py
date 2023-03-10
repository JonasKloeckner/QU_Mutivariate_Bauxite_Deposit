

import Python_Module.io_module as io
import matplotlib.pyplot as plt
import numpy as np


def Plot_Fraction_Constraint(df, frac_name, tot_name, fig_name):
    # PLOT TOTAL AND RECOVERABLE ALUMINA
    frac_min = df[frac_name].min()
    frac_max = df[frac_name].max()
    tot_min = df[tot_name].min()
    tot_max = df[tot_name].max()


    Y = df[frac_name]
    X = df[tot_name]
    plt.figure(figsize=(6, 6))
    plt.scatter(x=X, y=Y, c='grey', edgecolors='k', s=20, zorder=2)
    plt.grid(True, linestyle='--', color='grey')
    plt.xlabel(f'{tot_name} (%)', fontsize=15)
    plt.ylabel(f'{frac_name} (%)', fontsize=15)
    plt.title('Realization 1', fontsize=15)
    plt.axis('equal')
    x_line = np.array([frac_min, tot_max])
    y_line = x_line
    plt.plot(x_line, y_line, 'k')

    plt.fill_between(x=[frac_min, tot_max], y1=[frac_min, tot_max], y2=[frac_min, frac_min],
                     facecolor='blue',
                     alpha=0.30)

    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)

    plt.savefig(fig_name, dpi=600, facecolor='w', edgecolor='w', format=None,
                transparent=False, bbox_inches='tight', pad_inches=0.1,
                frameon=None)
    plt.close()

    return None

if __name__ == '__main__':
    n_nodes_f = 5531184
    names = ['RCG', 'ATGc', 'STGc', 'FEGc', 'TIGc', 'PPGc', 'AAG', 'SRG']
    n_var = len(names)

    sim_file = '9-Simulation_Orig_Units/1_end_f.out'
    df_sim = io.Get_Df_From_Sim_File(file_name=sim_file, grid_size=n_nodes_f)
    df_sim.columns = names


    df_sim['CHECK_AAG'] = df_sim['AAG'] >  df_sim['ATGc']
    print(df_sim['CHECK_AAG'].sum())

    df_sim['CHECK_SRG'] = df_sim['SRG'] > df_sim['STGc']
    print(df_sim['CHECK_SRG'].sum())

    x_names = ['ATGc', 'STGc']
    y_names = ['AAG', 'SRG']

    df_sample = df_sim.sample(n=5000, replace=False, random_state=69069)

    for i in range(2):
        x_name = x_names[i]
        y_name = y_names[i]
        fig_name = f'10-Validation/Fraction_Constraint/biplot_{x_name}_{y_name}.png'
        Plot_Fraction_Constraint(df = df_sample, frac_name=y_name, tot_name=x_name, fig_name=fig_name)

    # PLOT TOTAL AND REACTIVE SILICA


