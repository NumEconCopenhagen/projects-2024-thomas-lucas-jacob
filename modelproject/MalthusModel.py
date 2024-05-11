

##### MALTUS MODEL

from scipy import optimize
from types import SimpleNamespace
import sympy as sm
import numpy as np


class Malthus:

    def __init__(self):

        par = self.par = SimpleNamespace()
        par.alpha = 0.5
        par.r = 0.05
        par.LO = 1
    
    def Y(self, X, A, L):
        par = self.par

        return (A*X)**(1-par.alpha)*L**par.alpha

    def y(self, X, A, L):
        par = self.par
        
        return (A*X/L)**par.alpha

    def L(self, t):
        par = self.par
        t = np.arrange(0, 1000, 1)
        return par.LO*exp(par.r*t)*y 
        












