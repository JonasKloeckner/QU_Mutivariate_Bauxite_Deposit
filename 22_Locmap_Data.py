
import matplotlib.pyplot as plt
import Python_Module.io_module as io


if __name__ == '__main__':

    df = io.Get_Df_From_File('1-Data/proc_data.txt')

    plt.figure(figsize=(8, 6))

    plt.scatter(x=df['X'], y=df['Y'], c=df['ATGc'], cmap='viridis', s=5, zorder=2)
    plt.grid(True, linestyle='--', color='grey')
    plt.xlabel('X (m)', fontsize=15)
    plt.ylabel('Y (m)', fontsize=15)
    plt.axis('equal')

    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    cbar = plt.colorbar()
    cbar.set_label('ATGc (%)', fontsize=15)
    fig_name = '2-EDA/Locmap/locmap_ATGc.png'
    plt.savefig(fig_name, dpi=600, facecolor='w', edgecolor='w', format=None,
                transparent=False, bbox_inches='tight', pad_inches=0.1,
                frameon=None)
    plt.close()
