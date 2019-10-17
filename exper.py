import numpy as np
from scipy.spatial.distance import cdist
from acts import Activation

class Experiment:

	def __init__(self,ty_in):
		self.Sample_type=ty_in

	def Define_Positions(self,par):
		[x_samp,y_samp]=np.meshgrid(np.linspace(0,par.Env_size,par.RateMap_resol)-par.Env_size/2,np.linspace(0,par.Env_size,par.RateMap_resol)-par.Env_size/2)
		self.Input_Positions=np.zeros((x_samp.size,2))
		self.Input_Positions[:,0]=np.ndarray.flatten(x_samp)
		self.Input_Positions[:,1]=np.ndarray.flatten(y_samp)

	def SampleOutput(self,par,J,PlaceMap,W=np.array([])):
		if(self.Sample_type=='PlaceToGrid'):
			self.Output=np.zeros((self.Input_Positions.shape[0],J.shape[0]))
			for tt in range(self.Input_Positions.shape[0]):
				x=self.Input_Positions[tt,0]
				y=self.Input_Positions[tt,1]
				D_Act=(PlaceMap.Place_Centers[:,0]-x)**2+(PlaceMap.Place_Centers[:,1]-y)**2
				Act=par.Place_h*np.exp(-D_Act/(2*(par.Place_s)**2))

				ActRule=Activation(J,W,'reverberation','mean')
				ActRule.Propagate(Act)


				
				
				#AO=AO/sum(AO)
				self.Output[tt,:]=ActRule.ActOut
			#self.Output=np.reshape(self.Output,(par.RateMap_resol,par.RateMap_resol,-1))	