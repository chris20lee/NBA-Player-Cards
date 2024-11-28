########################################################################################################################
# 2st Graph
########################################################################################################################
cols = ref_player[['season', 'ortg_perc_rk', 'drtg_perc_rk']]

ref_player.plot(kind='line', x='season', y='ws_perc_rk', marker='o', color='r', linewidth=3.5, legend=None).grid(axis='y')
plt.gcf().set_size_inches(5, 3)
plt.title('Win Shares Percentile Rank', fontdict={'fontsize': 15, 'fontweight': 'bold'})
plt.xlabel('')
plt.ylabel('')
plt.xticks(fontsize=9)
plt.yticks(fontsize=9)
plt.ylim(0, 1)
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.margins(0.2, 0.2)
plt.locator_params(axis='y', nbins=4)
plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True)
plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=True)
for pos in ['right', 'top', 'left']:
    plt.gca().spines[pos].set_visible(False)
plt.tight_layout()
plt.show()
# plt.savefig('{}/{} in {}.png'.format(DATA_DIR, title, country), dpi=dpi_fig)
plt.close()

########################################################################################################################
# 2nd Graph
########################################################################################################################
ref_player.plot(kind='line', x='season', y=['ortg_perc_rk', 'drtg_perc_rk'], marker='o', color=['b', 'r'], linewidth=3.5, legend=None).grid(axis='y')
# cols.plot(kind='line', x='season', marker='o', color=['b', 'r'], linewidth=3.5, legend=None).grid(axis='y')
plt.gcf().set_size_inches(5, 3)
plt.title('Off Rating vs Def Rating', fontdict={'fontsize': 15, 'fontweight': 'bold'})
plt.xlabel('')
plt.ylabel('')
plt.xticks(fontsize=9)
plt.yticks(fontsize=9)
plt.ylim(0, 1)
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.margins(0.2, 0.2)
plt.locator_params(axis='y', nbins=4)
plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True)
plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=True)
for pos in ['right', 'top', 'left']:
    plt.gca().spines[pos].set_visible(False)
plt.tight_layout()
plt.show()
# plt.savefig('{}/{} in {}.png'.format(DATA_DIR, title, country), dpi=dpi_fig)
plt.close()
