import numpy as np
from scipy.spatial.distance import cdist

class Connections:

	def __init__(self,par,input_n,output_n,c_type,conn_str):
		self.W=np.zeros((output_n,input_n))
		self.c_type=c_type
		self.Conn_norm=conn_str

	def Normalize(self,par):
	# normalize matrix post_synaptic strengths 
		if self.W.size>0:
			z = abs(self.W).sum(1)
			z[z==0]=1
			self.W /= z[:,None]
			self.W *= self.Conn_norm

	def Initialize(self,par,Centers_In,Centers_Out):
		input_n=Centers_In.shape[0]
		output_n=Centers_Out.shape[0]

		if(self.c_type=='random'):
			self.W=np.random.rand(output_n,input_n)
		elif(self.c_type=='dist_placetogrid'):
			for ii in range(Centers_In.shape[0]):
				for jj in range(Centers_Out.shape[0]):
					field_d=cdist(Centers_In[[ii],:],Centers_Out[jj,:,:].T).min()
					
					self.W[jj,ii]=np.exp(-field_d**2/(2*(par.Conn_pltogr_spread)**2))
		
		elif(self.c_type=='dist_gridtogrid'):
			for ii in range(Centers_In.shape[0]):
				for jj in range(Centers_Out.shape[0]):
					#field_d=(np.sum((Centers_In[ii,:,0]-Centers_Out[jj,:,0])**2))**0.5
					#cdist(Centers_In[[ii],:,0],Centers_Out[jj,:,0].T).min()
					field_d=cdist(Centers_In[[ii],:,[7]],Centers_Out[jj,:,:].T).min()
					self.W[jj,ii]=np.exp(-field_d**2/(2*(par.Conn_grtogr_spread)**2))
			self.W-=par.Conn_grtogr_inhib
			np.fill_diagonal(self.W, 0)					
		self.Normalize(par)