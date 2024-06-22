from types import SimpleNamespace
import numpy as np

class problemone:
    def __init__(self):

        self.par = SimpleNamespace()
    
    def profit(p, y, w, l):
        return p*y - w*l
    
    def output(A, l, gamma):
        return A * (l**gamma)
    
    def labor_opt(p, A, gamma, w):
        x = 1/(1-gamma)
        z = (p*A*gamma)/w
        return z**x
    
    def output_opt(self, p, A, gamma, w):
        l = self.labor_opt(p, A, gamma, w)
        return A*(l**gamma)
    
    def utility(c1, c2, alpha, nu, l, epsilon):
        return np.log(((c1**alpha)*(c2**(1-alpha)))) - nu((l**(1+epsilon))/(1+epsilon))
    
    def consumption1(self, alpha, w, l, l1, l2, T, p1, p2, A, gamma):
        l1 = self.labor_opt(p1, A, gamma, w)
        y1 = self.output(A, l1, gamma)
        pr1 = self.profit(p1, y1, w, l1)
        l2 = self.labor_opt(p2, A, gamma, w)
        y2 = self.output(A, l2, gamma)
        pr2 = self.profit(p2, y2, w, l2)
        return alpha*(w*l + T + pr1 + pr2)/p1

    def consumption2(self, alpha, w, l, l1, l2, T, p1, p2, A, gamma, tau):
        l1 = self.labor_opt(p1, A, gamma, w)
        y1 = self.output(A, l1, gamma)
        pr1 = self.profit(p1, y1, w, l1)
        l2 = self.labor_opt(p2, A, gamma, w)
        y2 = self.output(A, l2, gamma)
        pr2 = self.profit(p2, y2, w, l2)
        return (1-alpha)*(w*l + T + pr1 + pr2)/(p2+tau)