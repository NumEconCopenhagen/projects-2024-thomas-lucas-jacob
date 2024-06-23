from types import SimpleNamespace
import numpy as np
from scipy.optimize import minimize_scalar

class ProblemOne:
    ####### Class for Problem 1, question 1 to 3 #######
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
    
    def profit_opt(self, p): #firms optimal profit definition
        par = self.par
        l = self.labor_opt(p)
        c = (1 - par.gamma) / par.gamma
        return c * par.w * l
    
    def utility(self, c1, c2, l): #Consumers utility function
        par = self.par
        return np.log((c1**par.alpha) * (c2**(1-par.alpha))) - (par.nu * ((l**(1+par.epsilon)) / (1+par.epsilon)))
    
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
    
    def market_clearing_errors(self, p1, p2): #defining the market clearing errors (clearing condition difference from 0)
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

    def market_clearing_l_1(self, vars): # defining market clearing errors for labor- and good 1 market. To be used for equilibrium optimization
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
    
    def market_clearing_l_2(self, vars): # defining market clearing errors for labor- and good 2 market. To be used for equilibrium optimization
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
    
    def market_clearing_1_2(self, vars): # defining market clearing errors for good 1- and good 2 market. To be used for equilibrium optimization
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
    
    def labor_supply_opt_t(self, tau, p1, p2): #maximizing the labor supply tau variable
        def neg_utility(l): #negative utility function, for maximization of utility
            par = self.par
            T = tau / self.output_opt(p2) #T as a function of tau and consumption of y2
            pr1 = self.profit_opt(p1)
            pr2 = self.profit_opt(p2)
            c1 = par.alpha*(par.w*l + T + pr1 + pr2)/p1
            c2 = (1-par.alpha)*(par.w*l + T + pr1 + pr2)/(p2+tau)
            return -self.utility(c1, c2, l)
        
        result = minimize_scalar(neg_utility, bounds=(0, 1e6), method='bounded') #maximizing utility function by minimizing the negative utility function
        return result.x #returns the labor l which maximises utility
    
    def SWF(self, vars): #defining Social Welfare Function, variable on tau and product prices
        tau, p1, p2 = vars
        par = self.par
        T = tau / self.output_opt(p2) #T as a function of tau and consumption of y2
        pr1 = self.profit_opt(p1)
        pr2 = self.profit_opt(p2)
        l = self.labor_supply_opt_t(tau, p1, p2)
        c1 = par.alpha*(par.w*l + T + pr1 + pr2)/p1
        c2 = (1-par.alpha)*(par.w*l + T + pr1 + pr2)/(p2+tau)

        U = self.utility(c1, c2, l)

        y2_star = self.output_opt(p2)

        return U - par.kappa * y2_star
    
    def neq_SWF(self, vars): # negative SWF to be used in optimization.
        par = self.par
        return -self.SWF(vars)
    
#Problemset 2 - Question 1

# Make a function for calculate utilies, we make a expected utility and realized utility function
def calculate_utilities():
    # Define the parameters using SimpleNamespace
    par = SimpleNamespace()
    par.J = 3  # Number of career choices
    par.N = 10  # Number of graduates
    par.K = 10000  # Number of simulations
    par.F = np.arange(1, par.N + 1)  # Array of integers from 1 to N
    par.sigma = 2  # Standard deviation for noise terms.
    par.v = np.array([1, 2, 3])  # Array of utilities for career choices
    par.c = 1  # Switching cost
    
    # Generate the noise terms (error term) for simulations
    rng = np.random.default_rng(2024)
    epsilon = rng.normal(0, par.sigma, (par.K, par.J))
    
    # Function to calculate expected utility
    # Which is just par.v, as the expected value of the error noise term is 0
    def expected_utility(vj):
        return vj
    
    # Calculate expected utility and average realized utility for each career choice
    expected_utilities = expected_utility(par.v)
    realized_utilities = par.v + epsilon
    
    # Store results in SimpleNamespace
    results = SimpleNamespace()
    results.expected_utilities = expected_utilities
    results.realized_utilities = np.mean(realized_utilities, axis=0)
    
    #Returns results so we can show it later in Jupiter
    return results

    # Solve Question 1
    results = calculate_utilities()
    print("Question 1 - Expected Utilities:", results.expected_utilities)
    print("Question 1 - Realized Utilities:", results.realized_utilities)

# Problemset 2 - Question 2

