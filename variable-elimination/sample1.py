
import numpy as np
from copy import copy
np.set_printoptions(suppress=True)
#define the integer mapping for variables
#FS=100
#FB=101
#FM=102
#NA=103
#FH=104
#NDG=105
#Probability=200
map1={'FS':100,'FB':101,'FM':102,'NA':103,'FH':104,'NDG':105}

#NOW WE CAN GO AHEAD AND STOR ETHE CPTS
FS=np.array([[100,200],[0,0.95],[1,0.05]])

# print 'FS is ',FS

FB=np.array([[101,100,200],[1,1,0.6],[0,1,0.4],[1,0,0.1],[0,0,0.9]])

# print 'FB is ',FB

FM=np.array([[102,200],[1,0.036],[0,0.964]])

#print 'FM is ',FM

NA=np.array([[103,200],[1,0.3],[0,0.7]])

#print 'NA is ',NA

NDG=np.array([[105,102,103,200],[1,0,0,0],[1,0,1,0.5],[1,1,0,0.4],[1,1,1,0.8],[0,0,0,1],[0,0,1,0.5],[0,1,0,0.6],[0,1,1,0.2]])

#print 'NDG is \n',NDG

FH=np.array([[104,102,105,100,200],[1,1,1,1,0.99],[1,0,0,0,0],[1,0,0,1,0.5],[1,0,1,1,0.75],[1,1,0,1,0.9],[1,1,1,0,0.65],[1,1,0,0,0.4],[1,0,1,0,0.2],[0,1,1,1,0.01],[0,0,0,0,1],[0,0,0,1,0.5],[0,0,1,1,0.25],[0,1,0,1,0.1],[0,1,1,0,0.35],[0,1,0,0,0.6],[0,0,1,0,0.8]])

# print 'FH is \n',FH

def restrict(factor, variable, value):
    #let factor be the array that stores the CPT which has the variable in its
    factor=copy(factor)
    #print 'in restrict factor is ',factor
    index1=np.where(factor[0]==variable)
    #print 'index1 is ',index1
    rows=np.where(factor[:,index1[0][0]]==value)[0]#, returns a array of row numbers
    reducedFactor=copy(factor[0])
    for row in rows:
        reducedFactor=np.vstack((reducedFactor,factor[row]))
    
    return reducedFactor
    
 
#trial with reducing NDG where FM=1




def returnConsistentRows(rowArray,list1,factor2,checkAmongColumns):
    
    consistentRows=[]
    for i in rowArray:
        #first construct list for the second factor2
        values=[]
        for j in checkAmongColumns:
            values.append(factor2[i,j])
        
        if cmp(values,list1)==0:
            consistentRows.append(i)
           
    consistentRows=np.asarray(consistentRows)
    return consistentRows
            
    

