import java.util.Random;

public class Rosenbrock {

    // Função para calcular a função objetivo (Rosenbrock)
    public static double rosenbrockFunction(double[] x) {
        double sum = 0;
        for (int i = 0; i < x.length - 1; i++) {
            double term1 = Math.pow(1 - x[i], 2);
            double term2 = 100 * Math.pow(x[i + 1] - Math.pow(x[i], 2), 2);
            sum += term1 + term2;
        }
        return sum;
    }

    // Função para inicializar a matriz de feromônios
    public static double[][] initializePheromoneMatrix(int numAnts, int numDimensions) {
        double[][] pheromones = new double[numAnts][numDimensions];
        for (int i = 0; i < numAnts; i++) {
            for (int j = 0; j < numDimensions; j++) {
                pheromones[i][j] = 1.0;
            }
        }
        return pheromones;
    }

    // Função para selecionar a próxima posição baseada nas probabilidades de transição
    public static int[] selectNextPosition(double[][] pheromoneMatrix) {
        int numAnts = pheromoneMatrix.length;
        int numDimensions = pheromoneMatrix[0].length;
        double[] probabilities = new double[numDimensions];
        Random random = new Random();
        int[] chosenDimensions = new int[numAnts];

        for (int i = 0; i < numAnts; i++) {
            double sum = 0;
            for (int j = 0; j < numDimensions; j++) {
                sum += pheromoneMatrix[i][j];
            }
            for (int j = 0; j < numDimensions; j++) {
                probabilities[j] = pheromoneMatrix[i][j] / sum;
            }
            double rand = random.nextDouble();
            double cumulativeProbability = 0;
            for (int j = 0; j < numDimensions; j++) {
                cumulativeProbability += probabilities[j];
                if (rand < cumulativeProbability) {
                    chosenDimensions[i] = j;
                    break;
                }
            }
        }
        return chosenDimensions;
    }

    // Função principal do algoritmo ACO
    public static double[] antColonyOptimization(int numAnts, int numDimensions, int numIterations, double evaporationRate) {
        double[] bestSolution = null;
        double bestFitness = Double.POSITIVE_INFINITY;

        double[][] pheromoneMatrix = initializePheromoneMatrix(numAnts, numDimensions);
        Random random = new Random();

        for (int iteration = 0; iteration < numIterations; iteration++) {
            double[][] solutions = new double[numAnts][numDimensions];
            for (int i = 0; i < numAnts; i++) {
                for (int j = 0; j < numDimensions; j++) {
                    solutions[i][j] = random.nextDouble();
                }
            }

            double[] fitnessValues = new double[numAnts];
            for (int i = 0; i < numAnts; i++) {
                fitnessValues[i] = rosenbrockFunction(solutions[i]);
            }

            // Atualização da melhor solução encontrada até agora
            double minFitness = Double.POSITIVE_INFINITY;
            int minIndex = -1;
            for (int i = 0; i < numAnts; i++) {
                if (fitnessValues[i] < minFitness) {
                    minFitness = fitnessValues[i];
                    minIndex = i;
                }
            }
            if (minFitness < bestFitness) {
                bestFitness = minFitness;
                bestSolution = solutions[minIndex];
            }

            // Atualização da matriz de feromônios
            for (int i = 0; i < numAnts; i++) {
                for (int j = 0; j < numDimensions; j++) {
                    pheromoneMatrix[i][j] *= (1 - evaporationRate);
                    pheromoneMatrix[i][j] += 1 / fitnessValues[i];
                }
            }

            // Movimento das formigas para a próxima posição
            int[] nextPosition = selectNextPosition(pheromoneMatrix);
            for (int i = 0; i < numAnts; i++) {
                solutions[i][nextPosition[i]] = random.nextDouble();  // Atualiza a posição escolhida
            }
        }

        return bestSolution;
    }

    // Main method
    public static void main(String[] args) {
        int numAnts = 20;
        int numDimensions = 10;
        int numIterations = 100;
        double evaporationRate = 0.1;

        double[] bestSolution = antColonyOptimization(numAnts, numDimensions, numIterations, evaporationRate);

        // Print best solution found
        System.out.println("Melhor solução encontrada:");
        for (double value : bestSolution) {
            System.out.print(value + " ");
        }
        System.out.println();
        System.out.println("Melhor valor de fitness: " + rosenbrockFunction(bestSolution));
    }
}
