##### MALTUS MODEL

from scipy import optimize
from types import SimpleNamespace
import sympy as sm
import numpy as np


class Malthus():

    def __init__(self):

        par = self.par = SimpleNamespace()
        par.anul = 0.5
        par.a = 0.05 
        par.bnul = 1 
        par.b = 1
        par.dnul = 0.1 
        par.d = 0.1
    
    def Yt(self, Lt):
        par = self.par
        return par.anul-par.a* Lt

    def Bt(self, Lt):
        par = self.par
        Yt = self.Yt(Lt)
        return (par.bnul + par.b* Yt)* Lt
    
    def Dt(self, Lt):
        par = self.par
        Yt = self.Yt(Lt)
        return (par.dnul + par.d* Yt)* Lt

    def Lt1(self, Lt):
        par = self.par
        Yt= self.Yt(Lt)
        Bt= self.Bt(Lt)
        Dt= self.Dt(Lt)
        L= Lt + Bt + Dt
        return L, Yt, Bt, Dt










    #def Y_t(self, X, A, L):
     #   par = self.par

      #  return (A*X)**(1-par.alpha)*L**par.alpha

    #def y_t(self, Y, L):
     #   par = self.par
        
      #  return Y / L
    
    #def L_t(self_)

    #def Lt1(self, t):
     #   par = self.par
      #  t = np.arrange(0, 1000, 1)
       # return L_t*y_t*par.p - par.D*L_t
        
    












