#!/usr/bin/env python

from collections import defaultdict
from scipy.spatial import distance
import random
import math
import matplotlib.pyplot as plt
import copy



class Tour(object):
    def __init__(self, tour, matrix):
        self.tour = tour
        self.matrix = matrix
    
    # get the total cost of the specific tour
    def get_distance(self):
        dist = self.matrix['A'][self.tour[0]]
        for i in range(0, len(self.tour) - 1):
            dist += self.matrix[self.tour[i]][self.tour[i + 1]]
        dist += self.matrix[self.tour[-1]]['A']       
        return dist

    def get_tour(self):
        return self.tour

    # local search operator: randomly swap two cities' positions
    def swap_positions(self):
        pos1, pos2 = random.sample(range(0, len(self.tour) - 1), 2)
        self.tour[pos1], self.tour[pos2] = self.tour[pos2], self.tour[pos1]
    
    # reverse a random sublist cities in the tour
    def reverse_sublist(self):
        pos1, pos2 = random.sample(range(0, len(self.tour) - 1), 2)
        if pos1 < pos2:
            self.tour[pos1:pos2] = self.tour[pos1:pos2][::-1]
        else:
            self.tour[pos2:pos1] = self.tour[pos2:pos1][::-1]
    
    # shuffle the tour, works as a restart to the algorithm
    def shuffle_tour(self):
        random.shuffle(self.tour)


def get_distance(tour, matrix):
    dist = matrix['A'][tour[0]]
    for i in range(0, len(tour) - 1):
        dist += matrix[tour[i]][tour[i + 1]]
    dist += matrix[tour[-1]]['A']

    return dist

# return the probability of going to a new moveset
def acceptability(current, new, temp):
    if new < current:
        return 1.
    return math.exp((current - new) / temp)

def main(input_file):
    city_locations = defaultdict(dict)
    f = open(input_file)
    num_cities = int(f.readline())
    for each in f.read().strip().split('\n'):
        city_locations[each.split()[0]] = (int(each.split()[1]), int(each.split()[2])) 
    # print city_locations
    

    # get the distance matrix among any two cities. The distance matrix can save resource for repeated calculations.
    distance_matrix = defaultdict(dict)
    for i in city_locations:
        for j in city_locations:
            if i == j:
                distance_matrix[i][j] = 0
                continue
            distance_matrix[i][j] = distance.euclidean(city_locations[i], city_locations[j])
    # print distance_matrix

    # initialize a start state: random ordered cities
    init_list = city_locations.keys()
    init_list.remove('A')
    random.shuffle(init_list)

    # print "initial: ", init_list, get_distance(init_list, distance_matrix)


    current = Tour(init_list, distance_matrix)
    best = Tour(list(init_list), distance_matrix)


    temp = 1000000000
    rate = 0.99999
    
    while temp > 1:
        # get a neighbour of the current tour
        new = Tour(list(current.get_tour()), distance_matrix)
        new.swap_positions()
        
        # allow random jump out of local optimal solutions
        if acceptability(current.get_distance(), new.get_distance(), temp) > random.random():
            current = Tour(list(new.get_tour()), distance_matrix)
        
        # update the solution
        if current.get_distance() < best.get_distance():
            best = Tour(list(current.get_tour()), distance_matrix)
        
        # temperature annealing
        temp *= rate
        
        # random restart
        # if random.random()<0.1:
        #     current.shuffle_tour()
    
    # print out the solution
    sa_tour = ['A'] + best.get_tour() + ['A']
    print "Tour: ", sa_tour
    print "Distance: ", best.get_distance()

 

###########################################################################

if __name__ == '__main__':
    # if not len(sys.argv) == 2:
    #     exit("Wrong arguments.")
    # main(sys.argv[1])
    main('/Users/choumasijia/Downloads/CS686/assignment1/randTSP/problem36')

    # main('/Users/choumasijia/Downloads/CS686/assignment2/randTSP/15/instance_1.txt')
