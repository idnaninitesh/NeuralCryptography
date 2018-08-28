from TPM import TPM
import numpy as np
import time
import sys


#Machine parameters
k = 3
n = 100
l = 15
m = 1
#Update rule
update_rules = ['hebbian', 'anti_hebbian', 'random_walk']
update_rule = update_rules[0]
attacks = ['geometric', 'majority-flipping']

g_list = []
m_list = []


#Create 3 machines : Alice, Bob and Eve. Eve will try to intercept the communication between
#Alice and Bob.
#Random number generator
def random():
	return np.random.choice([-1, 1], size=(k,n))
	#return np.random.randint(-l, l + 1, [k, n])

#Function to evaluate the synchronization score between two machines.
def sync_score(m1, m2):
	if m2.m == 1:
		return 1.0 - np.average(1.0 * np.abs(m1.W - m2.W)/(2 * l))
	else:
		ret_value = np.ndarray([m])
		for j in range(m):
			ret_value[j] = 1.0 - np.average(1.0 * np.abs(m1.W - m2.W[j])/(2 * l))
		return ret_value[np.argmax(ret_value)]

for ind in range(2):
	
	attack = attacks[ind]

	if ind == 1:
		m = 100

	for i in range(l):

		#succ_count = 0
		count_85 = 0
		count_80 = 0
		count_75 = 0
		count_70 = 0
		count_0 = 0
		eve_avg = 0

		print("L = " + str(i+1))
		avg_steps = int(9.5*(i+1)*(i+1) + 25)

		for j in range(10):

			Alice = TPM(k, n, i+1, 1)
			Bob = TPM(k, n, i+1, 1)
			Eve = TPM(k, n, i+1, m)
			sync = False # Flag to check if weights are sync
			nb_updates = 0

			while(not sync):

				X = random() # Create random vector of dimensions [k, n]
				
				tauA = Alice(X) # Get output from Alice
				tauB = Bob(X) # Get output from Bob
				tauE = Eve(X) # Get output from Eve
			
				Alice.update(tauB, update_rule) # Update Alice with Bob's output
				Bob.update(tauA, update_rule) # Update Bob with Alice's output
			
				nb_updates += 1


				Eve.perform_attack(nb_updates, 0, tauA, tauB, update_rule, attack, avg_steps)
				
				score = 100 * sync_score(Alice, Bob) # Calculate the synchronization of the 2 machines

				if score == 100: # If synchronization score is 100%, set sync flag = True
					sync = True
			

			eve_score=100*sync_score(Alice, Eve)
			eve_avg += eve_score

			if ind == 0:			# geometric attack
				if eve_score >= 85:
					count_85 += 1
				elif eve_score >= 80:
					count_80 += 1
				elif eve_score >= 75:
					count_75 += 1
				elif eve_score >= 70:
					count_70 += 1
				else:
					count_0 += 1
			else:					# majority flipping attack
				#score_sum += np.average(eve_score)
				flag_85 = 0
				flag_80 = 0
				flag_75 = 0
				flag_70 = 0
				flag_0 = 0

				if eve_score >= 85:
					if flag_85 == 0:
						flag_85 = 1
						count_85 += 1
				elif eve_score >= 80:
					if flag_80 == 0:
						flag_80 = 1
						count_80 += 1
				elif eve_score >= 75:
					if flag_75 == 0:
						flag_75 = 1
						count_75 += 1
				elif eve_score >= 70:
					if flag_70 == 0:
						flag_70 = 1
						count_70 += 1
				else:
					if flag_0 == 0:
						flag_0 = 1
						count_0 += 1

'''
				for ind in range(m):		
					if eve_score[ind] >= 80:
						succ_count += 1
						break
'''
		
		eve_avg = eve_avg/10

		#print("Count > 85 : " + str(count_85))
		#print("Count > 80 : " + str(count_80))
		#print("Count > 75 : " + str(count_75))
		#print("Count > 70 : " + str(count_70))
		#print("Count < 70 : " + str(count_0))
		print("Average score : " + str(eve_avg))
		if ind == 0:
			g_list.append(eve_avg)
		else:
			m_list.append(eve_avg)

		#print("Average: " + str(average_sync_score[i]))
		#print("Count: " + str(succ_count))


import matplotlib.pyplot as plt

x_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

tick_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
plt.plot(x_list, g_list, 'ro', label='Geometric attack')
plt.plot(x_list, m_list, 'go', label='Majority flipping attack')
plt.legend(loc='upper right')
plt.xticks(tick_list)
#plt.ylim(50,100)
plt.yticks(np.arange(50, 100, 5))
plt.xlabel('Synaptic depth(L)')
plt.ylabel('Synchronization score')
plt.title('Synchronization score vs Synaptic depth')
plt.show()
