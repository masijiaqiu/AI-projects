from prison import Player
import random

        
class Copycat(Player):
    def studentID(self):
        return "20739061"
    def agentName(self):
        return "Copycat2"
    def play(self, myHistory, oppHistory1, oppHistory2):
        # print('->',myHistory,oppHistory1,oppHistory2)
        sum_afterC1 = 0.
        sum_afterC2 = 0.
        sum_C1 = 0.
        sum_C2 = 0.
        sum_len = 1.

        if len(oppHistory1)== 0 | len(oppHistory2)== 0:
            return 0
        elif len(oppHistory1)== 1 | len(oppHistory2)== 1:
        	return (oppHistory1[-1] & oppHistory2[-1])
        for i in range(0, len(myHistory)):
        	sum_C1 += oppHistory1[i]
        	sum_C2 += oppHistory2[i]
        	if myHistory[i] == 0:
	        	sum_afterC1 += oppHistory1[i]
	        	sum_afterC2 += oppHistory2[i]
	        	sum_len += 1.

        perc1 = sum_afterC1 / sum_len
        perc2 = sum_afterC2 / sum_len
        
        sumh = oppHistory1[-1] + oppHistory1[-2] + oppHistory2[-1] + oppHistory2[-2]
        # print('percent  :' , perc2)
        if sumh == 0:
            if (perc1 > 0.5) | (perc2 > 0.5):
                return 1

            return 0

        elif sumh == 1:
            if (perc1 < 0.2) & (perc2 < 0.2):
                return 0
            elif(float(sum(myHistory))/len(myHistory) < 0.2) & (float(sum(myHistory))/len(myHistory)< 0.2):
            	return 0              
            return 1
        
        else:

        	return 1


