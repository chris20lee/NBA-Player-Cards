import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

x = 0.99
print(x * 0.85)
print((1 - x) * 0.85)


# Function to create color scale from matte red to matte blue
def red_to_blue_color_scale(n_points):
    # Define the RGB values for matte red and matte blue
    red = np.array([0.8, 0.5, 0])   # Matte red (RGB)
    blue = np.array([0, 0.5, 0.8])  # Matte blue (RGB)

    # Create a linear interpolation between the two colors
    colors = np.linspace(red, blue, n_points)

    return colors

# Example usage: Generate 10 colors from red to blue
n_points = 100
color_scale = red_to_blue_color_scale(n_points)

# Plotting the color scale
plt.figure(figsize=(6, 2))
plt.imshow([color_scale], aspect='auto', extent=[0, 1, 0, 1])
plt.axis('off')  # Turn off axis
plt.title('Color Scale from Matte Red to Matte Blue')
plt.show()


# ########################################################################################################################
# # 2st Graph
# ########################################################################################################################
# cols = ref_player[['season', 'ortg_perc_rk', 'drtg_perc_rk']]
#
# ref_player.plot(kind='line', x='season', y='ws_perc_rk', marker='o', color='r', linewidth=3.5, legend=None).grid(axis='y')
# plt.gcf().set_size_inches(5, 3)
# plt.title('Win Shares Percentile Rank', fontdict={'fontsize': 15, 'fontweight': 'bold'})
# plt.xlabel('')
# plt.ylabel('')
# plt.xticks(fontsize=9)
# plt.yticks(fontsize=9)
# plt.ylim(0, 1)
# plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
# plt.margins(0.2, 0.2)
# plt.locator_params(axis='y', nbins=4)
# plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True)
# plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=True)
# for pos in ['right', 'top', 'left']:
#     plt.gca().spines[pos].set_visible(False)
# plt.tight_layout()
# plt.show()
# # plt.savefig('{}/{} in {}.png'.format(DATA_DIR, title, country), dpi=dpi_fig)
# plt.close()
#
# ########################################################################################################################
# # 2nd Graph
# ########################################################################################################################
# ref_player.plot(kind='line', x='season', y=['ortg_perc_rk', 'drtg_perc_rk'], marker='o', color=['b', 'r'], linewidth=3.5, legend=None).grid(axis='y')
# # cols.plot(kind='line', x='season', marker='o', color=['b', 'r'], linewidth=3.5, legend=None).grid(axis='y')
# plt.gcf().set_size_inches(5, 3)
# plt.title('Off Rating vs Def Rating', fontdict={'fontsize': 15, 'fontweight': 'bold'})
# plt.xlabel('')
# plt.ylabel('')
# plt.xticks(fontsize=9)
# plt.yticks(fontsize=9)
# plt.ylim(0, 1)
# plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
# plt.margins(0.2, 0.2)
# plt.locator_params(axis='y', nbins=4)
# plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True)
# plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=True)
# for pos in ['right', 'top', 'left']:
#     plt.gca().spines[pos].set_visible(False)
# plt.tight_layout()
# plt.show()
# # plt.savefig('{}/{} in {}.png'.format(DATA_DIR, title, country), dpi=dpi_fig)
# plt.close()
