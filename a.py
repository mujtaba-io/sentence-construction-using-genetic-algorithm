
# python program to construct a valid sentence from a list of random words
# it uses a text file as a corpus to compare the fitness of the sentence
# with the corpus and uses genetic algorithm to find the best sentence

# as we increase the corpus size, the program gets extremely slow

import random
import re

# read the large text file to be used for fitness comparison
with open('tmp.txt', 'r') as file: # text.txt is large so takes too much time for string comparison, thus using smaller tmp.txt for testing
    corpus = file.read().lower()

# clean and tokenize the corpus
corpus_words = re.findall(r'\b\w+\b', corpus)

# generate a random initial population
def generate_population(words, population_size):
    return [random.sample(words, len(words)) for _ in range(population_size)]

# fitness function to compare the sequence against the corpus
def fitness(sequence):
    sequence_str = ' '.join(sequence)
    return sum(1 for i in range(len(corpus_words) - len(sequence))
               if corpus_words[i:i+len(sequence)] == sequence)

# selection: choose parents based on fitness
def select_parents(population, fitnesses):
    # ensure all fitnesses are greater than zero
    min_fitness = 0.1
    adjusted_fitnesses = [fit + min_fitness for fit in fitnesses]
    parents = random.choices(population, weights=adjusted_fitnesses, k=len(population)//2)
    return parents

# crossover: create children by combining two parents
def crossover(parent1, parent2):
    idx = random.randint(1, len(parent1) - 2)
    child1 = parent1[:idx] + parent2[idx:]
    child2 = parent2[:idx] + parent1[idx:]
    return child1, child2

# mutation: randomly swap two words in the sequence
def mutate(sequence):
    idx1, idx2 = random.sample(range(len(sequence)), 2)
    sequence[idx1], sequence[idx2] = sequence[idx2], sequence[idx1]
    return sequence

# genetic algorithm
def genetic_algorithm(words, population_size=100, generations=1000, mutation_rate=0.01):
    population = generate_population(words, population_size)
    
    for generation in range(generations):
        print(f'Generation {generation}...', end='\r')
        fitnesses = [fitness(seq) for seq in population]
        
        # check if any sequence is perfect
        if max(fitnesses) == len(words) - 1:
            print(f'Perfect sequence found in generation {generation}')
            break
        
        parents = select_parents(population, fitnesses)
        population = []
        
        while len(population) < population_size:
            parent1, parent2 = random.sample(parents, 2)
            child1, child2 = crossover(parent1, parent2)
            
            if random.random() < mutation_rate:
                child1 = mutate(child1)
            if random.random() < mutation_rate:
                child2 = mutate(child2)
                
            population.extend([child1, child2])
    
    # return the best sequence found
    best_sequence = max(population, key=fitness)
    return best_sequence

# list of random words
random_words = ["is", "a", "person", "good", "he"]

# run the genetic algorithm
best_sentence = genetic_algorithm(random_words)
print('Best sentence:', ' '.join(best_sentence))