def multiply(factor1, factor2):
    
    c1=factor1.shape[1]
    c2=factor2.shape[1]
    
    if c1>c2:
        temp=copy(factor1)
        factor1=copy(factor2)
        factor2=copy(temp)
    
    s1=set(factor1[0].tolist())
    s2=set(factor2[0].tolist())
    
    ss1=s1
    ss1=ss1.intersection(s2)
    ss1.remove(200)
    variable=ss1.pop() #since we check all the common variables, any variable would do 
    #ss1.remove(variable)
    #print 'the other common rows are ',ss1
    otherColumnsInFactor1=[]
    otherColumnsInFactor2=[]
    for i in ss1:
        otherColumnsInFactor1.append(np.where(factor1[0]==i)[0][0])
        otherColumnsInFactor2.append(np.where(factor2[0]==i)[0][0])
    
    #now we have the list of column numbers that need to be checked in order to do keep track of the consistent objects
    
    
    
    s1=s1-s2    #this will give the  elements of the first factor which are not there in the second factor
    
    product=np.array([]) # make a 
    
    for i in s1:
        product=np.hstack((product,i))
    product=np.hstack((product,factor2[0])) # now we have the product terms that will be there in the factor for 
    #print 'product is ',product
    #so now factor1 is the one with the lesser factors, and the procedure for doing it is as follows
    #1) Iterate through the first factor row by rows
    #2)For each row, chec what value the joining variable has
    #3)For that value of the variable get all the rows for the second factor1
    #4)After that multiply the respective probabilities and then combine the respective columns
    indexOfVariableInFactor1=np.where(factor1[0]==variable)[0][0]
    #print 'indexOfVariableInFactor1 is ',indexOfVariableInFactor1
    indexOfVariableInFactor2=np.where(factor2[0]==variable)[0][0]
    #print 'indexOfVariableInFactor2 is ',indexOfVariableInFactor2
    
    #To ease things up, we can create an array with the rows and columns such that thise particular columns are not there in the other array
    #so the set s1 contains the columns that are not there in the second array
    
    tempArray=np.array([])
    k=1
    for i in s1:
        index1=np.where(factor1[0]==i)[0][0]
        tempArray=np.hstack((tempArray,factor1[:,index1]))
        tempArray=tempArray.reshape(-1,k)
        k=k+1
        
    #print 'the temp array is ',tempArray
    #print 'the temp array is ',tempArray.shape
    #now the tempArray contains the part where we have just the columns that are not in factor2
    
    #now we can procedd with multiplying 
    for i in range(1,factor1.shape[0]):
        otherColumnsValuesinFactor1=[]
        for idx in otherColumnsInFactor1:
            otherColumnsValuesinFactor1.append(factor1[i,idx])
        #so now we have for each row the columns values for checking the consistency among different columns
        
        #check the first row , and most importantly check the value of the common variables
        val1=factor1[i,indexOfVariableInFactor1]
        val2=factor2[i,indexOfVariableInFactor2]
        #print 'val1 is  ',val1
        #now filter out those values of rows in factor2
        arr2=np.where(factor2[:,indexOfVariableInFactor2]==val1)[0]
        #now arr2 contains the array that will have the rows with value of the variable in factor1
        #We need to change over here , check for consistency between columns
        arr2=copy(returnConsistentRows(arr2,otherColumnsValuesinFactor1,factor2,otherColumnsInFactor2))
        temp2=np.array([])
        if tempArray.shape[0]>0:
            for j in range(0,tempArray.shape[1]):
                temp2=np.hstack((temp2,tempArray[i,j]))# so we first insert the variable which is not in factor2
        
        
        for k in range(0,arr2.shape[0]):
            temp=np.array([])
            
            temp=np.hstack((temp,temp2))
            temp=np.hstack((temp,factor2[arr2[k]]))
            temp[-1]=temp[-1]*factor1[i,-1]
            product=np.vstack((product,temp))
    
    #print 'the product is \n',product
    #print 'the product is \n',product.shape
    return product


ndgFh=copy(multiply(NDG,FH))


def findOtherRow(factor,rowNum,variableColumn,triedRows):
    val1=factor[rowNum,variableColumn]
    if val1==0:
        val2=1
    else:
        val2=0
    #first build the first List without without the variable to be summed up
    arr1=copy(factor[rowNum,0:variableColumn])
    arr1=copy(np.hstack((arr1,factor[rowNum,variableColumn+1:-1])))
    arr1=arr1.tolist()
    

    #print 'arr1 is ',arr1
    #now find the row with the same elements except for the summing out variable
    arr2=np.where(factor[:,variableColumn]==val2)[0] #find all the rows with the oppsite values
   #print 'arr2 is ',arr2
    for i in range(0,arr2.shape[0]):
        if len(triedRows)>0 and arr2[i] in triedRows:
            continue
        arr3=copy(factor[arr2[i],0:variableColumn])
        arr3=copy(np.hstack((arr3,factor[arr2[i],variableColumn+1:-1])))
        arr3=arr3.tolist()
        #print 'arr3 is ',arr3
        if cmp(arr1,arr3)==0:
            # i,e if the two lists are same, then return the sum of the probabilities in their rows
            arr3.append(factor[rowNum,-1]+factor[arr2[i],-1])
            arr3=np.asarray(arr3)
            
            return arr3,arr2[i]
            
            
    #so in this we return the sum of the 2 rows for the variable 
    
        
