import rpy2
import rpy2.robjects as robjects

## To aid in printing HTML in notebooks
import rpy2.ipython.html
rpy2.ipython.html.init_printing()

## To see plots in an output cell
from rpy2.ipython.ggplot import image_png

from rpy2.robjects.packages import importr, data

utils = importr('utils')
base = importr('base')