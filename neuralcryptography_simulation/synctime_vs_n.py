from TPM import TPM
import numpy as np
import time
import sys
import matplotlib.pyplot as plt

#Machine parameters
k = 3
n = 1000
l = 3


#Update rule
update_rules = ['hebbian', 'anti_hebbian', 'random_walk']
update_rule = update_rules[0]


#Create 3 machines : Alice, Bob and Eve. Eve will try to intercept the communication between
#Alice and Bob.
#Random number generator
def random(simN):
	return np.random.choice([-1, 1], size=(k,simN))
	#return np.random.randint(-l, l + 1, [k, n])

#Function to evaluate the synchronization score between two machines.
def sync_score(m1, m2):
	#if m2.m == 1:
		return 1.0 - np.average(1.0 * np.abs(m1.W - m2.W)/(2 * l))
	
#Synchronize weights

#print("Initial")
#print(Alice.W)
#print(Bob.W)

#average_time = [0]*10
sync_time=np.zeros((101, 1000))

for i in [25, 50, 100]:

	#sync_time = [0]*100

	for j in range(1000):

		print("Creating TPMs for iteration:" + str(j+1) + " k=" + str(k) + ", n=" + str(i) + ", l=" + str(l))
		Alice = TPM(k, i, l)
		Bob = TPM(k, i, l)

		sync = False # Flag to check if weights are sync
		nb_updates = 0 # Update counter
		alice_t = 0.0
		bob_t = 0.0

		sync_history = [] # to store the sync score after every update

		while(not sync):

			X = random(i) # Create random vector of dimensions [k, n]
			
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
			
			score = 100 * sync_score(Alice, Bob) # Calculate the synchronization of the 2 machines

			sync_history.append(score) # Add sync score to history, so that we can plot a graph later.

			sys.stdout.write('\r' + "Synchronization = " + str(int(score)) + "%   /  Updates = " + str(nb_updates)) 
			if score == 100: # If synchronization score is 100%, set sync flag = True
				sync = True

		sys.stdout.write('\n')
		sync_time[i][j] = (alice_t + bob_t)/2.0*1000

	#average_time[i] = np.average(sync_time)
	#print("Average time for l = " + str(i+1) + " : " + str(average_time[i]) + " seconds.")


print(str(sync_time[25]))
print(str(sync_time[50]))
print(str(sync_time[100]))

common_params = dict(bins=100,range=(0, 1000))
plt.title('Distribution of Synchronisation Time: ')
plt.hist(sync_time[25], **common_params, label='N = 25')
plt.hist(sync_time[50], **common_params, label='N = 50')
plt.hist(sync_time[100], **common_params, label='N = 100')
plt.legend(loc='upper right')
plt.xlabel('t_sync')
plt.ylabel('P(t_sync)')
plt.show()

'''
plt.xticks(tick_list)
plt.xlabel('Synaptic depth(L)')
plt.ylabel('Sync time t(avg)')
plt.title('Synchronization time vs Synaptic depth')
plt.show()
'''