def sumout(factor, variable):
    #print 'factor is ',factor
    index=np.where(factor[0]==variable)[0][0]
    #print 'the index is ',index
    sumout=copy(factor[0,0:index])
    sumout=copy(np.hstack((sumout,factor[0,index+1:])))
    #print 'sumout is ',sumout
    triedRows=set()
    
    for i in range(1,factor.shape[0]):
        if i in triedRows:
            continue
        arr3,otherRow=findOtherRow(factor,i,index,triedRows)
        #print 'arr3 is ',arr3,' and otherRow is ',otherRow,' triedRowsis ',triedRows
        sumout=copy(np.vstack((sumout,arr3)))
        triedRows.add(i)
        triedRows.add(otherRow)
        
    
    #print 'Sumout is \n',sumout
    #print 'shape of sumout is ',sumout.shape
    return sumout
#print '\n\nndgfh is \n',ndgFh    
#sumout(ndgFh,102)    


#print '\n\n\n\n\n\n\n'
# def inference(factorList, queryVariables, orderedListOfHiddenVariables, evidenceList):
    
#     print '\nin inference\n\n'
#     #first multiply all the factors over that hidden variable and then sum them up
#     factor1=factorList[0]
#     factor2=factorList[1]
#     factor3=copy(multiply(factor1,factor2))
#     print 'current factor is \n',factor3
#     if len(factorList) > 2 :
#         for i in range(2,len(factorList)):
#             factor3=copy(multiply(factor3,factorList[i]))
#             print 'current factor is \n',factor3
   
#     finalFactor=copy(sumout(factor3,orderedListOfHiddenVariables[0]))
    
#     return finalFactor
            
def isValid(factor1,factor2):
    s1=set(factor1[0].tolist())
    s2=set(factor2[0].tolist())
    s3=s1.intersection(s2)
    if(len(s3)>1):
        return 1
    else:
        return 0
        


def normalize(factor):
    normalizationFator=sum(factor[1:,-1])
    for i in range(1,factor.shape[0]):
        factor[i,-1]=factor[i,-1]/normalizationFator
    
    return factor



def inference3(factorList, queryVariables, orderedListOfHiddenVariables, evidenceList):
    
    #now hidden variables actually contains the variables, factorlist contains the reduced factors
    #print 'factorList is ',factorList
    #PRINT THE INITIAL FACTORS
    print 'The initial factors are\n'
    for factor in factorList:
        print factor,'\n'
    for hiddenVariable in orderedListOfHiddenVariables:
        
        #1)make the factorList of all the factors with the given hidden variable
        factorList2=[]
        indexesToRemove=[]
        #print 'len(factorList) is ',len(factorList)
        for i in range(0,len(factorList)):
            #print 'i is ',i
            f=copy(factorList[i])
            s1=set(f[0].tolist())
            if hiddenVariable in s1:
                #means that the factor contains that hiddenVariable
                #1)Remove that factor from the original factorList
                factorList2.append(factorList[i])
                #factorList.pop(i) 
                indexesToRemove.append(i)
        #print 'len(factorList) is ',len(factorList)
        indexesToRemove=copy(np.asarray(indexesToRemove))
        for index in range(0,len(indexesToRemove)):
            #print 'index is ',index
            factorList.pop(indexesToRemove[index])
            indexesToRemove=indexesToRemove-1
            
               
        #2)once we have the factors with that hidden variables present , we can run our usual inference task on it, provided it has more than 2 factors
        print 'Now doing Variable Elimination \n'
        if len(factorList2) ==1:
            reducedFactor=copy(sumout(factorList2[0],hiddenVariable))
            print reducedFactor,'\n'
            factorList.append(reducedFactor)
        else:
            factor1=copy(factorList2[0])
            factor2=copy(factorList2[1])
            factor3=copy(multiply(factor1,factor2))
            if len(factorList2) > 2 :
                for i in range(2,len(factorList2)):
                    factor3=copy(multiply(factor3,factorList2[i]))
                    print factor3,'\n'
                #print 'current factor is \n',factor3
                
            
            reducedFactor=copy(sumout(factor3,hiddenVariable))
            print reducedFactor,'\n'
            factorList.append(reducedFactor)
       #now once we have eliminated all the hidden variables in all the factors we can simply multiply all the remaining factors to get our result
       
    factor1=factorList[0]
    factorList.remove(factorList[0])
    while len(factorList)>0:
        factor2=factorList[0]
        factorList.remove(factorList[0])
        if isValid(factor1,factor2)==1:
            factor1=copy(multiply(factor1,factor2))
            print factor1,'\n'
            #print 'now factor1 is ',factor1
        else:
            factorList.append(factor2)  

    return factor1       
             



