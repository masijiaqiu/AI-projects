'''
NAME: Masijia Qiu
SID: 20739061

'''

import numpy as np
import copy


def restrict(factor, variable, value):
    variable_index = factor[0].index(variable)
    new_factor = [factor[0][:variable_index]+factor[0][variable_index+1:]]
    for row in factor[1:]:
        if row[variable_index] == value:
            new_factor.append(row[:variable_index]+row[variable_index+1:])
    return new_factor

def multiply(factor1, factor2):
    # print 'factor1\n',np.array(factor1)
    # print 'factor2\n',np.array(factor2)
    variables1 = set(factor1[0][:-1])
    variables2 = set(factor2[0][:-1])
    new_variables = variables1 | variables2
    new_factor = [list(new_variables)+['P']]

    diff_variables = variables2 - variables1
    same_variables = variables1 & variables2
    
    for row in factor1[1:]:
        for row2 in factor2[1:]:
            new_row = [0] * (len(new_variables) + 1)

            for i in variables1:
                new_row[new_factor[0].index(i)] = row[factor1[0].index(i)]

            if [row[factor1[0].index(m)] for m in same_variables] == [row2[factor2[0].index(n)] for n in same_variables]:
                for v in diff_variables:
                    new_row[new_factor[0].index(v)] = row2[factor2[0].index(v)]
                
                new_row[-1] = row[-1]*row2[-1]
                # print 'new_row',new_row
                new_factor.append(new_row)
                # print np.array(new_factor)
        
    return new_factor
        

def sumout(factor, variable):
    vindex = factor[0].index(variable)
    new_factor = [factor[0][:vindex] + factor[0][vindex+1:]]

    for row in factor[1:]:
        new_row = row[:vindex] + row[vindex+1:-1]
        flag = False
        for i in new_factor:
            if new_row != i[:-1]:
                continue
            else:
                i[-1] += row[-1]
                flag = True
                break
        if not flag:
            new_factor.append(new_row+[row[-1]])

    return new_factor 


def inference(factor_list, query_variables, ordered_list_of_hidden_variables, evidence_list):
    new_factor_list = copy.deepcopy(factor_list)
    # new_factor_list = factor_list
    # for i in new_factor_list:
    #     print np.array(i[0])
    #     print np.array(i[1:])
    #     print '\n'
    print '================ restrct the factors ================'
    for evidence in evidence_list:
        remove_list = []
        for factor in new_factor_list:
            if evidence in factor[0]:
                # print("========ev in varlist:======", evidence)
                # print np.array(factor[0])
                # print np.array(factor[1:])
                new_factor = restrict(factor, evidence, evidence_list[evidence])
                remove_list.append(factor)
                if len(new_factor[0]) > 1:
                    new_factor_list.append(new_factor)
                    print np.array(new_factor[0])
                    print np.array(new_factor[1:]),'\n'
        new_factor_list = [f for f in new_factor_list if f not in remove_list]

        # print "\t\tfor i in factor list:"
        # for i in new_factor_list:
        #     print np.array(i[0])
        #     print np.array(i[1:])
        #     print '\n'

    
    print '================ multiply & sumout the factors ================='
    for hidden_variable in ordered_list_of_hidden_variables:
        targets = [f for f in new_factor_list if hidden_variable in f[0][:-1]]
        if len(targets) == 0:
            continue
        res = targets[0]
        remove_list = [targets[0]]
        for i in range(1,len(targets)):
            res = multiply(res, targets[i])
            remove_list.append(targets[i])
        

        res = sumout(res, hidden_variable)

        new_factor_list = [f for f in new_factor_list if f not in remove_list]

        if res is not None:
            new_factor_list.append(res)

        print np.array(res[0])
        print np.array(res[1:]),'\n'

    
    print '\n================  sumout all the factors ================='
    res = new_factor_list[0]
    for factor in new_factor_list[1:]:
        res = multiply(res, factor)
    
        print np.array(res[0])
        print np.array(res[1:]),'\n'
  
    print "\n========================= after norm =======================\nThe final result is:\n"
    res = normalize(res)
    print np.array(res[0])
    print np.array(res[1:])
    return 'DONE\n\n'


        


def normalize(factor):
    total = 0
    for row in factor[1:]:
        total += row[-1]
    for row in factor[1:]:
        row[-1] = row[-1] / total

    return factor

#FS=100
#FB=101
#FM=102
#NA=103
#FH=104
#NDG=105
fs=[['FS','P'],[0,0.95],[1,0.05]]
fb = [['FB','FS','P'],[1,1,0.6],[0,1,0.4],[1,0,0.1],[0,0,0.9]]
fm = [['FM','P'],[1,0.036],[0,0.964]]

na=[['NA','P'],[1,0.3],[0,0.7]]

ndg=[['NDG','FM','NA','P'],[1,0,0,0],[1,0,1,0.5],[1,1,0,0.4],[1,1,1,0.8],[0,0,0,1],[0,0,1,0.5],[0,1,0,0.6],[0,1,1,0.2]]
fh=[['FH','FM','NDG','FS','P'],[1,1,1,1,0.99],[1,0,0,0,0],[1,0,0,1,0.5],[1,0,1,1,0.75],[1,1,0,1,0.9],[1,1,1,0,0.65],[1,1,0,0,0.4],[1,0,1,0,0.2],[0,1,1,1,0.01],[0,0,0,0,1],[0,0,0,1,0.5],[0,0,1,1,0.25],[0,1,0,1,0.1],[0,1,1,0,0.35],[0,1,0,0,0.6],[0,0,1,0,0.8]]


########## Q3-b ###########
evidence_list = {}
query_variables = ['FH']
ordered_list_of_hidden_variables = ['NA', 'NDG', 'FM', 'FS','FB']
print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  Q3-b   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<:'
print inference([fh,na,fs,fm,ndg,fb], query_variables, ordered_list_of_hidden_variables, evidence_list)

# ######### Q3-c ############

evidence_list = {'FH': 1, 'FM': 1}
query_variables = ['FS']
ordered_list_of_hidden_variables = ['NA', 'NDG', 'FB']
print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  Q3-c   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<:'
print inference([fh,fm,fs,na,ndg,fb], query_variables, ordered_list_of_hidden_variables, evidence_list)



######### Q3-d ############
evidence_list = {'FH': 1, 'FM': 1, 'FB': 1}
ordered_list_of_hidden_variables = ['NA', 'NDG']
query_variables = ['FS']
print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  Q3-d   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<:'
print inference([fh,fm,fs,na,ndg,fb], query_variables, ordered_list_of_hidden_variables, evidence_list)



######### Q3-e ############

evidence_list = {'FH': 1, 'FM': 1, 'FB': 1, 'NA': 1}
ordered_list_of_hidden_variables = ['NDG']
query_variables = ['FS']
print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  Q3-e   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<:'
print inference([fh,fm,fs,na,ndg,fb], query_variables, ordered_list_of_hidden_variables, evidence_list)







