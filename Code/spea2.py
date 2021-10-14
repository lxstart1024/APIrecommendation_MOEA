from . import population
import math
import numpy as np

iterdisplay = 1


def spea2(mop, populationsize, archivesize, propertynum, min, max, maxiter):
    P = []
    Q = []
    P.append(population.make_rand_population(
        populationsize, propertynum, min, max))
    Q.append([])
    t = 0
    while(True):
        if iterdisplay: 
            print(t, 'iter')
            print(population.printpopulation(Q[t]))
            print('-'*100)
        
        F, kdistance = cal_fitness(P[t]+Q[t], mop) 
        print(F)
        print(kdistance)
        
        Q.append(select_nondom(P[t]+Q[t], F)) 
        while(len(Q[t+1]) > archivesize):
            truncate_population(Q[t+1], kdistance) 
        if(len(Q[t+1]) < archivesize):
            Q[t+1] += fill_dominated(P[t]+Q[t], F, archivesize-len(Q[t+1])) 
        print(Q[t+1])
        if t >= maxiter or stop_criterion():
            return Q[t+1]
        
        P.append(population.make_new_population(Q[t+1]))
        t += 1


def cal_fitness(P, mop):
    S = [0]*len(P)
    R = [0]*len(P)
    for i in range(len(P)):
        for j in range(len(P)):
            if mop.dominate(P[i], P[j]):
                S[i] += 1
    for i in range(len(P)):
        for j in range(len(P)):
            if mop.dominate(P[j], P[i]):
                R[i] += S[j]
    k = int(math.sqrt(len(P)))
    kdistance = get_nearest_distance(P, k)
    D = [] 
    F = [] 
    for i in range(len(P)):
        D.append(1/(kdistance[i][k-1]+2))
        F.append(R[i]+D[i])
    return F, kdistance


def select_nondom(P, F):
    nondomP = []
    for i in range(len(P)):
        if F[i] < 1:
            nondomP.append(P[i])
    return nondomP


def truncate_population(P, kdistance):
    for i in range(len(P)):
        choose = True
        for j in range(len(P)):
            if not less_equal_distance(i, j, kdistance):
                choose = False
                break
        if choose:
            del(P[i], kdistance[i])
            return


def less_equal_distance(i, j, kdistance):
    condition0 = True
    for k in range(len(kdistance[0])): 
        if kdistance[i][k] != kdistance[j][k]: 
            condition0 = False
            break
    if condition0 == True:
        return True
    condition1 = False
    for k in range(len(kdistance[0])):
        condition10 = True
        for l in range(k):
            if kdistance[i][l] != kdistance[j][l]:
                condition10 = False
                break
        condition11 = False
        if kdistance[i][k] < kdistance[j][k]:
            condition11 = True
        condition1 = condition10 and condition11
        if condition1 == True:
            return True
    return False


def fill_dominated(P, F, fillnum):
    fill = []
    filled = 0
    sortF = np.argsort(F) 
    for i in sortF:
        if F[i] >= 1:
            fill.append(P[i])
            filled += 1
            if filled == fillnum:
                break
    return fill


def stop_criterion():
    return False


def get_distance(I, J):
    distance = 0
    for i in range(len(I)):
        distance += (I[i]-J[i])*(I[i]-J[i])
    return distance


def get_nearest_distance(P, k):
    distance = []
    nearest_distance = []
    for i in range(len(P)):
        distance.append([]) 
        for j in range(len(P)):
            if i != j:
                dis = get_distance(P[i], P[j])
                distance[i].append(dis)
    for i in range(len(P)): 
        nearest_distance.append([])
        distance[i].sort() 
        nearest_distance[i].append(distance[i][0])
        
        for j in range(1, k):
            nearest_distance[i].append(nearest_distance[i][j-1]+distance[i][j])
    return nearest_distance