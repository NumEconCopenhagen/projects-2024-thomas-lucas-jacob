##### MALTUS MODEL

# We import the relevant imports
from scipy import optimize
from types import SimpleNamespace
import sympy as sm
import numpy as np

# we create the model with class
class Malthus_cobbd():

    # We define the functions used in the malthus model with parameters guesses. Later you can change the parameters with a sliding scale.
    def __init__(self):

        par = self.par = SimpleNamespace()
        par.alpha = 0.85
        par.A = 1.5
        par.X = 1
        par.mu = 0.1
    
    def Yt(self, Lt):
        par=self.par
        return ((par.A*par.X)**(1- par.alpha))*(Lt**par.alpha)
    
    def yt(self, Lt):
        Yt = self.Yt(Lt)
        return Yt/Lt

    def nt(self, eta, Lt):
        yt = self.yt(Lt)
        return eta * yt
    
    def Lt1(self, Lt, eta):
        par=self.par
        nt = self.nt(eta, Lt)
        return (nt * Lt) + ((1 - par.mu) * Lt)

    def ss_conditions(self, vars, eta):
        L, Y = vars
        return [self.Yt(L) - Y, self.Lt1(L, eta) - L]

    












