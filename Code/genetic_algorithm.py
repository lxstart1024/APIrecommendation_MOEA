import math
import random

def select(P, number):
    selected_individual = []
    i = 0
    selected_index = random.sample(range(0, len(P)), number)
    for i in range(len(selected_index)):
        selected_individual.append(P[selected_index[i]])
    return selected_individual


def crossover(P, probability):
    i = 0
    while i < len(P):
        a, b = (random.randint(0, 9), random.randint(0, 9))
        if a == b:
            i += 1
            continue
        elif random.uniform(0, 1) > probability:
            i += 1
            continue
        else:
            crosspoint = random.randint(1, 5)
            if (random.randint(0, 1) == 0):
                temp = P[a][:crosspoint]
                P[a][:crosspoint] = P[b][:crosspoint]
                P[b][:crosspoint] = temp
            else:
                temp = P[a][crosspoint:]
                P[a][crosspoint:] = P[b][crosspoint:]
                P[b][crosspoint:] = temp
            i += 1


def mutation(P, probability):
    bitnums = len(P) * len(P[0])
    mutatedindex = bitnums * probability
    mutatedindividual = int(mutatedindex/len(P[0]))
    mutatedbit = int(mutatedindex%len(P[0]))
    
    flag = True
    while flag:
        mutatednum = random.randint(1, 208)
        if mutatednum in P[mutatedindividual]:
            mutatednum = random.randint(1, 208)
        else:
            flag = False
    P[mutatedindividual][mutatedbit] = mutatednum
