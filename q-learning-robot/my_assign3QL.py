'''
HEADER:
Introduction to Artificial Intelligence: Assignment 3, Reinforcement Learning(QLearning)
Teach the kid to wear clothes in a proper manner.


(1) Representations of states:
At any given state of the program the state is defined as a 4 character string, where each character denotes the position of the cloth denoted by that character position.
Clothes Order in string: 0: shirt, 1: sweater, 2: socks, 3: shoes.
Example:
RRRR: Denotes that all the clothes are in the room. (initial state)
UUFF: Denotes that all the clothes have been worn in a proper manner. The shirt and sweater are on the upper body and the socks and shoes are on the feet.(Final State)


(2) Transition Diagram:
The transition Diagram is stored in a Dictionary where each key denotes a node in the graph and
the value for eack key is a list of all nodes that have a connection from that node.
For example: For the graph (http://www.mrgeek.me/wp-content/uploads/2014/04/directed-graph.png) the dictionary would look like:

tDiag = {
	"A":["B"],
	"B":["C"],
	"C":["E"],
	"D":["B"],
	"E":["D","F"],
	"F":[]
}

'''

#Libraries allowed: Numpy, Matplotlib
#Installed using: pip install numpy matplotlib
import matplotlib.pyplot as plt
import numpy as np
import random
import copy
'''
All possible locations for the clothes: "R: Room", "U: Upper Body", "F: Feet"
Clothes to wear along with their type; U: Upper Body, F: Feet:
NOTE: It is "not" required to use this variable.
'''
clothes = {
	0:{"name":"shirt","type":"U","order":1},
	1:{"name":"sweater","type":"U","order":2},
	2:{"name":"socks","type":"F","order":1},
	3:{"name":"shoes","type":"F","order":2}
}

'''
Global variable to store all "possible" states.
Please enter all possible states from part (a) Transition Graph in this variable.
For state reference check HEADER(1)
'''
states = ['RRRR','URRR','RRFR','UURR','RRFF','URFR','UUFR','URFF','UUFF']


'''
This function is used to build the Transition Diagram.(tDiag)
I/P: states variable, O/P: returns transition dictionary.
For reference check HEADER(2)
'''
def buildTransitionDiag(states):
	tDiag = {}
	for s1 in states:
		tDiag[s1] = []
		for s2 in states:
			difference = [i for i in range(len(s1)) if s1[i] != s2[i]]
			if len(difference) == 1:
				tDiag[s1].append(s2)
			else:
				continue
	# tDiag['UUFF'] = []
	return tDiag

'''
This function builds the Reward Matrix R.
Penultimate transition are assigned a high score ~ 100.
Possible transitions are assigned 0.
Transitions not possible are assigned -1.
I/P: transition diagram, O/P: returns R matrix.
'''
def buildRMatrix(tD):
	# Enter your code here.
	R = np.zeros((len(states),len(states)))
	for row in range(len(states)):         
		for col in range(len(states)):       
			if states[col] not in tD[states[row]]:
				R[row][col] = -1
			elif states[col] == 'UUFF':
				R[row][col] = 100
			else:
				continue
	return R      # type: np.array

'''
This function returns the path taken while solving the graph by utilizing the Q-Matrix.
I/P: Q-Matrix. O/P: Steps taken to reach the goal state from the initial state.
NOTE: As you probably infer from the code, the break-off point is 50-traversals. 
You'll probably encounter this while finishing this assignment that at the initial stages of training, 
it is impossible for the agent to reach the goal stage using Q-Matrix. 
This break-off point allows your program to not be stuck in a REALLY-LONG loop.
'''
def solveUsingQ(Q):
	start = initial_state
	steps = [start]
	while start != goal_state:
		start = Q[start,].argmax()
		steps.append(start)
		if len(steps) > 50: break
	return steps


'''
Q-Learning Function.
This function takes as input the R-Matrix, gamma, alpha and Number of Episodes to train Q for.
It returns the Q-Matrix as output.
'''
def learn_Q(R, gamma = 0.8, alpha = 0.0, numEpisodes = 0):

	#Write your code to do the work here.
	state = random.randint(1,len(states)-2)    #except final state
	# state = initial_state
	Q = copy.deepcopy(R)
	for times in range(numEpisodes):
		# print Q
		if state == goal_state:
			state = random.randint(1,len(states)-2)
		action = np.random.choice([i for i in range(0,len(states)) if R[state][i] >= 0])
		Q[state][action] = (1- alpha) * Q[state][action] + alpha * R[state][action] + alpha * gamma * Q[action,].argmax()
		Q[state][action] = float(Q[state][action])
		state = int(action)
		times += 1
	return np.matrix(Q)


#variables that hold returned values from the defined functions.
tDiag = buildTransitionDiag(states)
R = buildRMatrix(tDiag)

#Define the initial and goal state with the corresponding index they hold in variable "states".
initial_state = 0
goal_state = 8

'''
Problem: Perform 500 episodes of training, and after every 2nd iteration,
use the Q Matrix to solve the problem, and save the number of steps taken.
At the end of training, use the saved step-count to plot a graph: training episode vs # of Moves.

NOTE: Do this for 4 alpha values. alpha = 0.1, 0.5, 0.8, 1.0
'''
trainSteps = []#Variable to save iteration# and step-count.
runs = [i for i in range(10,200,2)]#List contatining the runs from 10 -> 200, with a jump of 2.

# stepsTaken = len(solveUsingQ(Q))
# trainSteps.append([i,stepsTaken])

for i in runs:
	Q = learn_Q(R, alpha = 0.5, numEpisodes = i)
	stepsTaken = len(solveUsingQ(Q))
	trainSteps.append([i,stepsTaken])

#After Training, plotting diagram.
#NOTE: rename diagram accordingly or it will overwrite previous diagram.
x,y = zip(*trainSteps)
plt.plot(x,y,".-")
plt.xlabel("Training Episode")
plt.ylabel("# of Traversals.")
plt.savefig("output_0.5.png")

#Save the output for the best possible order, as generated by the code in the FOOTER.
path = solveUsingQ(Q)
print("\nThe best possible order to wear clothes is:\n")
tmp = ""
for i in path:
	tmp += states[i] + " -> "
print(tmp.rstrip(" ->"))
'''
FOOTER: Save program output here:

'''
