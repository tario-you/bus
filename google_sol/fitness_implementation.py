import pandas as pd
from copy import deepcopy
from random import shuffle, sample, random

df = pd.read_excel(r'assets/time_btw_stops_left.xlsx', index_col=0)
time_matrix = df.to_dict()

population_size = 100
num_generations = 10000
mutation_rate = 0.2


def fitness(individual):
    total_time = 0
    for route in individual:
        time = 0
        for i in range(len(route) - 1):
            time += time_matrix[route[i]][route[i + 1]]
        total_time += time

        total_time += min(float(dis_2_school[route[0]][0][:-2]),
                          float(dis_2_school[route[-1]][0][:-2]))

    return total_time

# Crossover function


def crossover(parent1, parent2):
    all_stops = sum(parent1, [])
    shuffle(all_stops)
    split1 = len(parent1[0])
    split2 = split1 + len(parent1[1])
    return [all_stops[:split1], all_stops[split1:split2], all_stops[split2:]]

# Mutation function


def mutate(individual):
    if random() < mutation_rate:
        route1, route2 = sample(range(3), 2)
        if individual[route1] and individual[route2]:
            index1, index2 = sample(range(len(individual[route1])), 1)[
                0], sample(range(len(individual[route2])), 1)[0]
            individual[route1][index1], individual[route2][index2] = individual[route2][index2], individual[route1][index1]


# Initialize population
population = []
for _ in range(population_size):
    shuffled_elements = deepcopy(elements_left)
    shuffle(shuffled_elements)
    split1 = len(shuffled_elements) // 3
    split2 = 2 * split1
    individual = [shuffled_elements[:split1],
                  shuffled_elements[split1:split2], shuffled_elements[split2:]]
    population.append(individual)

# Main Genetic Algorithm loop
for generation in range(num_generations):
    evaluated_population = [(fitness(ind), ind) for ind in population]
    evaluated_population.sort(key=lambda x: x[0])
    new_population = [ind for _,
                      ind in evaluated_population[:population_size // 2]]

    while len(new_population) < population_size:
        parent1, parent2 = sample(new_population, 2)
        child = crossover(parent1, parent2)
        new_population.append(child)

    for individual in new_population:
        mutate(individual)

    population = new_population

final_population = [(fitness(ind), ind) for ind in population]
final_population.sort(key=lambda x: x[0])
best_solution = final_population[0]
print(best_solution)
