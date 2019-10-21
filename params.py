import os

import numpy as np

from bunch import *
par = Bunch()
aux = Bunch()

################################################################################
#                            main parameters                               #
################################################################################
def get_par():
	par.N_hc=1500
	par.N_ec_deep=15**2
	par.N_ec_supe=15**2

	par.Place_s=1				# Place Field Size
	par.Place_h=1				# Place Field Height

	par.Grid_spacing=5
	par.Grid_s=par.Grid_spacing/6
	par.Grid_h=1

	par.Conn_pltogr_spread=par.Grid_s/4
	par.Conn_grtogr_spread=par.Grid_s/3

	par.Conn_grtogr_inhib=0.0009  # To be compared with a mximum positive connection of 1

	par.Env_shape='square'
	par.Env_size=10
	par.RateMap_resol=50

	par.Remap_prob=0.2


	par.Conn_norm_ff=1
	par.Conn_norm_re=1

	par.Act_noise_grid=0.005

	par.Rever_steps=100