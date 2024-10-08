from generate_genotype_data import generate_genotype_data

from calc_N import calc_N
from calc_next_N import calc_next_N
from calc_N_sub import calc_N_sub

from adj_by_fitness import adj_by_fitness
from adj_by_drift import adj_by_drift
from adj_by_mutation import adj_by_mutation

from calc_next_genotypes_data import calc_next_genotypes_data

from calc_genotype_counts import calc_genotype_counts
from calc_genotype_frequencies import calc_genotype_frequencies
from calc_allele_counts import calc_allele_counts
from calc_allele_frequencies import calc_allele_frequencies
from calc_population_sizes import calc_population_sizes
from calc_avgerage_fitness import calc_avgerage_fitness

from calc_Ne import calc_Ne_over_generations

from plot import create_plot

class PopGen:
    def __init__(self):
        """
        The PopGen class simulates population genetics over multiple generations.
        It models the evolution of genotype data based on various evolutionary forces such as fitness,
        drift, mutation, etc. The class includes methods for running simulations, generating genotype data,
        and visualizing the results. The latter includes functionality to plot various aspects of the
        simulation, including genotype counts, allele frequencies, population sizes, and effective population sizes.

        Public Attributes:
         - growth_rate (float): The growth rate of the population (default 0, no population growth).
         - carrying_capacity (int): The carrying capacity of the population (default None, no limit).
         - max_drift (float): The maximum drift rate for allele frequencies (default 0, no drift).
         - mutation_rate (float): The mutation rate for alleles (default None, no mutation).
         - genotype_data (dict): The genotype data for the current generation.

        Private Attributes:
         - _gens_genotype_data (list): A list of genotype data for each generation.

        """
        self.growth_rate = 0
        self.carrying_capacity = None
        self.max_drift = 0
        self.mutation_rate = None
        self.genotype_data = None
        self._gens_genotype_data = []
    
    def run(self, generations, bottleneck_yr=None, bottleneck_N=None):
        """
        Runs the simulation for the specified number of generations.
        """
        if self.genotype_data is None:
            raise ValueError("Genotype data must be provided")
        
        # Repeates for each generation
        for i in range(generations):
            self.calc_generation(i, bottleneck_yr, bottleneck_N)

        return self._gens_genotype_data

    def calc_generation(self, i, bottleneck_yr=None, bottleneck_N=None):
        """
        Calculates the genotype data for the next generation.
        """
        
        # Append the next generation to the list of generations
        self._gens_genotype_data.append(self.genotype_data)

        curr_genotypes_data = self._gens_genotype_data[-1]
        next_N = calc_next_N(calc_N(curr_genotypes_data), self.growth_rate, self.carrying_capacity)

        # Apply evolutionary forces to genotypes in the current generation
        curr_genotypes_data = adj_by_fitness(curr_genotypes_data)
        curr_genotypes_data = adj_by_drift(curr_genotypes_data, self.max_drift, calc_N(curr_genotypes_data), self.carrying_capacity)

        # If bottleneck, adjust population size, apply drift
        if bottleneck_yr == i and next_N > bottleneck_N:
            curr_genotypes_data = adj_by_drift(curr_genotypes_data, 1-bottleneck_N/next_N, bottleneck_N, self.carrying_capacity)
            next_N = bottleneck_N

        # Calculate the next generation
        self.genotype_data = calc_next_genotypes_data(curr_genotypes_data, next_N)
        self.genotype_data = adj_by_mutation(self.genotype_data, self.mutation_rate)
    
    def generate_genotype_data(self, *args, **kargs):
        """
        Generates genotype data based on the specified arguments.
        """
        return generate_genotype_data(*args, **kargs)
    
    def plot_genotype_counts(self):
        """
        Plots the population size of each genotype over generations.
        """

        fig = create_plot('Genotype Counts', calc_genotype_counts(self._gens_genotype_data), 'Count')
        fig.show()
    
    def plot_genotype_frequencies(self):
        """
        Plots the frequency of each genotype over generations.
        """
        fig = create_plot('Genotype Frequencies', calc_genotype_frequencies(self._gens_genotype_data), 'Frequency')
        fig.show()

    def plot_allele_counts(self):
        """
        Plots the counts of each allele over generations.
        """
        fig = create_plot('Allele Counts', calc_allele_counts(self._gens_genotype_data), 'Count')
        fig.show()

    def plot_allele_frequencies(self):
        """
        Plots the frequencies of each allele over generations.
        """
        fig = create_plot('Allele Frequencies', calc_allele_frequencies(self._gens_genotype_data), 'Frequency')
        fig.show()
    
    def plot_population_sizes(self):
        """
        Plots the population sizes over generations.
        """
        fig = create_plot('Population Size', calc_population_sizes(self._gens_genotype_data), 'Population Sizes')
        fig.show()
    
    def plot_effective_population_sizes(self):
        """
        Plots the effective population sizes over generations.
        """
        gens_Nm = calc_N_sub(self._gens_genotype_data, 'Nm')
        gens_Nf = calc_N_sub(self._gens_genotype_data, 'Nf')
        gens_allele_freqs = calc_allele_frequencies(self._gens_genotype_data)

        gens_Ne = calc_Ne_over_generations(gens_Nm, gens_Nf, gens_allele_freqs)

        fig = create_plot('Effective Population Size', gens_Ne, 'Effective Population Size')
        fig.show()
    
    def plot_average_fitness(self):
        """
        Plots the average fitness over generations.
        """
        fig = create_plot('Average Fitness', calc_avgerage_fitness(self._gens_genotype_data), 'Fitness')
        fig.show()