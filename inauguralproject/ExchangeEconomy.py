from types import SimpleNamespace

# Har vi det hele?

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
        par.w2B = 1-par.w2B

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
        return par.alpha*(I)/p1, (1-par.alpha)* I
        

    def demand_B(self,p1):
        par = self.par
        I = p1 * par.w1B + 1 * par.w2B 
        return par.beta * I/p1, (1-par.beta) * I

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

        # 4. Getting the price where eps1 is closest to zero - the market clearing price
        price = p1[index_closest_to_zero]

        # 5. Getting the market clearing demand for consumer A
        (x1A, x2A) = self.demand_A(price)

        return (price, x1A, x2A)
    
#Printing the graph for pareto optimizing allocations. Consider changing this part to jupiter file
    
    import matplotlib.pyplot as plt
plt.rcParams.update({"axes.grid":True,"grid.color":"black","grid.alpha":"0.25","grid.linestyle":"--"})
plt.rcParams.update({'font.size': 14})

%load_ext autoreload
%autoreload 2


from ExchangeEconomy import ExchangeEconomyClass

par = model.par

# a. total endowment
w1bar = 1.0
w2bar = 1.0

# b. figure set up
fig = plt.figure(frameon=False,figsize=(6,6), dpi=100)
ax_A = fig.add_subplot(1, 1, 1)

ax_A.set_xlabel("$x_1^A$")
ax_A.set_ylabel("$x_2^A$")

temp = ax_A.twinx()
temp.set_ylabel("$x_2^B$")
ax_B = temp.twiny()
ax_B.set_xlabel("$x_1^B$")
ax_B.invert_xaxis()
ax_B.invert_yaxis()

# A
ax_A.scatter(par.w1A,par.w2A,marker='s',color='black',label='endowment')

# limits
ax_A.plot([0,w1bar],[0,0],lw=2,color='black')
ax_A.plot([0,w1bar],[w2bar,w2bar],lw=2,color='black')
ax_A.plot([0,0],[0,w2bar],lw=2,color='black')
ax_A.plot([w1bar,w1bar],[0,w2bar],lw=2,color='black')

ax_A.set_xlim([-0.1, w1bar + 0.1])
ax_A.set_ylim([-0.1, w2bar + 0.1])    
ax_B.set_xlim([w1bar + 0.1, -0.1])
ax_B.set_ylim([w2bar + 0.1, -0.1])

ax_A.legend(frameon=True,loc='upper right',bbox_to_anchor=(1.6,1.0));

print(plot)
    




