from TPM import TPM
import numpy as np
import time
import sys

#Machine parameters
k = 3
n = 1000
l = 10
m = 1
M = 1000

#Update rule
update_rules = ['hebbian', 'anti_hebbian', 'random_walk']
update_rule = update_rules[0]
attacks = ['simple', 'geometric', 'majority', 'genetic','majority-flipping']
attack = attacks[1]


#Create 3 machines : Alice, Bob and Eve. Eve will try to intercept the communication between
#Alice and Bob.
print("Creating TPMs : k=" + str(k) + ", n=" + str(n) + ", l=" + str(l))
print("Using " + update_rule + " update rule.")
print("Attack performed : " + attack + " attack.")

Alice = TPM(k, n, l, 1)
Bob = TPM(k, n, l, 1)
Eve = TPM(k, n, l, m)

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
		return ret_value

#Synchronize weights

sync = False # Flag to check if weights are sync
nb_updates = 0 # Update counter
nb_eve_updates = 0 # To count the number of times eve updated
alice_t = 0
bob_t = 0
eve_t = 0

sync_history = [] # to store the sync score after every update
eve_history = []
#print("Initial")
#print(Alice.W)
#print(Bob.W)

while(not sync):

	X = random() # Create random vector of dimensions [k, n]
	
	start = time.time()
	tauA = Alice(X) # Get output from Alice
	end = time.time()
	alice_t += end-start
	
	start = time.time()
	tauB = Bob(X) # Get output from Bob
	end = time.time()
	bob_t += end-start

	start = time.time()
	tauE = Eve(X) # Get output from Eve
	end = time.time()
	eve_t += end-start

	start = time.time()
	Alice.update(tauB, update_rule) # Update Alice with Bob's output
	end = time.time()
	alice_t += end-start

	start = time.time()
	Bob.update(tauA, update_rule) # Update Bob with Alice's output
	end = time.time()
	bob_t += end-start
	nb_updates += 1

	#Eve would perform any type of attack 
	start = time.time()
	nb_eve_updates += Eve.perform_attack(nb_updates, M, tauA, tauB, update_rule, attack)
	end = time.time()
	eve_t += end-start
	score = 100 * sync_score(Alice, Bob) # Calculate the synchronization of the 2 machines
	eve_score = 100 * sync_score(Alice, Eve )
	eve_history.append(eve_score)
	sync_history.append(score) # Add sync score to history, so that we can plot a graph later.

	sys.stdout.write('\r' + "Synchronization = " + str(int(score)) + "%   /  Updates = " + str(nb_updates) + " / Eve's updates = " + str(nb_eve_updates))# + '\n') 
	if score == 100: # If synchronization score is 100%, set sync flag = True
		sync = True


sync_time=bob_t
if alice_t > bob_t:
	sync_time=alice_t
#Print results
print ('\nMachines have been synchronized.\n')
print ('Time taken by Alice = ' + str(alice_t)+ " seconds.\n")
print ('Time taken by Bob= ' + str(bob_t)+ " seconds.\n")
print ('Time taken by Eve= ' + str(eve_t)+ " seconds.\n")
print ('Time taken for synchronisation= ' + str(sync_time)+ " seconds.\n")

#See if Eve got what she wanted:
if m == 1:
	eve_score = 100 * sync_score(Alice, Eve)
	if eve_score >= 100:
		print("Eve synced her machine with Alice's and Bob's !")
	else:
		print("Eve's machine is only " + str(eve_score) + " % " + "synced with Alice's and Bob's and she did " + str(nb_eve_updates) + " updates.") 
else:
	eve_score = sync_score(Alice, Eve)
	for j in range(m):
		if eve_score[j] >= 1:
			print("Eve machine " + str(j+1) + " synced her machine with Alice's and Bob's !")
		else:
			print("Eve's machine is only " + str(eve_score[j]*100) + " % " + "synced with Alice's and Bob's and she did " + str(nb_eve_updates) + " updates.") 		

#Plot graph 
import matplotlib.pyplot as mpl
line_up, = mpl.plot(sync_history, label='Bob')
line_down, =mpl.plot(eve_history, label='Eve')
mpl.xlabel("Number of updates")
mpl.ylabel("Synchronisation Score")
mpl.title("Comparison of the learning process of Bob and Eve")
mpl.legend(handles=[line_up, line_down])
mpl.show()
