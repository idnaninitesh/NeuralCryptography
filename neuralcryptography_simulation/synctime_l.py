from TPM import TPM
import numpy as np
import time
import sys

#Machine parameters
k = 3
n = 100
l = 10

#Update rule
update_rules = ['hebbian', 'anti_hebbian', 'random_walk']
update_rule = update_rules[0]
input_methods = ['random']
input_method = input_methods[0]

#Create 3 machines : Alice, Bob and Eve. Eve will try to intercept the communication between
#Alice and Bob.
#Random number generator
def random_input():
	return np.random.choice([-1, 1], size=(k,n))
	#return np.random.randint(-l, l + 1, [k, n])


#Function to evaluate the synchronization score between two machines.
def sync_score(m1, m2, i):
	if m2.m == 1:
		return 1.0 - np.average(1.0 * np.abs(m1.W - m2.W)/(2 * i))
	else:
		ret_value = np.ndarray([m])
		for j in range(m):
			ret_value[j] = 1.0 - np.average(1.0 * np.abs(m1.W - m2.W[j])/(2 * i))
		return ret_value

#Synchronize weights

#print("Initial")
#print(Alice.W)
#print(Bob.W)

random_list = [0]*10

for i in range(l):

	sync_time = [0]*10

	for j in range(10):

		print("Creating TPMs for iteration:" + str(j+1) + " k=" + str(k) + ", n=" + str(n) + ", l=" + str(i+1))
		Alice = TPM(k, n, i+1, 1)
		Bob = TPM(k, n, i+1, 1)

		sync = False # Flag to check if weights are sync
		nb_updates = 0 # Update counter
		alice_t = 0.0
		bob_t = 0.0

		sync_history = [] # to store the sync score after every update

		while(not sync):

			X = random_input() # Create random vector of dimensions [k, n]
					
			start = time.time()
			tauA = Alice(X) # Get output from Alice
			end = time.time()
			alice_t += end-start
			
			start = time.time()
			tauB = Bob(X) # Get output from Bob
			end = time.time()
			bob_t += end-start

			start = time.time()
			Alice.update(tauB, update_rule) # Update Alice with Bob's output
			end = time.time()
			alice_t += end-start

			start = time.time()
			Bob.update(tauA, update_rule) # Update Bob with Alice's output
			end = time.time()
			bob_t += end-start

			nb_updates += 1
			
			score = 100 * sync_score(Alice, Bob, i+1) # Calculate the synchronization of the 2 machines

			sync_history.append(score) # Add sync score to history, so that we can plot a graph later.

			sys.stdout.write('\r' + "Synchronization = " + str(int(score)) + "%   /  Updates = " + str(nb_updates)) 
			if score == 100: # If synchronization score is 100%, set sync flag = True
				sync = True

		sys.stdout.write('\n')
		sync_time[j] = (alice_t + bob_t)/2.0
		print("Time: " + str(sync_time[j]))

	random_list[i] = np.average(sync_time)*10
	print("Average time for l = " + str(i+1) + " : " + str(random_list[i]) + " seconds.")


import matplotlib.pyplot as plt
x_list = [1,2,3,4,5,6,7,8,9,10]
tick_list = [0,1,2,3,4,5,6,7,8,9,10,11]
plt.plot(x_list, random_list, 'go', label='Random input')

plt.xticks(tick_list)
plt.xlabel('Synaptic depth(L)')
plt.ylabel('Sync time t(avg)')
plt.title('Synchronization time vs Synaptic depth')
plt.show()

