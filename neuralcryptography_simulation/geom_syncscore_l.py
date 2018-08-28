from TPM import TPM
import numpy as np
import time
import sys

#Machine parameters
k = 3
n = 100
l = 10
R = 20
m = 1
M = 1000

#Update rule
update_rules = ['hebbian', 'anti_hebbian', 'random_walk']
update_rule = update_rules[0]
input_methods = ['random', 'feedback']
input_method = input_methods[1]
attack = 'geometric'
random_score = [97.38, 89.41, 84.49, 79.72, 77.03, 76.56, 75.07, 73.27, 72.91, 70.06]
feedback_score = [79.35, 73.26, 68.79, 65.15, 60.84, 58.45, 56.24, 55.03, 53.56, 52.25]

#Create 3 machines : Alice, Bob and Eve. Eve will try to intercept the communication between
#Alice and Bob.
#Random number generator

def random_input():
	return np.random.choice([-1, 1], size=(k,n))
	#return np.random.randint(-l, l + 1, [k, n])

def feedback_input(mA, mB, mE, XA, XB, XE):
	
	X_tA = XA
	X_tA = np.roll(X_tA, 1, axis = 1)
	X_tB = XB
	X_tB = np.roll(X_tB, 1, axis = 1)
	X_tE = XE
	X_tE = np.roll(X_tE, 1, axis = 1)

	if mA.tau == mB.tau:
		for i in range(k):
			X_tA[i][0] = mA.sigma[i]
			X_tB[i][0] = mB.sigma[i]
	else:
		for i in range(k):
			X_tA[i][0] = np.random.choice([-1, 1])
			X_tB[i][0] = X_tA[i][0]

	if mA.tau == mE.tau:
		for i in range(k):
			X_tE[i][0] = mE.sigma[i]
	else:
		for i in range(k):
			X_tE[i][0] = np.random.choice([-1, 1])

	return X_tA, X_tB, X_tE

#Function to evaluate the synchronization score between two machines.
def sync_score(m1, m2, i):
	if m2.m == 1:
		#return (1.0 * np.sum(m1.W == m2.W))/(k*n)
		return 1.0 - np.average(1.0 * np.abs(m1.W - m2.W)/(2 * i))
	else:
		ret_value = np.ndarray([m])
		for j in range(m):
			ret_value[j] = 1.0 - np.average(1.0 * np.abs(m1.W - m2.W[j])/(2 * i)) #(1.0 * np.sum(m1.W == m2.W[j]))/(k*n)
		return ret_value

#Synchronize weights

#print("Initial")
#print(Alice.W)
#print(Bob.W)
'''

random_score = [0]*10

for i in range(9,10):

	eve_score = [0]*10

	for j in range(10):

		print("Creating TPMs for iteration:" + str(j+1) + " k=" + str(k) + ", n=" + str(n) + ", l=" + str(i+1))
		Alice = TPM(k, n, i+1, 1)
		Bob = TPM(k, n, i+1, 1)
		Eve = TPM(k, n, i+1, m)

		sync = False # Flag to check if weights are sync
		nb_updates = 0 # Update counter
		
		R_count = 0

		while(not sync):

			if input_method == 'random':
				XA = XB = XE = random_input() # Create random vector of dimensions [k, n]
			else:
				if nb_updates == 0:
					XA = XB = XE = random_input()
				else:
					XA, XB, XE = feedback_input(Alice, Bob, Eve, XA, XB, XE)
					if Alice.tau != Bob.tau:
						R_count += 1

					if R_count >= R:
						R_count = 0
						XA = XB = XE = random_input()

			tauA = Alice(XA) # Get output from Alice
			tauB = Bob(XB) # Get output from Bob
			tauE = Eve(XE)

			Alice.update(tauB, update_rule) # Update Alice with Bob's output
			Bob.update(tauA, update_rule) # Update Bob with Alice's output

			nb_updates += 1

			Eve.perform_attack(nb_updates, M, tauA, tauB, update_rule, attack)

			score = 100 * sync_score(Alice, Bob, i+1) # Calculate the synchronization of the 2 machines

			sys.stdout.write('\r' + "Synchronization = " + str(int(score)) + "%   /  Updates = " + str(nb_updates)) 

			if score == 100: # If synchronization score is 100%, set sync flag = True
				sync = True

		sys.stdout.write('\n')
		eve_score[j] = sync_score(Alice, Eve, i+1)
		print("Score for iteration " + str(j+1) + ": " + str(eve_score[j]*100))

	random_score[i] = np.average(eve_score)*100
	print("Average score for l = " + str(i+1) + " : " + str(random_score[i]) + " seconds.")


'''

import matplotlib.pyplot as plt
x_list = [1,2,3,4,5,6,7,8,9,10]
tick_list = [0,1,2,3,4,5,6,7,8,9,10,11]
plt.plot(x_list, feedback_score, 'ro', label='Feedback mechanism')
plt.plot(x_list, random_score, 'go', label='Random input')
plt.legend(loc='upper right')

plt.xticks(tick_list)
plt.yticks(np.arange(50, 100, 5))
plt.xlabel('Synaptic depth(L)')
plt.ylabel('Sync score ')
plt.title('Synchronization score(Geometric attack) vs Synaptic depth')
plt.show()

