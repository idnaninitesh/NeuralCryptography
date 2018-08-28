from TPM import TPM
import numpy as np
import time
import sys

#Machine parameters
k = 3
n = 100
l = 4
m = 1
M = 1000
R = 20

#Update rule
update_rules = ['hebbian', 'anti_hebbian', 'random_walk']
update_rule = update_rules[0]
attacks = ['simple', 'geometric', 'majority', 'genetic','majority-flipping']
attack = attacks[1]
input_methods = ['random', 'feedback']
input_method = input_methods[0]
avg_steps = int(9.5*(l*l) + 25)


#Create 3 machines : Alice, Bob and Eve. Eve will try to intercept the communication between
#Alice and Bob.
print("Creating TPMs : k=" + str(k) + ", n=" + str(n) + ", l=" + str(l))
print("Using " + update_rule + " update rule.")
print("Attack performed : " + attack + " attack.")
Alice = TPM(k, n, l, 1)
Bob = TPM(k, n, l, 1)
Eve = TPM(k, n, l, m)

#Random number generator
def random_input():
	return np.random.choice([-1, 1], size=(k,n))
	#return np.random.randint(-l, l + 1, [k, n])

#Feedback input generator
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
def sync_score(m1, m2):
	if m2.m == 1:
		#return (1.0 * np.sum(m1.W == m2.W))/(k*n)
		return 1.0 - np.average(1.0 * np.abs(m1.W - m2.W)/(2 * l))
	else:
		ret_value = np.ndarray([m])
		for j in range(m):
			ret_value[j] = 1.0 - np.average(1.0 * np.abs(m1.W - m2.W[j])/(2 * l)) #(1.0 * np.sum(m1.W == m2.W[j]))/(k*n)
		return ret_value


def geneticSyncScore(m1, m2, geneticM):
		ret_value = np.ndarray([geneticM])
		for j in range(geneticM):
			ret_value[j] = 1.0 - np.average(1.0 * np.abs(m1.W - m2.W[j])/(2 * l))
		return ret_value

#Synchronize weights

sync = False # Flag to check if weights are sync
nb_updates = 0 # Update counter
nb_eve_updates = 0 # To count the number of times eve updated
R_count = 0

alice_t = 0.0
bob_t = 0.0
eve_t = 0.0

sync_history = [] # to store the sync score after every update

#print("Initial")
#print(Alice.W)
#print(Bob.W)

while(not sync):

	#X = random_input() # Create random vector of dimensions [k, n]
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

	#if nb_updates <= 50:
	#	print(XA)
	#	print(XB)
	#	print(XE)

	start = time.time()
	tauA = Alice(XA) # Get output from Alice
	end = time.time()
	alice_t += end-start
	
	start = time.time()
	tauB = Bob(XB) # Get output from Bob
	end = time.time()
	bob_t += end-start

	start = time.time()
	tauE = Eve(XE) # Get output from Eve
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
	#print(X)
	#print(Alice.W)
	#print(Bob.W)
	#print(Eve.W)

	#print("A: " + str(tauA))
	#print("B: " + str(tauB))
	#print("E: " + str(tauE))

	nb_updates += 1

	#Eve would perform any type of attack 
	start = time.time()
	nb_eve_updates += Eve.perform_attack(nb_updates, M, tauA, tauB, update_rule, attack, avg_steps)
	end = time.time()
	eve_t += end-start
	
	score = 100 * sync_score(Alice, Bob) # Calculate the synchronization of the 2 machines

	sync_history.append(score) # Add sync score to history, so that we can plot a graph later.

	sys.stdout.write('\r' + "Synchronization = " + str(int(score)) + "%   /  Updates = " + str(nb_updates) + " / Eve's updates = " + str(nb_eve_updates))# + '\n') 
	if score == 100: # If synchronization score is 100%, set sync flag = True
		sync = True


sync_time=(alice_t + bob_t)/2.0

#Print results
print ('\nMachines have been synchronized.')
print ('Alice: ' + str(alice_t) + ' seconds.')
print ('Bob: ' + str(bob_t) + ' seconds.')
print ('Eve: ' + str(eve_t) + ' seconds.')
print ('Time taken = ' + str(sync_time)+ " seconds.")

#See if Eve got what she wanted:
if attack == attacks[3]:
	geneticM = Eve.getM()
	eve_score = geneticSyncScore(Alice, Eve, geneticM)
	print("Number of machines: "+str(geneticM))
	for j in range(geneticM):
		if eve_score[j] >= 1:
			print("Eve's machine " + str(j+1) + " synced her machine with Alice's and Bob's !")
		else:
			print("Eve's machine is only " + str(eve_score[j]*100) + " % " + "synced with Alice's and Bob's and she did " + str(nb_eve_updates) + " updates.") 	



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

import matplotlib.pyplot as plt
plt.plot(sync_history)
plt.show()
