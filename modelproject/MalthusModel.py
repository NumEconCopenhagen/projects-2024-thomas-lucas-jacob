##### MALTUS MODEL

from scipy import optimize
from types import SimpleNamespace
import sympy as sm
import numpy as np


class Malthus():

    def __init__(self):

        par = self.par = SimpleNamespace()
        par.alpha = 0.5
        par.r = 0.05 
        par.LO = 1 
        par.D = 1
        par.p = 0.1 
    
    def Y_t(self, X, A, L):
        par = self.par

        return (A*X)**(1-par.alpha)*L**par.alpha

    def y_t(self, Y, L):
        par = self.par
        
        return Y / L
    
    def L_t(self_)

    def Lt1(self, t):
        par = self.par
        t = np.arrange(0, 1000, 1)
        return L_t*y_t*par.p - par.D*L_t
        
    












