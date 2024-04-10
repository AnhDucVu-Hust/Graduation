population_generate_template= """Below is the populations (Genetic Algorithm) . Each line is genome-score and they are permutation of each other. \
Generate the new population by mutation and crossover to have a new population. Just generate the genome in each line, don't predict the score
# Population:
{previous_population}
# Population:
{current_population}
# Population:
"""