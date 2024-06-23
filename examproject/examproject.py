from types import SimpleNamespace
import numpy as np
from scipy.optimize import minimize_scalar

class ProblemOne:
    def __init__(self):
        par = self.par = SimpleNamespace()

        ##parameters set up from problem tekst

        par.A = 1.0  # Technology parameter
        par.gamma = 0.5  # Output elasticity of labor
        par.alpha = 0.3  # Preference parameter for good 1
        par.nu = 1.0  # Disutility of labor parameter
        par.epsilon = 2.0  # Labor elasticity parameter
        par.tau = 0.0  # Tax rate on good 2
        par.T = 0.0  # Lump-sum transfer
        par.kappa = 0.1  # Social cost of carbon parameter
        par.w = 1

    def profit(self, p, y, l): #definition of the firms profit function
        par = self.par
        return p*y - par.w*l
    
    def output(self, l): #firms output functions
        par = self.par
        return par.A * (l**par.gamma)
    
    def labor_opt(self, p): #firms optimal labor demand
        par = self.par
        x = 1/(1-par.gamma)
        z = (p*par.A*par.gamma)/par.w
        return z**x
    
    def output_opt(self, p): #firms optimal output, given the optimal labor
        par = self.par
        l = self.labor_opt(p)
        return par.A*(l**par.gamma)
    
    def profit_opt(self, p):
        par = self.par
        l = self.labor_opt(p)
        c = (1 - par.gamma) / par.gamma
        return c * par.w * l
    
    def utility(self, c1, c2, l): #Consumers utility function
        par = self.par
        return np.log((c1**par.alpha) * (c2**(1-par.alpha))) - par.nu * ((l**(1+par.epsilon)) / (1+par.epsilon))
    
    def consumption1(self, l, p1, p2): #demand for good 1 / consumption of good 1
        par = self.par
        pr1 = self.profit_opt(p1)
        pr2 = self.profit_opt(p2)
        return par.alpha*(par.w*l + par.T + pr1 + pr2)/p1

    def consumption2(self, l, p1, p2): #demand for good 2 / consumption of good 2
        par = self.par
        pr1 = self.profit_opt(p1)
        pr2 = self.profit_opt(p2)
        return (1-par.alpha)*(par.w*l + par.T + pr1 + pr2)/(p2+par.tau)
    
    def labor_supply_opt(self, p1, p2): #maximizing the labor supply
        def neg_utility(l): #negative utility function, for maximization of utility
            par = self.par
            c1 = self.consumption1(l, p1, p2)
            c2 = self.consumption2(l, p1, p2)
            return -self.utility(c1, c2, l)
        
        result = minimize_scalar(neg_utility, bounds=(0, 1e6), method='bounded') #maximizing utility function by minimizing the negative utility function
        return result.x #returns the labor l which maximises utility
    
    def market_clearing_errors(self, p1, p2):
        par=self.par
        l_star = self.labor_supply_opt(p1, p2)
        l1_star = self.labor_opt(p1)
        l2_star = self.labor_opt(p2)
        labor = l_star - (l1_star + l2_star)

        y1_star = self.output_opt(p1)
        y2_star = self.output_opt(p2)
        c1 = self.consumption1(l_star, p1, p2)
        c2 = self.consumption2(l_star, p1, p2)
        good1 = y1_star - c1
        good2 = y2_star - c2

        return [labor, good1, good2]

    def market_clearing_l_1(self, vars):
        p1, p2 = vars
        par=self.par
        l_star = self.labor_supply_opt(p1, p2)
        l1_star = self.labor_opt(p1)
        l2_star = self.labor_opt(p2)
        labor = l_star - (l1_star + l2_star)

        y1_star = self.output_opt(p1)
        c1 = self.consumption1(l_star, p1, p2)
        good1 = y1_star - c1
        return [labor, good1]
    
    def market_clearing_l_2(self, vars):
        p1, p2 = vars
        par=self.par
        l_star = self.labor_supply_opt(p1, p2)
        l1_star = self.labor_opt(p1)
        l2_star = self.labor_opt(p2)
        labor = l_star - (l1_star + l2_star)

        y2_star = self.output_opt(p2)
        c2 = self.consumption2(l_star, p1, p2)
        good2 = y2_star - c2

        return [labor, good2]
    
    def market_clearing_1_2(self, vars):
        p1, p2 = vars
        par=self.par
        l_star = self.labor_supply_opt(p1, p2)
        y1_star = self.output_opt(p1)
        y2_star = self.output_opt(p2)
        c1 = self.consumption1(l_star, p1, p2)
        c2 = self.consumption2(l_star, p1, p2)
        good1 = y1_star - c1
        good2 = y2_star - c2

        return [good1, good2]
    
    def labor_supply_opt_t(self, tau, p1, p2): #maximizing the labor supply
        def neg_utility(l): #negative utility function, for maximization of utility
            par = self.par
            T = tau / self.output_opt(p2)
            pr1 = self.profit_opt(p1)
            pr2 = self.profit_opt(p2)
            c1 = par.alpha*(par.w*l + T + pr1 + pr2)/p1
            c2 = (1-par.alpha)*(par.w*l + T + pr1 + pr2)/(p2+tau)
            return -self.utility(c1, c2, l)
        
        result = minimize_scalar(neg_utility, bounds=(0, 1e6), method='bounded') #maximizing utility function by minimizing the negative utility function
        return result.x #returns the labor l which maximises utility
    
    def SWF(self, vars):
        tau, p1, p2 = vars
        par = self.par
        T = tau / self.output_opt(p2)
        pr1 = self.profit_opt(p1)
        pr2 = self.profit_opt(p2)
        l = self.labor_supply_opt_t(tau, p1, p2)
        c1 = par.alpha*(par.w*l + T + pr1 + pr2)/p1
        c2 = (1-par.alpha)*(par.w*l + T + pr1 + pr2)/(p2+tau)

        U = self.utility(c1, c2, l)

        y2_star = self.output_opt(p2)

        return U - par.kappa * y2_star
    
    def neq_SWF(self, vars):
        par = self.par
        return -self.SWF(vars)