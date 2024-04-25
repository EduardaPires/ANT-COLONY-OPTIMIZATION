import numpy as np

# Função de Ackley
def ackley_function(x):
    n = len(x)
    sum1 = np.sum(x**2)
    sum2 = np.sum(np.cos(2 * np.pi * x))
    return -20 * np.exp(-0.2 * np.sqrt(sum1 / n)) - np.exp(sum2 / n) + 20 + np.e

# Função para inicializar as formigas
def initialize_ants(num_ants, num_dimensions, search_space):
    ants = []
    for _ in range(num_ants):
        ant = np.random.uniform(search_space[0], search_space[1], num_dimensions)
        ants.append(ant)
    return ants

# Função para escolher o próximo movimento da formiga
def choose_next_move(current_position, pheromones, search_space, alpha=1.0, beta=1.0):
    num_dimensions = len(current_position)
    max_value = -np.inf
    next_position = None
    for i in range(num_dimensions):
        for j in range(-1, 2):
            move = np.zeros(num_dimensions)
            move[i] = j
            new_position = current_position + move
            new_position = np.clip(new_position, search_space[0], search_space[1])
            value = pheromones[tuple(new_position.astype(int))]
            if value > max_value:
                max_value = value
                next_position = new_position
    return next_position

# Parâmetros do algoritmo ACO
num_ants = 10
num_iterations = 100
num_dimensions = 2
search_space = (-5, 5)
alpha = 1.0
beta = 1.0
evaporation_rate = 0.1

# Inicialização dos feromônios
pheromones = np.ones((11, 11))

# Execução do algoritmo ACO
ants = initialize_ants(num_ants, num_dimensions, search_space)
for _ in range(num_iterations):
    for ant in ants:
        ant_value = ackley_function(ant)
        next_position = choose_next_move(ant, pheromones, search_space)
        next_value = ackley_function(next_position)
        if next_value < ant_value:
            ant[:] = next_position
    pheromones *= (1 - evaporation_rate)

# Encontrando a melhor solução encontrada pelas formigas
best_ant = min(ants, key=lambda x: ackley_function(x))
best_value = ackley_function(best_ant)
print("Melhor solução encontrada:", best_ant)
print("Valor da função de Ackley:", best_value)