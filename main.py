import numpy as np

import params

from maps import PlaceRepresentation
from maps import GridRepresentation
from conns import Connections
from exper import Experiment

import matplotlib.pyplot as plt


para=params
para.get_par()

BaseMap=PlaceRepresentation(para.par)
BaseMap.New_Map(para.par)
BaseMap.Generate_RateMap(para.par)
plt.imshow(BaseMap.RateMap[:,:,0])
plt.show()
plt.scatter(BaseMap.Place_Centers[:,0],BaseMap.Place_Centers[:,1])
plt.show()


GridMap=GridRepresentation(para.par)
GridMap.New_Map(para.par)

GridMap.Generate_RateMap(para.par)
plt.imshow(GridMap.RateMap[:,:,0])
plt.show()


plt.scatter(GridMap.Grid_Centers[:,0,0],GridMap.Grid_Centers[:,1,0])
plt.show()

FF_Conn=Connections(para.par,BaseMap.Place_Centers.shape[0],GridMap.Grid_Centers.shape[0],'dist_placetogrid')
FF_Conn.Initialize(para.par,BaseMap.Place_Centers,GridMap.Grid_Centers)

Exp=Experiment('PlaceToGrid')
Exp.Define_Positions(para.par)

Exp.SampleOutput(para.par,FF_Conn.W,BaseMap)
AA=np.reshape(Exp.Output,(para.par.RateMap_resol,para.par.RateMap_resol,-1))
plt.imshow(AA[:,:,20])
plt.show()


BaseMap.Remap(para.par)
BaseMap.Generate_RateMap(para.par)
# plt.imshow(BaseMap.RateMap[:,:,0])
# plt.show()
# plt.scatter(BaseMap.Place_Centers[:,0],BaseMap.Place_Centers[:,1])
# plt.show()

Exp.SampleOutput(para.par,FF_Conn.W,BaseMap)
AA=np.reshape(Exp.Output,(para.par.RateMap_resol,para.par.RateMap_resol,-1))
plt.imshow(AA[:,:,20])
plt.show()


