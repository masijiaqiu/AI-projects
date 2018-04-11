'''
Student Name: Masijia Qiu
Student ID: 20739061
Language: Python2
'''

import copy
import math

class Node(object):
    def __int__(self, attribute, threshold, classification, Lsubtree, Rsubtree):
        self.attribute = attribute
        self.threshold = threshold
        self.classification = classification
        self.left = Lsubtree
        self.right = Rsubtree

    def set_classification(self, c):
        self.classification = c

    def set_threshold(self, t):
    	self.threshold = t

    def set_attribute(self, a):
    	self.attribute = a

    def set_Lsubtree(self, l):
    	self.left = l

    def set_Rsubtree(self, r):
    	self.right = r

class BestAttribute(object):
    def __init__(self, attribute, threshold):
        self.attribute = attribute
        self.threshold = threshold


def load_data(input_file):
    f = open(input_file)
    data = []
    for each in f.read().strip().split('\n'):
        i = [float(e) for e in each.strip().split(',')[:-1]]
        if each.strip().split(',')[-1] == 'healthy.':
            i.append(0)
        else:
            i.append(1)
        data.append(i)
    return data

def in_same_classification(data):
    if len(data) == 0:
        return True
    head = data[0][-1]
    for e in data:
        if e[-1] != head:
            return False
    return True

def get_mode_classification(data):
    ones = 0
    zeros = 0
    for e in data:
        if e[-1] == 1:
            ones += 1
        else:
            zeros += 1
    if ones > zeros:
        return 1
    else:
        return 0

def get_oneI(a,b):
	if a == 0 or b == 0:
	    return 0
	return -a/(a+b)*math.log(a/(a+b), 2) - b/(a+b)*math.log(b/(a+b),2)

def get_entropy(data, attr, threshold):
    left_zeros = 0.
    left_ones = 0.
    right_zeros = 0.
    right_ones = 0.
    for sample in data:
        if sample[attr] < threshold:
            if sample[-1] == 0:
                left_zeros += 1
            else:
                left_ones += 1
        else:
            if sample[-1] == 0:
                right_zeros += 1
            else:
                right_ones += 1
    
    return (left_zeros+left_ones)/len(data)*get_oneI(left_zeros, left_ones) + (right_zeros+right_ones)/len(data)*get_oneI(right_zeros, right_ones)

def get_best_attribute(data, attributes):
    minextropy = 1
    bestattr = -1
    bestthres = -1
    for attr in attributes:
        candidates = sorted(set([sample[attr] for sample in data]))
        for i in range(0, len(candidates)-1):
            thres = candidates[i]/2 + candidates[i+1]/2
            entropy = get_entropy(data, attr, thres)

            if entropy < minextropy:
                minextropy = copy.deepcopy(entropy)
                bestattr = copy.deepcopy(attr)
                bestthres = copy.deepcopy(thres) 
    # return best
    return BestAttribute(bestattr, bestthres)

def divide_tree(data, best):
    left = []
    right = []
    for sample in data:
        if sample[best.attribute] < best.threshold:
        	left.append(sample)
        else:
        	right.append(sample)
    return left, right

def decision_tree_learning(examples, attributes, classification):
    cur_node = Node()
    if len(examples) == 0:
        cur_node.set_classification(classification)
        print '********* leaves'
    elif in_same_classification(examples):
    	print '********* leaves with classification', get_mode_classification(examples)
        cur_node.set_classification(get_mode_classification(examples))
    elif attributes == 0:
    	print '********* no attribute'
        cur_node.set_classification(get_classification(examples))
    else:
        best_attribute = get_best_attribute(examples, attributes)

        cur_node.set_classification(-1)
        cur_node.set_attribute(best_attribute.attribute)
        cur_node.set_threshold(best_attribute.threshold)

        left, right = divide_tree(examples, best_attribute)
        # print 'left:', [i[-1] for i in left]
        # print 'right:', [i[-1] for i in right]

        print '** NODE **\n attribute index:',cur_node.attribute, 'threshold:', cur_node.threshold, cur_node.classification
        cur_node.Lsubtree = decision_tree_learning(left, attributes, get_mode_classification(left))
        cur_node.Rsubtree = decision_tree_learning(right, attributes, get_mode_classification(right))
        
    return cur_node

def predict_sample(sample, tree):
    if tree.classification >= 0:
    	print tree.classification
    	return tree.classification
    elif sample[tree.attribute] < tree.threshold:
    	return predict_sample(sample, tree.Lsubtree)
    else:
    	return predict_sample(sample, tree.Rsubtree)

def run_tree(data, tree):
    correct = 0
    incorrect = 0
    for sample in data:
        if predict_sample(sample, tree) == sample[-1]:
        	correct += 1
        else:
        	incorrect += 1
    return correct, incorrect

def main(train, test):
    traindata = load_data(train)
    dtl = decision_tree_learning(traindata, range(0,16), 1)

    testdata = load_data(test)

    correct, incorrect = run_tree(testdata, dtl)
    print '---->  predict sample:  <----'
    print 'correct:', correct, 'incorrect:', incorrect
    print 'Done'
    
    # m = dtl.Lsubtree.Rsubtree
    # print m.classification, m.attribute, m.Lsubtree.classification, m.Rsubtree.classification




if __name__ == '__main__':
    main('/Users/choumasijia/Desktop/CS686/assignment5/horseTrain.txt', 
     '/Users/choumasijia/Desktop/CS686/assignment5/horseTest.txt')
