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

        


    def get_distance(self):
        dist = self.matrix['A'][self.tour[0]]
        for i in range(0, len(self.tour) - 1):
            dist += self.matrix[self.tour[i]][self.tour[i + 1]]
        dist += self.matrix[self.tour[-1]]['A']       
        return dist

    def get_tour(self):
        return self.tour

    def swap_positions(self):
        pos1, pos2 = random.sample(range(0, len(self.tour) - 1), 2)
        self.tour[pos1], self.tour[pos2] = self.tour[pos2], self.tour[pos1]

    def shuffle_tour(self):
        random.shuffle(self.tour)



def get_distance(tour, matrix):
    dist = matrix['A'][tour[0]]
    for i in range(0, len(tour) - 1):
        dist += matrix[tour[i]][tour[i + 1]]
    dist += matrix[tour[-1]]['A']

    return dist

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
    current = Tour(init_list, distance_matrix)
    best = Tour(list(init_list), distance_matrix)

    
    
    print "****************  start  ************"
    
    for counts in range(0,2):
        temp = 900000
        rate = 0.99995
        if i > 0:
            current.shuffle_tour()
        print "a restart"
        while temp > 1:
            # get a neighbour of the current tour
            new = Tour(list(current.get_tour()), distance_matrix)
            new.swap_positions()

            if acceptability(current.get_distance(), new.get_distance(), temp) > random.random():
                current = Tour(list(new.get_tour()), distance_matrix)

            if current.get_distance() < best.get_distance():
                best = Tour(list(current.get_tour()), distance_matrix)


            temp *= rate
    

    print "After SA: ", best.get_tour(), best.get_distance()


###########################################################################

if __name__ == '__main__':
    # if not len(sys.argv) == 2:
    #     exit("Wrong arguments.")
    # main(sys.argv[1])
    # a_star('/Users/choumasijia/Downloads/CS686/assignment1/randTSP/problem36')

    main('/Users/choumasijia/Downloads/CS686/assignment2/randTSP/15/instance_1.txt')
    # test()