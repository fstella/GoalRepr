import numpy as np
from scipy.spatial.distance import cdist
from acts import Activation
import matplotlib.pyplot as plt

import random
import bisect

class Experiment:

	def __init__(self,ty_in):
		self.Sample_type=ty_in

	def Define_Positions(self,par,pos_type='full'):
		if(pos_type=='full'):
			[x_samp,y_samp]=np.meshgrid(np.linspace(0,par.Env_size,par.RateMap_resol)-par.Env_size/2,np.linspace(0,par.Env_size,par.RateMap_resol)-par.Env_size/2)
			self.Input_Positions=np.zeros((x_samp.size,2))
			self.Input_Positions[:,0]=np.ndarray.flatten(x_samp)
			self.Input_Positions[:,1]=np.ndarray.flatten(y_samp)
		if(pos_type=='goal'):
			self.Input_Positions=np.zeros((100,2))
			self.Input_Positions[:,0]=0
			self.Input_Positions[:,1]=0

	def SampleOutput(self,par,J,PlaceMap,W=np.array([]),Act_Prop='sample'):
		if(self.Sample_type=='PlaceToGrid'):
			self.Output=np.zeros((self.Input_Positions.shape[0],J.shape[0]))
			
			if Act_Prop=='sample':
				self.OutputEvol=np.zeros((self.Input_Positions.shape[0],10,J.shape[0]))
			elif Act_Prop=='reverberation':
				self.OutputEvol=np.zeros((self.Input_Positions.shape[0],par.Rever_steps,J.shape[0]))

			for tt in range(self.Input_Positions.shape[0]):
				x=self.Input_Positions[tt,0]
				y=self.Input_Positions[tt,1]
				D_Act=(PlaceMap.Place_Centers[:,0]-x)**2+(PlaceMap.Place_Centers[:,1]-y)**2
				self.Act=par.Place_h*np.exp(-D_Act/(2*(par.Place_s)**2))

				self.SubSampleActivity(0.1)

				ActRule=Activation(J,W,Act_Prop,'none')
				ActRule.Propagate(self.Act,par.Act_noise_grid,par.Rever_steps)

				plt.plot(np.sum(ActRule.TimeAct,axis=1))
				
				
				#AO=AO/sum(AO)
				self.OutputEvol[tt,:,:]=ActRule.TimeAct
				self.Output[tt,:]=ActRule.ActOut
			#self.Output=np.reshape(self.Output,(par.RateMap_resol,par.RateMap_resol,-1))	
	def SubSampleActivity(self,perc):
		Act_Take=np.zeros(self.Act.shape)
		weights=self.Act

		counts = {}
		cdf_vals = np.cumsum(weights)/sum(weights)
		cdf_vals=np.ndarray.tolist(cdf_vals)
		
		while len(counts)<self.Act.size*perc:
			x = random.random()
			idx = bisect.bisect(cdf_vals, x)
			#print(idx)
			#idx=idx.astype(int)
			if idx in counts:
				counts[idx] += 1
			else:
				counts[idx] = 1
				Act_Take[idx]=1
		
		self.Act*=Act_Take