def simulate_career_choices():
    # Parameters using SimpleNamespace
    par = SimpleNamespace()
    par.J = 3  # Number of career choices
    par.N = 10  # Number of graduates
    par.K = 10000  # Number of simulations
    par.sigma = 2  # Standard deviation for noise terms
    par.v = np.array([1, 2, 3])  # Array of utilities for career choices
    par.c = 1  # Switching cost
    
    # Preallocate arrays to store results
    career_choices = np.zeros((par.N, par.K, par.J))
    prior_expected_utilities = np.zeros((par.N, par.K, par.J))
    realized_utilities = np.zeros((par.N, par.K))
    
    # Arrays to store graduate shares
    graduate_shares = np.zeros((par.N, par.J))
    
    # Loop through each graduate from i=1 to i=10.
    for i in range(par.N):
        F = i + 1  # Number of friends is graduate index
        # Simulate career choice for each simulation
        for k in range(par.K):
            epsilon_friends = np.random.normal(0, par.sigma, (F, par.J))
            prior_expected_utilities[i, k, :] = np.mean(par.v + epsilon_friends, axis=0)
            
            # Below we find the career choice that maximize utility for each simulations
            chosen_career = np.argmax(prior_expected_utilities[i, k, :])
            career_choices[i, k, chosen_career] = 1
            realized_utilities[i, k] = par.v[chosen_career]
        
        # Calculate graduate shares for each career choice
        for j in range(par.J):
            graduate_shares[i, j] = np.mean(career_choices[i, :, j])
            # We expect the graduate share of j=3 to be higher for i=10 than i=1 as the latter have less friends to collect info.
    
    # Calculate average realized utilities
    average_realized_utility = np.mean(realized_utilities, axis=1)
    
    # Calculate average subjective expected utilities
    average_subjective_utility = np.mean(np.max(prior_expected_utilities, axis=2), axis=1)
    
    # We return the functions
    return graduate_shares, average_subjective_utility, average_realized_utility
 

# Problemset 2 - Question 3 

def simulate_career_choices_with_switch():
    # Parameters using SimpleNamespace
    par = SimpleNamespace()
    par.J = 3  # Number of career choices
    par.N = 10  # Number of graduates
    par.K = 10000  # Number of simulations
    par.sigma = 2  # Standard deviation for noise terms
    par.v = np.array([1, 2, 3])  # Array of utilities for career choices
    par.c = 1  # Switching cost
    
    # Preallocate arrays to store results
    career_choices = np.zeros((par.N, par.K, par.J))
    prior_expected_utilities = np.zeros((par.N, par.K, par.J))
    realized_utilities = np.zeros((par.N, par.K))
    new_realized_utilities = np.zeros((par.N, par.K))
    switch_decisions = np.zeros((par.N, par.K))
    final_graduate_counts = np.zeros((par.N, par.J))  # Initialize final graduate counts
    
    # Arrays to store graduate shares
    graduate_shares = np.zeros((par.N, par.J))
    
    # Loop through each graduate
    for i in range(par.N):
        F = i + 1  # Number of friends is graduate index
        # Simulate career choice for each simulation
        for k in range(par.K):
            epsilon_friends = np.random.normal(0, par.sigma, (F, par.J))
            prior_expected_utilities[i, k, :] = np.mean(par.v + epsilon_friends, axis=0)
            
            chosen_career = np.argmax(prior_expected_utilities[i, k, :])
            career_choices[i, k, chosen_career] = 1
            realized_utilities[i, k] = par.v[chosen_career]
            
            # Simulate the perfect information after a year
            true_utilities = par.v + np.random.normal(0, par.sigma, par.J)
            new_expected_utilities = np.copy(prior_expected_utilities[i, k, :])
            new_expected_utilities[chosen_career] = true_utilities[chosen_career]
            
            # Apply the switching cost
            new_expected_utilities[chosen_career != np.arange(par.J)] -= par.c
            
            # Decide whether to switch
            new_chosen_career = np.argmax(new_expected_utilities)
            new_realized_utilities[i, k] = min(true_utilities[new_chosen_career], 3)
            
            if new_chosen_career != chosen_career:
                switch_decisions[i, k] = 1
        
        # Calculate graduate shares for each career choice
        graduate_shares[i, :] = np.mean(career_choices[i, :, :], axis=0)
        
        # Calculate final graduate shares after the switching decision
        # This calculates the share of graduates in each career after allowing for switching
        for j in range(par.J):
            final_graduate_counts[i, j] = np.sum(career_choices[i, :, j] * (1 - switch_decisions[i, :]))
        
        # Normalize to get shares instead of counts
        if np.sum(final_graduate_counts[i, :]) > 0:
            final_graduate_counts[i, :] /= np.sum(final_graduate_counts[i, :])
    
    # Calculate average realized utilities
    average_realized_utility = np.mean(realized_utilities, axis=1)
    average_new_realized_utility = np.mean(new_realized_utilities, axis=1)
    
    # Calculate average subjective expected utilities
    average_subjective_utility = np.mean(np.max(prior_expected_utilities, axis=2), axis=1)
    
    # Calculate switch rates based on initial career choice
    switch_rates = np.zeros((par.N, par.J))
    for i in range(par.N):
        for j in range(par.J):
            initial_career_indices = np.where(career_choices[i, :, j] == 1)[0]
            if len(initial_career_indices) > 0:
                switch_rates[i, j] = np.mean(switch_decisions[i, initial_career_indices])
            else:
                switch_rates[i, j] = 0
    
    # Return graduate shares, average utilities, switch rates, and final graduate shares
    return graduate_shares, average_subjective_utility, average_realized_utility, average_new_realized_utility, switch_rates, final_graduate_counts