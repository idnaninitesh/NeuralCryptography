from learning_rules import hebbian, anti_hebbian, random_walk
import numpy as np


class TPM:
	'''TPM
	A tree parity machine. Generates a binary digit(tau) for a given random vector(X).
	The machine can be described by the following parameters:
	k - The number of hidden neurons
	n - Then number of input neurons connected to each hidden neuron
	l - Defines the range of each weight ({-L, ..., -2, -1, 0, 1, 2, ..., +L })
	W - The weight matrix between input and hidden layers. Dimensions : [M, K, N]
	'''
	def __init__(self, k=3, n=4, l=6):
		'''
		Arguments:
		k - The number of hidden neurons
		n - Then number of input neurons connected to each hidden neuron
		l - Defines the range of each weight ({-L, ..., -2, -1, 0, 1, 2, ..., +L })	'''

		self.k = k
		self.n = n
		self.l = l
		self.W = np.random.randint(-l, l + 1, [k, n])

	def get_output(self, X):
		'''
		Returns a binary digit tau for a given random vecor.
		Arguments:
		X - Input random vector
		'''

		k = self.k
		n = self.n
		W = self.W
		X = X.reshape([k, n])

		h = np.sum(X * W, axis=1);
		sigma = np.sign(h) # Compute inner activation sigma Dimension:[K]
		for n,i in enumerate(sigma):
			if i == 0:
				sigma[n] = -1

		tau = np.prod(sigma) # The final output


		self.X = X
		self.h = h
		self.sigma = sigma
		self.tau = tau

		return tau

	def __call__(self, X):
		return self.get_output(X)

	def update(self, tau2, update_rule='hebbian'):
		'''
		Updates the weights according to the specified update rule.

		Arguments:
		tau2 - Output bit from the other machine;

		update_rule - The update rule. 
		Should be one of ['hebbian', 'anti_hebbian', random_walk']

		j -  Index of machine whose weight is to be considered( used by attacker )
		'''

		X = self.X
		sigma = self.sigma
		W = self.W
		l = self.l

		tau1 = self.tau
		if (tau1 == tau2):
			if update_rule == 'hebbian':
				hebbian(W, X, sigma, tau1, tau2, l)
			elif update_rule == 'anti_hebbian':
				anti_hebbian(W, X, sigma, tau1, tau2, l)
			elif update_rule == 'random_walk':
				random_walk(W, X, sigma, tau1, tau2, l)
			else:
				raise Exception("Invalid update rule. Valid update rules are: " + 
					"\'hebbian\', \'anti_hebbian\' and \'random_walk\'.")
