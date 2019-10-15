import os

import numpy as np

from bunch import *
par = Bunch()
aux = Bunch()

################################################################################
#                            main parameters                               #
################################################################################
def get_par():
	par.N_hc=1000
	par.N_ec_deep=15**2
	par.N_ec_supe=15**2

	par.Place_s=1				# Place Field Size
	par.Place_h=1				# Place Field Height

	par.Grid_spacing=3
	par.Grid_s=par.Grid_spacing/6
	par.Grid_h=1

	par.Env_shape='square'
	par.Env_size=10
	par.RateMap_resol=50

	par.Remap_prob=0.5
