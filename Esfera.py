import numpy as np

# Função para calcular a função objetivo (esfera)
def sphere_function(x):
    return np.sum(x**2)

# Função para inicializar a matriz de feromônios
def initialize_pheromone_matrix(num_ants, num_dimensions):
    return np.ones((num_ants, num_dimensions))

# Função para selecionar a próxima posição baseada nas probabilidades de transição
def select_next_position(pheromone_matrix):
    num_ants, num_dimensions = pheromone_matrix.shape
    probabilities = pheromone_matrix / np.sum(pheromone_matrix, axis=1)[:, np.newaxis]
    chosen_dimensions = np.array([np.random.choice(num_dimensions, p=probabilities[i]) for i in range(num_ants)])
    return chosen_dimensions

# Função principal do algoritmo ACO
def ant_colony_optimization(num_ants, num_dimensions, num_iterations, alpha, beta, evaporation_rate):
    best_solution = None
    best_fitness = float('inf')

    pheromone_matrix = initialize_pheromone_matrix(num_ants, num_dimensions)

    for iteration in range(num_iterations):
        solutions = np.random.rand(num_ants, num_dimensions)  # Inicialização das soluções das formigas
        fitness_values = np.apply_along_axis(sphere_function, 1, solutions)  # Avaliação das soluções

        # Atualização da melhor solução encontrada até agora
        if np.min(fitness_values) < best_fitness:
            best_fitness = np.min(fitness_values)
            best_solution = solutions[np.argmin(fitness_values)]

        # Atualização da matriz de feromônios
        pheromone_matrix *= (1 - evaporation_rate)
        for ant in range(num_ants):
            for dim in range(num_dimensions):
                pheromone_matrix[ant, dim] += 1 / fitness_values[ant]

        # Movimento das formigas para a próxima posição
        for ant in range(num_ants):
            next_position = select_next_position(pheromone_matrix)
            solutions[ant, next_position] = np.random.rand()  # Atualiza a posição escolhida

    return best_solution, best_fitness

# Parâmetros do algoritmo
num_ants = 20
num_dimensions = 10
num_iterations = 100
alpha = 1.0  # Peso do feromônio
beta = 1.0   # Peso da visibilidade
evaporation_rate = 0.1

# Execução do algoritmo ACO
best_solution, best_fitness = ant_colony_optimization(num_ants, num_dimensions, num_iterations, alpha, beta, evaporation_rate)

print("Melhor solução encontrada:", best_solution)
print("Melhor valor de fitness:", best_fitness)