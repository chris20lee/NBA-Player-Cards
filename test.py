import matplotlib
matplotlib.use('ps')
from matplotlib import rc

rc('text',usetex=True)
rc('text.latex', preamble=r'\usepackage{color}')
import matplotlib.pyplot as plt

plt.figure()
plt.ylabel(r'\textcolor{red}{Today} '+
           r'\textcolor{green}{is} '+
           r'\textcolor{blue}{cloudy.}')
plt.show()