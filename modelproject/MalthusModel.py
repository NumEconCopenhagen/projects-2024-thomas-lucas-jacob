##### MALTUS MODEL

from scipy import optimize
from types import SimpleNamespace
import sympy as sm
import numpy as np


class Malthus_analytical():

    def __init__(self):

        par = self.par = SimpleNamespace()
        par.A = sm.symbols('A')
        par.X = sm.symbols('X')
        par.alpha = sm.symbols('alpha')
        par.eta = sm.symbols('eta')
        par.L_t = sm.symbols('L_t')
        par.mu = sm.symbols('mu')

    def L_function(self):
        par = self.par
        Y_t = (par.A*par.X)**(1-par.alpha)*par.L_t**par.alpha
        n_t = par.eta * Y_t/par.L_t
        return (n_t * par.L_t) + (1-par.mu * par.L_t)
    
    def L_function_ss(self):
        par = self.par
        ss_function = sm.Eq(par.L_t, self.L_function())
        return sm.solve(ss_function, par.L_t)[0]
    
    def lmb_L(self):
        par = self.par
        return sm.lambdify(par.A, par.X, par.alpha, par.eta, par.mu, self.L_function_ss(), 'numpy')


class Malthus_cobbd():

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
        return nt * Lt + (1 - par.mu) * Lt

    def ss_conditions(self, vars, eta):
        L, Y = vars
        return [self.Yt(L) - Y, self.Lt1(L, eta) - L]




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
        
    












