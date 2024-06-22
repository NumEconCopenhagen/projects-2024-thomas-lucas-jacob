from types import SimpleNamespace
import numpy as np

class ProblemOne:
    def __init__(self):
        par = self.par = SimpleNamespace()
        par.A = 1.0  # Technology parameter
        par.gamma = 0.5  # Output elasticity of labor
        par.alpha = 0.3  # Preference parameter for good 1
        par.nu = 1.0  # Disutility of labor parameter
        par.epsilon = 2.0  # Labor elasticity parameter
        par.tau = 0.0  # Tax rate on good 2
        par.T = 0.0  # Lump-sum transfer
        par.kappa = 0.1  # Social cost of carbon parameter

    def profit(self, p, y, w, l):
        return p*y - w*l
    
    def output(self, l):
        par = self.par
        return par.A * (l**par.gamma)
    
    def labor_opt(self, p, w):
        par = self.par
        x = 1/(1-par.gamma)
        z = (p*par.A*par.gamma)/w
        return z**x
    
    def output_opt(self, p, w):
        par = self.par
        l = self.labor_opt(p, w)
        return par.A*(l**par.gamma)
    
    def utility(self, c1, c2, l):
        par = self.par
        return np.log((c1**par.alpha) * (c2**(1-par.alpha))) - par.nu * ((l**(1+par.epsilon)) / (1+par.epsilon))
    
    def consumption1(self, w, l, l1, l2, p1, p2):
        par = self.par
        l1 = self.labor_opt(p1, w)
        y1 = self.output(l1)
        pr1 = self.profit(p1, y1, w, l1)
        l2 = self.labor_opt(p2, w)
        y2 = self.output(l2)
        pr2 = self.profit(p2, y2, w, l2)
        return par.alpha*(w*l + par.T + pr1 + pr2)/p1

    def consumption2(self, w, l, l1, l2, p1, p2):
        par = self.par
        l1 = self.labor_opt(p1, w)
        y1 = self.output(l1)
        pr1 = self.profit(p1, y1, w, l1)
        l2 = self.labor_opt(p2, w)
        y2 = self.output(l2)
        pr2 = self.profit(p2, y2, w, l2)
        return (1-par.alpha)*(w*l + par.T + pr1 + pr2)/(p2+par.tau)