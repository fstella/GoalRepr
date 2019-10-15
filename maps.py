import numpy as np


class PlaceRepresentation:

	def __init__(self,par):
		self.Place_Centers=np.zeros((par.N_hc,2))
		self.RateMap=np.zeros((par.RateMap_resol,par.RateMap_resol,par.N_hc))

	def New_Map(self,par):
		if(par.Env_shape=='circle'):
			RR=np.random.rand(par.N_hc)*par.Env_size/2
			AA=np.random.rand(par.N_hc)*np.pi*2
			self.Place_Centers[:,0]=np.sqrt(RR/(par.Env_size/2))*np.cos(AA)*par.Env_size/2
			self.Place_Centers[:,1]=np.sqrt(RR/(par.Env_size/2))*np.sin(AA)*par.Env_size/2
		elif(par.Env_shape=='square'):
			self.Place_Centers[:,0]=np.random.rand(par.N_hc)*par.Env_size-par.Env_size/2
			self.Place_Centers[:,1]=np.random.rand(par.N_hc)*par.Env_size-par.Env_size/2

	def Remap(self,par):
		remapping=np.random.rand(par.N_hc)
		remapping[remapping<(1-par.Remap_prob)]=0
		remapping[remapping>0]=1
		ch_place=np.where(remapping)[0]
		for cc in ch_place:
			goal_disp=[np.random.rand(1)*1, np.random.rand(1)*np.pi*2]
			goal_disp=goal_disp[0]*[np.cos(goal_disp[1]), np.sin(goal_disp[1])]
			self.Place_Centers[cc,:]=goal_disp.ravel()

	def Generate_RateMap(self,par):
		[x_samp,y_samp]=np.meshgrid(np.linspace(0,par.Env_size,par.RateMap_resol)-par.Env_size/2,np.linspace(0,par.Env_size,par.RateMap_resol)-par.Env_size/2)
		x_samp=np.ndarray.flatten(x_samp)
		y_samp=np.ndarray.flatten(y_samp)
		Act_Map=np.zeros((x_samp.size,par.N_hc))
		
		for pp in range(x_samp.size):
			Act_Map[pp,:]=self.Activity(par,x_samp[pp],y_samp[pp])

		
		self.RateMap=np.reshape(Act_Map,(par.RateMap_resol,par.RateMap_resol,-1))

	def Activity(self,par,x,y):
		D_Act=(self.Place_Centers[:,0]-x)**2+(self.Place_Centers[:,1]-y)**2
		Act=par.Place_h*np.exp(-D_Act/(2*par.Place_s**2))

		return Act

class GridRepresentation:

	def __init__(self,par,layer='deep'):
		if(layer=='deep'):
			self.N_ec=par.N_ec_deep
		elif(layer=='superficial'):
			self.N_ec=par.N_ec_supe	

		Latt_Rep=int(np.ceil(par.Env_size/par.Grid_spacing/2));
		self.N_field_grid=(Latt_Rep*2+1)*((Latt_Rep+1)*2+1);
		zz=0
		self.Grid_lattice=np.zeros((2,self.N_field_grid))
		for ii in range(-Latt_Rep,Latt_Rep+1):
			for jj in range(-Latt_Rep-1,Latt_Rep+2):
				self.Grid_lattice[0,zz]=0-par.Grid_spacing/2*np.mod(jj,2)+ii*par.Grid_spacing
				self.Grid_lattice[1,zz]=0+par.Grid_spacing/np.sqrt(2)*jj
				zz+=1
		

		self.Grid_Centers=np.zeros((self.N_ec,2,self.N_field_grid))
		self.RateMap=np.zeros((par.RateMap_resol,par.RateMap_resol,self.N_ec))

	def New_Map(self,par):
		nx, ny = (np.sqrt(self.N_ec), np.sqrt(self.N_ec))
		X = np.linspace(0, 1, nx)
		Y = np.linspace(0, 1, ny)
		XX, YY = np.meshgrid(X, Y)
		XX=np.reshape(XX,(self.N_ec,1))
		YY=np.reshape(YY,(self.N_ec,1))
		#XX=np.random.rand(self.N_ec,1)
		#YY=np.random.rand(self.N_ec,1)
		self.Grid_Centers[:,0,0]=(XX*par.Grid_spacing+YY*par.Grid_spacing/2).ravel()
		self.Grid_Centers[:,1,0]=(YY*par.Grid_spacing*1/np.sqrt(2)).ravel()


		for uu in range(self.Grid_Centers.shape[0]):
			self.Grid_Centers[uu,:,:]=np.tile(self.Grid_Centers[uu,:,0:1],(1,self.Grid_lattice.shape[1]))+self.Grid_lattice

	def Generate_RateMap(self,par):
		[x_samp,y_samp]=np.meshgrid(np.linspace(0,par.Env_size,par.RateMap_resol)-par.Env_size/2,np.linspace(0,par.Env_size,par.RateMap_resol)-par.Env_size/2)
		x_samp=np.ndarray.flatten(x_samp)
		y_samp=np.ndarray.flatten(y_samp)
		Act_Map=np.zeros((x_samp.size,self.N_ec))
		
		for pp in range(x_samp.size):
			Act_Map[pp,:]=self.Activity(par,x_samp[pp],y_samp[pp])

		
		self.RateMap=np.reshape(Act_Map,(par.RateMap_resol,par.RateMap_resol,-1))

	def Activity(self,par,x,y):
		D_Act=((self.Grid_Centers[:,0,:]-x)**2+(self.Grid_Centers[:,1,:]-y)**2).min(axis=1)
		Act=par.Grid_h*np.exp(-D_Act/(2*par.Grid_s**2))

		return Act
	

						


