import random
from . import genetic_algorithm


class Individual:
    def __init__(self, properties, lower, upper):
        self.properties = properties
        if not isinstance(lower, list):
            self.lower = [lower]*len(properties)
        else:
            self.lower = lower
        if not isinstance(upper, list):
            self.upper = [upper]*len(properties)
        else:
            self.upper = upper

    def __getitem__(self, i):
        return self.properties[i]

    def __str__(self):
        return str(self.properties)

class MOP:
    def __init__(self, funs, minormax):
        self.funs = funs 
        self.minormax = minormax 

    
    def result(self, individual):
        funresult = []
        for fun in self.funs:
            funresult.append(fun(individual))
        return funresult

    
    def dominate(self, i0, i1): 
        result0 = self.result(i0)
        result1 = self.result(i1)
        diff = [result0[i]-result1[i] for i in range(len(self.funs))]
        # print(diff)
        if self.minormax == 'min':
            if max(diff) <= 0 and diff != [0]*len(self.funs):
                return True
        if self.minormax == 'max':
            if min(diff) >= 0 and diff != [0]*len(self.funs):
                return True
        return False


def printpopulation(P):
    s = ''
    for i, indi in enumerate(P):
        s += str(i+1)+':'+str(indi)+'\n'
    return s


def make_rand_individual(propertynum, min, max):
    L = []
    for i in range(propertynum):
        L.append(random.randint(min, max)) 
    return L


def make_rand_population(populationsize, propertynum, min, max): 
    P = []
    for i in range(populationsize): 
        P.append(make_rand_individual(propertynum, min, max))
    return P


def make_new_population(P, crossprobability=0.8, mutationprobability=0.01):
    matingpool = genetic_algorithm.select(P, 10) 
    genetic_algorithm.crossover(matingpool, crossprobability)
    genetic_algorithm.mutation(matingpool, mutationprobability)
    newpopulation = genetic_algorithm.select(matingpool, 10)
    return newpopulation
