import numpy as np
from scipy.spatial.distance import cdist

class Activation:
	def __init__(self,FF_Conn=np.array([]),RR_Conn=np.array([]),a_type='sample',n_type='none'):
	
		self.a_type=a_type
		self.n_type=n_type
		self.J=FF_Conn
		self.W=RR_Conn
	
	def Propagate(self,Act):
		self.ActOut=self.J.dot(Act)
		norm=sum(self.ActOut)
		self.Normalize(norm)
		if(self.a_type=='reverberation'):
			for tt in range(2):
				self.ActOut=self.J.dot(Act)+self.W.dot(self.ActOut)
				
				self.Normalize(norm)
			for tt in range(20):
				self.ActOut=self.W.dot(self.ActOut)
				
				self.Normalize(norm)
		
		
		self.Normalize(norm)
	
	def Normalize(self,norm=1):
		self.ActOut[self.ActOut<0]=0
		if (self.n_type=='mean'):
			self.ActOut=self.ActOut/sum(self.ActOut)*norm		