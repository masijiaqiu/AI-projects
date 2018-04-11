class VariableElimination:
    @staticmethod
    def inference(factorList, queryVariables, orderedListOfHiddenVariables, evidenceList):
        # for f in factorList:
        #     f.print()
        for ev in evidenceList:
            remove_list = []
            for factor in factorList:
                if ev in factor.varList:
                    # print("^^^^^^^^^^^ev in varlist:", ev)
                    # factor.print()
                    newFactor = factor.restrict(ev, evidenceList[ev])
                    # newFactor.print()
                    remove_list.append(factor)
                    if len(newFactor.varList) > 0:
                        factorList.append(newFactor)
            factorList = [factor for factor in factorList if factor not in remove_list]
            # print("\t\tfor f in factorlist:")
            # for f in factorList:
                # f.print()
        # print('******************* after evidence')
        # for f in factorList:
            # f.print()

        # print("************************hidden variables:\n")
        for var in orderedListOfHiddenVariables:
            targets = [factor for factor in factorList if var in factor.varList]
            if len(targets) == 0:
                continue

            res = targets[0]
            remove_list = [targets[0]]
            for i in range(1, len(targets)):
                target = targets[i]
                res = res.multiply(target)
                remove_list.append(target)

            res = res.sumout(var)
            factorList = [factor for factor in factorList if factor not in remove_list]
            if res is not None:
                factorList.append(res)
            
            # res.print()


        # print("-------------RESULT:")
        res = factorList[0]
        # for i in factorList:
        #     i.print()

        # print('-------------RESULT END\n')
    
    

        for factor in factorList[1:]:
            res = res.multiply(factor)
            # res.print()

        total = sum(res.cpt.values())
        res.cpt = {k: v/total for k, v in res.cpt.items()}
        res.print()

    @staticmethod
    def printFactors(factorList):
        for factor in factorList:
            factor.print()

class Util:
    @staticmethod
    def to_binary(num, len):
        return format(num, '0' + str(len) + 'b')


class Node:
    def __init__(self, name, var_list):
        self.name = name
        self.varList = var_list
        self.cpt = {}

    def setCpt(self, cpt):
        self.cpt = cpt

    def print(self):
        print("Name = " + self.name)
        print(" vars " + str(self.varList))

        for key in self.cpt:
            print("   key: " + key + " val : " + str(self.cpt[key]))

        print("")

    def multiply(self, factor):
        """function that multiplies with another factor"""
        common = [var for var in factor.varList if var in self.varList]
        common_in_1 = [self.varList.index(var) for var in self.varList if var in common]
        common_in_2 = [factor.varList.index(var) for var in factor.varList if var in common]
        key_len_1 = len(self.varList)
        key_len_2 = len(factor.varList)
        new_cpt = {}
        firstMap = {}
        for key in self.cpt:
            new_key = ''.join([key[i] for i in range(key_len_1) if i in common_in_1])
            rest = ''.join([key[i] for i in range(key_len_1) if i not in common_in_1]) # bad style. d.c
            if new_key not in firstMap:
                firstMap[new_key] = {}
            firstMap[new_key][rest] = self.cpt[key];

        for key in factor.cpt:
            new_key = ''.join([key[i] for i in range(key_len_2) if i in common_in_2])
            rest = ''.join([key[i] for i in range(key_len_2) if i not in common_in_2]) # bad style. d.c
            fp = firstMap[new_key]
            for key2 in fp:
                res_key = new_key + key2 + rest
                new_cpt[res_key] = fp[key2] * factor.cpt[key]

        newList = common + [var for var in self.varList if var not in common] + \
                  [var for var in factor.varList if var not in common]

        new_node = Node("f" + str(newList), newList)
        new_node.setCpt(new_cpt)
        return new_node



    def sumout(self, variable):
        """function that sums out a variable given a factor"""
        # print('<<<<<<<<<',self.cpt)
        if len(self.varList) == 1:
            return None
        index = self.varList.index(variable)
        new_cpt = {}
        new_var_list = self.varList
        del new_var_list[index]
        new_size = 2 ** len(new_var_list)
        for i in range(new_size):
            new_key = str(Util.to_binary(i, len(new_var_list)))
            val1 = self.cpt[new_key[:index] + '0' + new_key[index:]]
            val2 = self.cpt[new_key[:index] + '1' + new_key[index:]]
            new_cpt[new_key] = val1 + val2

        new_node = Node("f" + str(new_var_list), new_var_list)
        new_node.setCpt(new_cpt)
        # print('>>>>>>>>>',new_node.cpt)
        return new_node

    def restrict(self, variable, value):
        """function that restricts a variable to some value in a given factor"""
        index = self.varList.index(variable);
        new_cpt = {}
        for key in self.cpt:
            if key[index] == str(value):
                new_key = key[:index] + key[index + 1:]
                new_cpt[new_key] = self.cpt[key]

        new_var_list = self.varList[:index] + self.varList[index + 1:]
        new_node = Node("f" + str(new_var_list), new_var_list)
        new_node.setCpt(new_cpt)
        return new_node


# create nodes for Bayes Net
FM = Node("FM", ["FM"])
NA = Node("NA", ["NA"])
FS = Node("FS", ["FS"])
FB = Node("FB", ["FB", "FS"])
NDG = Node("NDG", ["NDG", "FM", "NA"])
FH = Node("FH", ["FH", "NDG", "FS", "FM"])

# Generate cpt for each node
FM.setCpt({'0': 1-1/28, '1': 1/28})
NA.setCpt({'0': 1-0.3, '1': 0.3})
FS.setCpt({'0': 1-0.05, '1': 0.05})
FB.setCpt({'11': 0.6, '01': 1-0.6, '10': 0.1, '00': 1-0.1})
NDG.setCpt({'111': 0.8, '011': 1-0.8, '110': 0.4, '010': 0.6, '101': 0.5, '001': 0.5, '100': 0, '000': 1})
FH.setCpt({'1111': 0.99, '0111': 0.01, '1011': 0.9, '0011': 0.1, '1101': 0.65, '0101': 0.35, '1110': 0.75, '0110': 0.25,
           '1010': 0.5, '0010': 0.5, '1100': 0.2, '0100': 0.8, '1001': 0.4, '0001': 0.6, '1000': 0, '0000': 1})


print("Q2 **********************")
VariableElimination.inference([FH, NA, FS, FM, NDG], ['FH'], ['NA', 'NDG', 'FM', 'FS'], {})

print("Q4 **********************")
VariableElimination.inference([FH, FM, NA, FS, NDG, FB], ['FS'], ['NA', 'NDG'],
                              {'FH': 1, 'FM': 1, 'FB': 1})
print("Q5 **********************")
VariableElimination.inference([FH, FM, NA, FS, NDG, FB], ['FS'], ['NDG'],
                              {'FH': 1, 'FM': 1, 'FB': 1, 'NA': 1})

print("Q3 **********************")
VariableElimination.inference([FH, FM, NA, FS, NDG, FB], ['FS'], ['NA', 'NDG', 'FB'], {'FH': 1, 'FM': 1})

