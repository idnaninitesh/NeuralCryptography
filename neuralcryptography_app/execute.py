from tkinter import *
from tkinter.ttk import Separator

from TPM import TPM
import numpy as np
import time
import sys

#Random number generator
def random(K, N, SEED):
	state = np.random.RandomState(SEED)
	return state.choice([-1, 1], size=(K,N))

#Function to evaluate the synchronization score between two machines.
def sync_score(m1, m2, L):
		return 1.0 - np.average(1.0 * np.abs(m1.W - m2.W)/(2 * L))

def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

def display_weights(root, weightA = None, weightB = None):

	weightAFrame = Frame(root.weightACanvas, bg = 'black')
	weightBFrame = Frame(root.weightBCanvas, bg = 'black')

	if root.K >= 7:
		weightAvsb = Scrollbar(root, orient = "vertical", command = root.weightACanvas.yview)
		root.weightACanvas.configure(yscrollcommand = weightAvsb.set)
		weightAvsb.grid(row = 8, column = 2, rowspan = 4, sticky = "nsw")

		weightBvsb = Scrollbar(root, orient = "vertical", command = root.weightBCanvas.yview)
		root.weightBCanvas.configure(yscrollcommand = weightBvsb.set)
		weightBvsb.grid(row = 8, column = 5, rowspan = 4, sticky = "nsw")


	if root.N >= 6:
		weightAhsb = Scrollbar(root, orient = "horizontal", command = root.weightACanvas.xview)
		root.weightACanvas.configure(xscrollcommand = weightAhsb.set)
		weightAhsb.grid(row = 12, column = 0, columnspan = 2, sticky = "ewn")

		weightBhsb = Scrollbar(root, orient = "horizontal", command = root.weightBCanvas.xview)
		root.weightBCanvas.configure(xscrollcommand = weightBhsb.set)
		weightBhsb.grid(row = 12, column = 3, columnspan = 2, sticky = "ewn")


	root.weightACanvas.create_window((0, 0), window = weightAFrame, anchor = "nw")
	root.weightBCanvas.create_window((0, 0), window = weightBFrame, anchor = "nw")	

	if root.K >= 7 or root.N >= 6:
		weightAFrame.bind("<Configure>", lambda event, canvas = root.weightACanvas: onFrameConfigure(root.weightACanvas))
		weightBFrame.bind("<Configure>", lambda event, canvas = root.weightBCanvas: onFrameConfigure(root.weightBCanvas))

	_widgets = []
	for row in range(root.K):
		current_row = []
		for column in range(root.N):
			label = Label(weightAFrame, text="%s" %weightA[row][column], 
							borderwidth=1, width=5)
			label.grid(row = 8 + row, column = column, sticky = "nw", padx = 1, pady = 1)
			current_row.append(label)
			_widgets.append(current_row)

	_widgets = []
	for row in range(root.K):
		current_row = []
		for column in range(root.N):
			label = Label(weightBFrame, text="%s" %weightB[row][column], 
							borderwidth=1, width=5)
			label.grid(row = 8 + row, column = 3 + column, sticky = "nw", padx = 1, pady = 1)
			current_row.append(label)
			_widgets.append(current_row)

	

def sync_weights(root, K = 3, N = 10, L = 4, MAX_ITERATIONS = 1000, SEED = 12345, delay = 0.001):

	#Update rule
	update_rules = ['hebbian', 'anti_hebbian', 'random_walk']
	update_rule = update_rules[0]


	#Create 2 machines : Alice and Bob for communication
	#Alice and Bob.
	Alice = TPM(K, N, L)
	Bob = TPM(K, N, L)

	display_weights(root, Alice.W, Bob. W)
	root.update()

	nb_updates = 0 # Update counter

	
	for i in range(MAX_ITERATIONS):

		X = random(K, N, SEED) # Create random vector of dimensions [k, n]
		
		tauA = Alice(X) # Get output from Alice
		
		tauB = Bob(X) # Get output from Bob

		Alice.update(tauB, update_rule) # Update Alice with Bob's output

		Bob.update(tauA, update_rule) # Update Bob with Alice's output

		#display_weights(root, Alice.W, Bob.W)

		score = 100 * sync_score(Alice, Bob, L)
		
		if score != 100:
			nb_updates += 1
			root.totalIterEntry.config(state = 'normal')
			root.totalIterEntry.delete(0, END)
			root.totalIterEntry.insert(0, str(nb_updates))
			root.totalIterEntry.config(state = 'readonly')

		root.maxIterEntry.config(state = 'normal')
		root.maxIterEntry.delete(0, END)
		root.maxIterEntry.insert(0, str(i+1))
		root.maxIterEntry.config(state = 'readonly')

		SEED = SEED + 1
		
		root.update()

		if delay > 0:
			time.sleep(delay)

	if score != 100:
		print("Not Synchronized!")
	
	display_weights(root, Alice.W, Bob.W)	
	
	return Alice.W, Bob.W, nb_updates