#Q2


factorList=[NDG,NA,FM,FH,FS]
queryVariables=[FH]
orderedListOfHiddenVariables=[103,102,105,100]
evidenceList=[]
res1=copy(inference3(factorList, queryVariables, orderedListOfHiddenVariables, evidenceList))
print '\nQ2 answer is \n',res1


#----------------------------------------------------------------------------------------#
# For Question 3 #
# print '\n\n now Q3 begins\n\n'



# fh2=copy(FH)
# fm=copy(FM)
# NDG2=copy(NDG)

# fm=copy(restrict(fm,102,1))

# fh2=copy(restrict(fh2,102,1))
# fh2=copy(restrict(fh2,104,1))
# NDG2=copy(restrict(NDG2,102,1))
# fm=copy(restrict(fm,102,1))








#print '\n\n now trying inference3\n\n'
# factorList=[NDG2,NA,fm,fh2,FS]
# queryVariables=[FS]
# orderedListOfHiddenVariables=[103,105]
# evidenceList=[FM,FH]
# res2=copy(inference3(factorList, queryVariables, orderedListOfHiddenVariables, evidenceList))
# # res2=copy(normalize(res2))
# print '\nQ3 answer  is \n',res2



# #Now starting Q4
# print '\n\n\n\n\n'

# fb=copy(restrict(FB,101,1))
# fm3=copy(restrict(FM,102,1))
# NDG3=copy(restrict(NDG,102,1))
# fh3=copy(restrict(FH,102,1))
# fh3=copy(restrict(fh3,104,1))



# #first sumout FH too from the last factor then multiply all the remaining factors




# #print '\n\n now trying inference3\n\n'
# factorList=[NDG3,NA,fm3,fh3,FS,fb]
# queryVariables=[FS]
# orderedListOfHiddenVariables=[103,105]
# evidenceList=[FM,FH]
# res3=copy(inference3(factorList, queryVariables, orderedListOfHiddenVariables, evidenceList))
# res3=copy(normalize(res3))
# print 'Q4 answer P(FS|FH,FB,FM) is \n',res3




#now starting part 5

#print '\n\n\n\n\n\n'

fb4=copy(restrict(FB,101,1))
fm4=copy(restrict(FM,102,1))

fh4=copy(restrict(FH,102,1))
fh4=copy(restrict(fh4,104,1))
na4=copy(restrict(NA,103,1))
NDG4=copy(restrict(NDG,102,1))
NDG4=copy(restrict(NDG4,103,1))



#so in this case there is only one inference with NDG and 





#print '\n\n now trying inference3\n\n'
factorList=[NDG4,na4,fm4,fh4,FS,fb4]
queryVariables=[FS]
orderedListOfHiddenVariables=[105]
evidenceList=[FM,FH,NA,FB]
res4=copy(inference3(factorList, queryVariables, orderedListOfHiddenVariables, evidenceList))
res4=copy(normalize(res4))
print 'Q5 answer P(FS|FH,FM,NA,FB) is \n',res4
