import itertools
from collections import defaultdict
from scipy.spatial import distance as dist

def distance(p1, p2):
        #calculates distance from two points
        d = (((p2[0] - p1[0])**2) + ((p2[1] - p1[1])**2))**.5
        return float(d)

def calCosts(routes, nodes):
    travelCosts = []

    for route in routes:
        travelCost = 0

        #Sums up the travel cost
        for i in range(1,len(route)):
            #takes an element of route, uses it to find the corresponding coords and calculates the distance
            travelCost += distance(nodes[str(route[i-1])], nodes[str(route[i])])

        travelCosts.append(travelCost)

    #pulls out the smallest travel cost
    smallestCost = min(travelCosts)
    shortest = (routes[travelCosts.index(smallestCost)], smallestCost)

    #returns tuple of the route and its cost
    return shortest


def genRoutes(routeLength):
    #lang hold all the 'alphabet' of nodes
    lang = [ x for x in range(2,routeLength+1) ]

    #uses built-in itertools to generate permutations
    routes = list(map(list, itertools.permutations(lang)))
    #inserts the home city, must be the first city in every route
    for x in routes:
        x.insert(0,1)
    return routes


def main(nodes=None, instanceSize=5):
    #nodes and instanceSize are passed into main() using another program
    #I just gave them default values for this example

    #The Node lookup table.
    # Nodes = {
        # '1': (565.0, 575.0),
        # '2': (25.0, 185.0),
        # '3': (345.0, 750.0),
        # '4': (945.0, 685.0),
        # '5': (845.0, 655.0),
        # '6': (880.0, 660.0),
        # '7': (25.0, 230.0),
        # '8': (525.0, 1000.0),
        # '9': (580.0, 1175.0),
        # '10': (650.0, 1130.0),
        # '11': (1605.0, 620.0),
        # '12': (1220.0, 580.0),
        # '13': (1465.0, 200.0),
        # '14': (1530.0, 5.0),
        # '15': (845.0, 680.0)
    # }
    

    # city_locations = defaultdict(dict)
    # f = open('/Users/choumasijia/Downloads/CS686/assignment2/randTSP/5/instance_1.txt')
    # num_cities = int(f.readline())
    # for each in f.read().strip().split('\n'):
    #     city_locations[each.split()[0]] = (float(each.split()[1]), float(each.split()[2])) 
    # print city_locations


    # Nodes = {'A': (40., 94.), 'C': (71., 25.), 'B': (25., 73.), 'E': (81., 62.), 'D': (48., 80.)}
    Nodes = {'1': (40., 94.), '2': (71., 25.), '3': (25., 73.), '4': (81., 62.), '5': (48., 80.)}

    # Nodes = city_locations



    routes = genRoutes(instanceSize)
    shortest = calCosts(routes, Nodes)

    print("Shortest Route: ", shortest[0])
    print("Travel Cost: ", shortest[1])


if __name__ == '__main__':
    main()