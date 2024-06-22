from types import SimpleNamespace
import numpy as np
from scipy.optimize import minimize_scalar

class ProblemOne:
    def __init__(self):
        par = self.par = SimpleNamespace()

        ##parameters set up from problem tekst

        par.A = 1.0  # Technology parameter
        par.gamma = 0.5  # Output elasticity of labor
        par.alpha = 0.5  # Preference parameter for good 1
        par.nu = 1.0  # Disutility of labor parameter
        par.epsilon = 2.0  # Labor elasticity parameter
        par.tau = 0.0  # Tax rate on good 2
        par.T = 0.0  # Lump-sum transfer
        par.kappa = 0.1  # Social cost of carbon parameter

    def profit(self, p, y, w, l): #definition of the firms profit function
        return p*y - w*l
    
    def output(self, l): #firms output functions
        par = self.par
        return par.A * (l**par.gamma)
    
    def labor_opt(self, p, w): #firms optimal labor demand
        par = self.par
        x = 1/(1-par.gamma)
        z = (p*par.A*par.gamma)/w
        return z**x
    
    def output_opt(self, p, w): #firms optimal output, given the optimal labor
        par = self.par
        l = self.labor_opt(p, w)
        return par.A*(l**par.gamma)
    
    def utility(self, c1, c2, l): #Consumers utility function
        par = self.par
        return np.log((c1**par.alpha) * (c2**(1-par.alpha))) - par.nu * ((l**(1+par.epsilon)) / (1+par.epsilon))
    
    def consumption1(self, w, l, l1, l2, p1, p2): #demand for good 1 / consumption of good 1
        par = self.par
        l1 = self.labor_opt(p1, w)
        y1 = self.output(l1)
        pr1 = self.profit(p1, y1, w, l1)
        l2 = self.labor_opt(p2, w)
        y2 = self.output(l2)
        pr2 = self.profit(p2, y2, w, l2)
        return par.alpha*(w*l + par.T + pr1 + pr2)/p1

    def consumption2(self, w, l, l1, l2, p1, p2): #demand for good 2 / consumption of good 2
        par = self.par
        l1 = self.labor_opt(p1, w)
        y1 = self.output(l1)
        pr1 = self.profit(p1, y1, w, l1)
        l2 = self.labor_opt(p2, w)
        y2 = self.output(l2)
        pr2 = self.profit(p2, y2, w, l2)
        return (1-par.alpha)*(w*l + par.T + pr1 + pr2)/(p2+par.tau)
    
    def labor_supply_opt(self, w, p1, p2): #maximizing the labor supply
        def neg_utility(l): #negative utility function, for maximization of utility
            par = self.par
            l1_star = self.labor_opt(p1, w)
            y1_star = self.output_opt(p1, w)
            pi1_star = self.profit(p1, y1_star, w, l1_star)
            l2_star = self.labor_opt(p2, w)
            y2_star = self.output_opt(p2, w)
            pi2_star = self.profit(p2, y2_star, w, l2_star)
            c1 = self.consumption1(w, l, pi1_star, pi2_star, p1, p2)
            c2 = self.consumption2(w, l, pi1_star, pi2_star, p1, p2)
            return -self.utility(c1, c2, l)
        
        result = minimize_scalar(neg_utility, bounds=(0, 1e6), method='bounded') #maximizing utility function by minimizing the negative utility function
        return result.x #returns the labor l which maximises utility
    
    def labor_clear_con(self, p2, p1, w): #setting up the clearing condition for the labor market (ready for fsolve of p2)
        par = self.par
        l_star = self.labor_supply_opt(w, p1, p2)
        l1_star = self.labor_opt(p1, w)
        l2_star = self.labor_opt(p2, w)
        return l_star -(l1_star + l2_star)

    def labor_clear_con2(self, p1, p2, w): #setting up the clearing condition for the labor market (ready for fsolve of p1)
        par = self.par
        l_star = self.labor_supply_opt(w, p1, p2)
        l1_star = self.labor_opt(p1, w)
        l2_star = self.labor_opt(p2, w)
        return l_star -(l1_star + l2_star)

    def good1_clear_con(self, p2, p1, w): #setting up the clearing condition for the good 1 market (ready for fsolve of p2)
        par = self.par
        l_star = self.labor_supply_opt(w, p1, p2)
        l1_star = self.labor_opt(p1, w)
        y1_star = self.output_opt(p1, w)
        pi1_star = self.profit(p1, y1_star, w, l1_star)
        l2_star = self.labor_opt(p2, w)
        y2_star = self.output_opt(p2, w)
        pi2_star = self.profit(p2, y2_star, w, l2_star)
        c1 = self.consumption1(w, l_star, pi1_star, pi2_star, p1, p2)
        return y1_star - c1
    
    def good1_clear_con2(self, p1, p2, w): #setting up the clearing condition for the good 1 market (ready for fsolve of p1)
        par = self.par
        l_star = self.labor_supply_opt(w, p1, p2)
        l1_star = self.labor_opt(p1, w)
        y1_star = self.output_opt(p1, w)
        pi1_star = self.profit(p1, y1_star, w, l1_star)
        l2_star = self.labor_opt(p2, w)
        y2_star = self.output_opt(p2, w)
        pi2_star = self.profit(p2, y2_star, w, l2_star)
        c1 = self.consumption1(w, l_star, pi1_star, pi2_star, p1, p2)
        return y1_star - c1

    def good2_clear_con(self, p2, p1, w): #setting up the clearing condition for the good 2 market (ready for fsolve of p2)
        par = self.par
        l_star = self.labor_supply_opt(w, p1, p2)
        l1_star = self.labor_opt(p1, w)
        y1_star = self.output_opt(p1, w)
        pi1_star = self.profit(p1, y1_star, w, l1_star)
        l2_star = self.labor_opt(p2, w)
        y2_star = self.output_opt(p2, w)
        pi2_star = self.profit(p2, y2_star, w, l2_star)
        c2 = self.consumption1(w, l_star, pi1_star, pi2_star, p1, p2)
        return y2_star - c2
    
    def good2_clear_con2(self, p1, p2, w): #setting up the clearing condition for the good 2 market (ready for fsolve of p1)
        par = self.par
        l_star = self.labor_supply_opt(w, p1, p2)
        l1_star = self.labor_opt(p1, w)
        y1_star = self.output_opt(p1, w)
        pi1_star = self.profit(p1, y1_star, w, l1_star)
        l2_star = self.labor_opt(p2, w)
        y2_star = self.output_opt(p2, w)
        pi2_star = self.profit(p2, y2_star, w, l2_star)
        c2 = self.consumption1(w, l_star, pi1_star, pi2_star, p1, p2)
        return y2_star - c2