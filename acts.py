import numpy as np
from scipy.spatial.distance import cdist

class Activation:
	def __init__(self,FF_Conn=np.array([]),RR_Conn=np.array([]),a_type='sample',n_type='none'):
	
		self.a_type=a_type
		self.n_type=n_type
		self.J=FF_Conn
		self.W=RR_Conn
		
	
	def Propagate(self,Act,Noise,N_Steps):
		self.ActOut=self.J.dot(Act)
		norm=sum(self.ActOut)
		self.Normalize(norm)
		if(self.a_type=='sample'):
			self.TimeAct=np.zeros((10,self.J.shape[0]))
			for tt in range(10):
				self.ActOut=self.ActOut-0.1*(self.ActOut-(self.J.dot(Act)+np.random.standard_normal(self.J.shape[0])*Noise))
				self.Normalize(norm)
				self.TimeAct[tt,:]=self.ActOut

		if(self.a_type=='reverberation'):
			self.TimeAct=np.zeros((N_Steps,self.J.shape[0]))

			for tt in range(10):
				self.ActOut=self.ActOut-0.1*(self.ActOut-(self.J.dot(Act)+self.W.dot(self.ActOut)+np.random.standard_normal(self.J.shape[0])*Noise))
				self.Normalize(norm)
				self.TimeAct[tt,:]=self.ActOut

			for tt in range(10,N_Steps):
				self.ActOut=self.ActOut-0.1*(self.ActOut-self.W.dot(self.ActOut)-np.random.standard_normal(self.J.shape[0])*Noise)
				self.Normalize(norm)
				self.TimeAct[tt,:]=self.ActOut
		
		self.Normalize(norm)
	
	def Normalize(self,norm=1):
		self.ActOut[self.ActOut<0]=0
		if (self.n_type=='mean'):
			self.ActOut=self.ActOut/sum(self.ActOut)*norm		