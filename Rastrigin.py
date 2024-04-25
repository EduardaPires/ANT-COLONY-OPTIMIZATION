import numpy as np

# Função Rastrigin
def rastrigin(x):
    A = 10
    n = len(x)
    return A * n + np.sum(x**2 - A * np.cos(2 * np.pi * x))

# Calcular a distância entre dois pontos
def calcular_distancia(ponto1, ponto2):
    return np.sqrt(np.sum((ponto1 - ponto2)**2))

# Função principal de otimização
def otimizacao_colonia_formigas(pontos, num_formigas, num_iteracoes, alfa, beta, taxa_evaporacao, Q):
    num_pontos = len(pontos) # Numero de pontos no grafo
    feromonio = np.ones((num_pontos, num_pontos)) # Inicialização dos feromônios
    melhor_ponto = None # Inicialização do melhor ponto
    melhor_fitness = np.inf # Inicialização do melhor fitness
    
    # Loop correspondente às iterações e inicialização do vetor que irá conter todos os caminhos de todas as formigas em uma iteração
    for iteracao in range(num_iteracoes):
        caminhos = []
        comprimentos_caminhos = []
        
        # Rotas de cada formiga
        for formiga in range(num_formigas):
            visitados = [False]*num_pontos # Cria-se um vetor correspondente aos pontos visitados (inicialmente todos falsos)
            ponto_atual = np.random.randint(num_pontos) # É escolhido aleatoriamente o ponto inicial da formiga
            visitados[ponto_atual] = True # Ponto inicial passa a ser visitado
            caminho = [ponto_atual] # Vetor contendo o caminho passa a ter um valor
            comprimento_caminho = 0 
            
            while False in visitados: # Loop irá acontecer até que a formiga visite todos os pontos
                nao_visitados = np.where(np.logical_not(visitados))[0] # Encontrar pontos não visitados
                probabilidades = np.zeros(len(nao_visitados)) # Criação do vetor com as probabilidades da formiga visitar cada ponto
                
                # Calcular as probabilidades de escolha do próximo ponto baseado nos feromônios e no inverso da distância (visibilidade)
                for i, ponto_nao_visitado in enumerate(nao_visitados):
                    probabilidades[i] = feromonio[ponto_atual, ponto_nao_visitado]**alfa / rastrigin(pontos[ponto_atual] - pontos[ponto_nao_visitado])**beta # Fórmula de probabilidade
                
                probabilidades /= np.sum(probabilidades)
                
                proximo_ponto = np.random.choice(nao_visitados, p=probabilidades) # Escolha aleatória do próximo ponto (mas impactado pela probabilidade de cada um)
                caminho.append(proximo_ponto) # Adiciona ponto escolhido no vetor de caminho
                comprimento_caminho += calcular_distancia(pontos[ponto_atual], pontos[proximo_ponto]) # Atualização do comprimento do caminho
                visitados[proximo_ponto] = True # Passa a ser visitado
                ponto_atual = proximo_ponto # Atualizamos o ponto atual
            
            caminhos.append(caminho) # Adicionamos o caminho da formiga ao vetor de caminhos
            comprimentos_caminhos.append(comprimento_caminho) # Adicionamos tbm a lista de comprimentos
            
            # Atualização da melhor solução encontrada
            if comprimento_caminho < melhor_fitness:
                melhor_ponto = pontos[proximo_ponto]
                melhor_fitness = comprimento_caminho
        
        feromonio *= taxa_evaporacao # Atualização dos feromônios pela taxa de evaporação
        
        # Atualização dos feromônios baseada nas soluções construídas pelas formigas (depósito, quanto melhor a solução mais feromonios naquele caminho)
        for caminho, comprimento_caminho in zip(caminhos, comprimentos_caminhos): # Percorre cada caminho com seu respectivo comprimento
            for i in range(num_pontos-1):
                feromonio[caminho[i], caminho[i+1]] += Q/comprimento_caminho
            # feromonio[caminho[-1], caminho[0]] += Q/comprimento_caminho
    
    print("Melhor ponto encontrado:", melhor_ponto)
    print("Melhor valor de fitness:", melhor_fitness)
    
    return melhor_fitness

# Exemplo de caso
pontos = np.random.rand(10, 10) # Gerar 10 pontos aleatórios de 10 dimensões
melhor_fitness = otimizacao_colonia_formigas(pontos, num_formigas=10, num_iteracoes=100, alfa=1, beta=1, taxa_evaporacao=0.01, Q=10)
