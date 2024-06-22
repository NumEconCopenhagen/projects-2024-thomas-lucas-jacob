import numpy as np
from types import SimpleNamespace

def calculate_utilities():
    # Define the parameters
    par = SimpleNamespace()
    par.J = 3
    par.N = 10
    par.K = 10000
    par.F = np.arange(1, par.N + 1)
    par.sigma = 2
    par.v = np.array([1, 2, 3])
    par.c = 1

    # Generate the noise terms
    rng = np.random.default_rng(2024)
    epsilon = rng.normal(0, par.sigma**2, (par.K, par.J))

    # Function to calculate expected utility (which is just par.v)
    def expected_utility(vj):
        return vj

    # Calculate expected utility and average realized utility for each career choice
    expected_utilities = expected_utility(par.v)
    realized_utilities = par.v + epsilon

    # Store results
    results = SimpleNamespace()
    results.expected_utilities = expected_utilities
    results.realized_utilities = np.mean(realized_utilities, axis=0)

    return results

def simulate_career_choices():
    # Parameters
    par = SimpleNamespace()
    par.J = 3
    par.N = 10
    par.K = 10000
    par.sigma = 2
    par.v = np.array([1, 2, 3])
    par.c = 1

    # Preallocate arrays to store results
    career_choices = np.zeros((par.N, par.K, par.J))
    prior_exp_utilities = np.zeros((par.N, par.K, par.J))
    realized_utilities = np.zeros((par.N, par.K))

    # Arrays to store graduate shares
    graduate_shares = np.zeros((par.N, par.J))

    for i in range(par.N):
        Fi = i + 1  # Number of friends is graduate index
        for k in range(par.K):
            epsilon_friends = np.random.normal(0, par.sigma, (Fi, par.J))
            prior_exp_utilities[i, k, :] = np.mean(par.v + epsilon_friends, axis=0)
            
            chosen_career = np.argmax(prior_exp_utilities[i, k, :])
            career_choices[i, k, chosen_career] = 1
            realized_utilities[i, k] = par.v[chosen_career]
        
        # Calculate graduate shares for each career choice
        for j in range(par.J):
            graduate_shares[i, j] = np.mean(career_choices[i, :, j])

    # Calculate average realized utilities
    avg_realized_util = np.mean(realized_utilities, axis=1)

    # Calculate average subjective expected utilities
    avg_subjective_util = np.mean(np.max(prior_exp_utilities, axis=2), axis=1)

    return graduate_shares, avg_subjective_util, avg_realized_util

if __name__ == "__main__":
    # Solve Question 1
    results = calculate_utilities()
    print("Question 1 - Expected Utilities:", results.expected_utilities)
    print("Question 1 - Realized Utilities:", results.realized_utilities)

    # Solve Question 2
    share_graduates, avg_subjective_util, avg_realized_util = simulate_career_choices()
    np.savez("career_simulation_results.npz", share_graduates=share_graduates, avg_subjective_util=avg_subjective_util, avg_realized_util=avg_realized_util)
    print("Question 2 results saved to 'career_simulation_results.npz'")


