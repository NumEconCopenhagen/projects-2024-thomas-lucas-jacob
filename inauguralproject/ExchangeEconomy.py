from types import SimpleNamespace
import numpy as np

class ExchangeEconomyClass:

    def __init__(self):

        par = self.par = SimpleNamespace()

        # a. preferences 
        par.alpha = 1/3
        par.beta = 2/3

        # b. endowments
        par.w1A = 0.8
        par.w2A = 0.3
        par.w1B = 1-par.w1A
        par.w2B = 1-par.w2A

    def utility_A(self, x1A, x2A):
        par = self.par
        return x1A**par.alpha * x2A**(1-par.alpha)

    def utility_B(self, x1B, x2B):
        par = self.par
        return x1B**par.beta * x2B**(1-par.beta)

    #Define demand functions with P2 as numaire.
    def demand_A(self, p1):
        par = self.par
        I = p1 * par.w1A + 1 * par.w2A 
        return par.alpha*(I)/p1, (1-par.alpha)* (I)

    def demand_A1(self, p1):
        par = self.par
        I = p1 * par.w1A + 1 * par.w2A 
        return par.alpha*(I)/p1

    def demand_A2(self, p1):
        par = self.par
        I = p1 * par.w1A + 1 * par.w2A 
        return (1-par.alpha)* (I)

    def demand_B(self,p1):
        par = self.par
        I = p1 * par.w1B + 1 * par.w2B 
        return par.beta * (I)/p1, (1-par.beta) * (I)

    def demand_B1(self, p1):
        par = self.par
        I = p1 * par.w1B + 1 * par.w2B 
        return par.beta*(I)/p1

    def demand_B2(self, p1):
        par = self.par
        I = p1 * par.w1B + 1 * par.w2B 
        return (1-par.beta)* (I)

    def check_market_clearing(self,p1):

        par = self.par

        x1A,x2A = self.demand_A(p1)
        x1B,x2B = self.demand_B(p1)

        eps1 = x1A-par.w1A + x1B-(1-par.w1A)
        eps2 = x2A-par.w2A + x2B-(1-par.w2A)

        return eps1,eps2
    
    def find_market_clearing(self):

        # Defining p1
        price_scope = 75
        p1 = [(0.5 + 2*i/price_scope) for i in range(price_scope + 1)]

        #Estimating the errors
        errors = [self.check_market_clearing(x) for x in p1]
        eps1 = [x[0] for x in errors]
        eps2 = [x[1] for x in errors]

        #Minimizing the error rate
        index_closest_to_zero, error_min = min(enumerate(eps1), key=lambda x: abs(x[1]))

        #The price that minimze the error rate
        price = p1[index_closest_to_zero]

        #Demand for A under market clearing
        (x1A, x2A) = self.demand_A(price)

        return (price, x1A, x2A)
    
    # defining the utility function for A as a function of the price of good 1
    def utility_A2(self,p_1):
        par = self.par
        I = p_1 * par.w1A + 1 * par.w2A
        return (par.alpha*(I)/p_1)**par.alpha * ((1-par.alpha)* I)**(1-par.alpha)
    


  