import execute as ex

from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto import Random

from tkinter import *
from tkinter.ttk import Separator
import base64
import numpy as np

bgcolor = '#D3D3D3'

nLabel = lLabel = delayLabel = None
kEntry = nEntry = lEntry = delayEntry = None

syncButton = None

wLabel = None
machineALabel = machineBLabel = None

totalIterLabel = maxIterLabel = keyLengthLabel = keyLabel = None
totalIterEntry = maxIterEntry = keyLengthEntry = keyEntry = None

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[:-ord(s[len(s)-1:])]


def create_param(root):

	root.paramLabel = Label(root, text = "Machine Parameters", bg = bgcolor)

	root.kLabel = Label(root, text = "K ", bg = bgcolor)
	root.nLabel = Label(root, text = "N ", bg = bgcolor)
	root.lLabel = Label(root, text = "L ", bg = bgcolor)
	root.delayLabel = Label(root, text = "Time Delay(sec) ", bg = bgcolor)

	root.kEntry = Entry(root)
	root.kEntry.insert(END, '3')
	root.nEntry = Entry(root)
	root.nEntry.insert(END, '10')
	root.lEntry = Entry(root)
	root.lEntry.insert(END, '4')
	root.delayEntry = Entry(root)
	root.delayEntry.insert(END, '0')

	syncButton = Button(root, text = "Synchronize weights", bg = bgcolor, command = handle_sync)

	emptyLabel2 = Label(root, text = "", bg = bgcolor)

	horSeparator = Separator(root, orient = "horizontal")

	root.paramLabel.grid(row = 0, columnspan = 5)

	root.kLabel.grid(row = 1, column = 0, sticky = "W")
	root.nLabel.grid(row = 1, column = 2, sticky = "W")
	root.lLabel.grid(row = 2, column = 0, sticky = "W")
	root.delayLabel.grid(row = 2, column = 2, sticky = "W")

	root.kEntry.config(highlightbackground = bgcolor)
	root.nEntry.config(highlightbackground = bgcolor)
	root.lEntry.config(highlightbackground = bgcolor)
	root.delayEntry.config(highlightbackground = bgcolor)

	root.kEntry.grid(row = 1, column = 1)
	root.nEntry.grid(row = 1, column = 3)
	root.lEntry.grid(row = 2, column = 1)
	root.delayEntry.grid(row = 2, column = 3)

	syncButton.config(highlightbackground = bgcolor)

	syncButton.grid(row = 1, column = 4, rowspan = 2)

	emptyLabel2.grid(row = 3, columnspan = 5)

	horSeparator.grid(row = 4, columnspan = 5, sticky = "EW")


def create_weights(root):

	emptyLabel1 = Label(root, text = "", bg = bgcolor)

	root.wLabel = Label(root, text = "Weights of Tree Parity Machines", bg = bgcolor)

	root.machineALabel = Label(root, text = "Machine A", bg = bgcolor)
	root.machineBLabel = Label(root, text = "Machine B", bg = bgcolor)

	root.weightACanvas = Canvas(root, width=300, height=150, bg = bgcolor)
	root.weightBCanvas = Canvas(root, width=300, height=150, bg = bgcolor)

	#ex.display_weights(root)

	'''
	weightAFrame = Frame(weightACanvas, bg = 'black')
	weightBFrame = Frame(weightBCanvas, bg = 'black')

	weightAvsb = Scrollbar(root, orient = "vertical", command = weightACanvas.yview)
	weightACanvas.configure(yscrollcommand = weightAvsb.set)
	weightAhsb = Scrollbar(root, orient = "horizontal", command = weightACanvas.xview)
	weightACanvas.configure(xscrollcommand = weightAhsb.set)

	weightBvsb = Scrollbar(root, orient = "vertical", command = weightBCanvas.yview)
	weightBCanvas.configure(yscrollcommand = weightBvsb.set)
	weightBhsb = Scrollbar(root, orient = "horizontal", command = weightBCanvas.xview)
	weightBCanvas.configure(xscrollcommand = weightBhsb.set)

	weightACanvas.create_window((0, 0), window = weightAFrame, anchor = "nw")
	weightBCanvas.create_window((0, 0), window = weightBFrame, anchor = "nw")	

	weightAFrame.bind("<Configure>", lambda event, canvas=weightACanvas: onFrameConfigure(weightACanvas))
	weightBFrame.bind("<Configure>", lambda event, canvas=weightBCanvas: onFrameConfigure(weightBCanvas))

	_widgets = []
	for row in range(10):
		current_row = []
		for column in range(10):
			label = Label(weightAFrame, text="%s/%s" % (row, column), 
							borderwidth=1, width=5)
			label.grid(row = 8 + row, column = column, sticky = "nw", padx = 1, pady = 1)
			current_row.append(label)
			_widgets.append(current_row)

	_widgets = []
	for row in range(10):
		current_row = []
		for column in range(10):
			label = Label(weightBFrame, text="%s/%s" % (row, column), 
							borderwidth=1, width=5)
			label.grid(row = 8 + row, column = 3 + column, sticky = "nw", padx = 1, pady = 1)
			current_row.append(label)
			_widgets.append(current_row)

	'''

	emptyLabel2 = Label(root, text = "", bg = bgcolor)

	verSeparator = Separator(root, orient = "vertical")

	horSeparator = Separator(root, orient = "horizontal")

	emptyLabel1.grid(row = 5, columnspan = 5)

	root.wLabel.grid(row = 6, columnspan = 5)

	root.machineALabel.grid(row = 7, column = 0, columnspan = 2)
	root.machineBLabel.grid(row = 7, column = 3, columnspan = 2)


	root.weightACanvas.grid(row = 8, column = 0, rowspan = 4, columnspan = 2)
	root.weightBCanvas.grid(row = 8, column = 3, rowspan = 4, columnspan = 2)
	
	'''
	weightAvsb.grid(row = 8, column = 2, rowspan = 4, sticky = "nsw")
	weightAhsb.grid(row = 12, column = 0, columnspan = 2, sticky = "ewn")
	weightBvsb.grid(row = 8, column = 5, rowspan = 4, sticky = "nsw")
	weightBhsb.grid(row = 12, column = 3, columnspan = 2, sticky = "ewn")
	'''

	emptyLabel2.grid(row = 12, columnspan = 5)

	verSeparator.grid(row = 7, column = 2, rowspan = 5, sticky = "NS")

	horSeparator.grid(row = 13, columnspan = 5, sticky = "EW")

def create_result(root):

	root.resLabel = Label(root, text = "Synchronization Results", bg = bgcolor)

	root.totalIterLabel = Label(root, text = "Total iterations ", bg = bgcolor)
	root.maxIterLabel = Label(root, text = "Max iterations ", bg = bgcolor)
	root.keyLengthLabel = Label(root, text = "Key length ", bg = bgcolor)
	root.bytesLabel = Label(root, text = "(bytes)", bg = bgcolor)
	root.keyLabel = Label(root, text = "Key ", bg = bgcolor)

	root.totalIterEntry = Entry(root)
	root.totalIterEntry.insert(END, '')
	root.maxIterEntry = Entry(root)
	root.maxIterEntry.insert(END, '')
	root.keyLengthEntry = Entry(root)
	root.keyLengthEntry.insert(END, '')
	root.keyEntry = Entry(root)
	root.keyEntry.insert(END, '')

	emptyLabel1 = Label(root, text = "", bg = bgcolor)

	horSeparator = Separator(root, orient = "horizontal")

	root.resLabel.grid(row = 14, columnspan = 5)

	root.totalIterLabel.grid(row = 15, column = 0, sticky = "W")
	root.maxIterLabel.grid(row = 15, column = 2, sticky = "W")
	root.keyLengthLabel.grid(row = 16, column = 0, sticky = "W")
	root.bytesLabel.grid(row = 16, column = 2, sticky = "W")
	root.keyLabel.grid(row = 17, column = 0, sticky = "W")

	root.totalIterEntry.config(highlightbackground = bgcolor, state = 'readonly')
	root.maxIterEntry.config(highlightbackground = bgcolor, state = 'readonly')
	root.keyLengthEntry.config(highlightbackground = bgcolor, state = 'readonly')
	root.keyEntry.config(highlightbackground = bgcolor, state = 'readonly')

	root.totalIterEntry.grid(row = 15, column = 1)
	root.maxIterEntry.grid(row = 15, column = 3)
	root.keyLengthEntry.grid(row = 16, column = 1)
	root.keyEntry.grid(row = 17, column = 1, columnspan = 3, sticky = "NEWS")

	emptyLabel1.grid(row = 18, columnspan = 5)

	horSeparator.grid(row = 19, columnspan = 5, sticky = "EW")

def create_message(root):

	root.cryptLabel = Label(root, text = "AES Cryptography", bg = bgcolor)

	root.messageLabel = Label(root, text = "Input Message ", bg = bgcolor)
	root.encryptLabel = Label(root, text = "Encrypted message ", bg = bgcolor)
	root.decryptLabel = Label(root, text = "Decrypted message ", bg = bgcolor)

	root.messageEntry = Entry(root)
	root.messageEntry.insert(END, 'Enter your message here')
	root.encryptEntry = Entry(root)
	root.encryptEntry.insert(END, '')
	root.decryptEntry = Entry(root)
	root.decryptEntry.insert(END, '')

	encryptButton = Button(root, text = "Encrypt", bg = bgcolor, command = handle_encrypt)
	decryptButton = Button(root, text = "Decrypt", bg = bgcolor, command = handle_decrypt)

	emptyLabel1 = Label(root, text = "", bg = bgcolor)

	root.finalLabel = Label(root, text = "", bg = bgcolor)

	horSeparator = Separator(root, orient = "horizontal")

	root.cryptLabel.grid(row = 20, columnspan = 5)

	root.messageLabel.grid(row = 21, column = 0, sticky = "W")
	root.encryptLabel.grid(row = 22, column = 0, sticky = "W")
	root.decryptLabel.grid(row = 23, column = 0, sticky = "W")

	root.messageEntry.config(highlightbackground = bgcolor)
	root.encryptEntry.config(highlightbackground = bgcolor, state = 'readonly')
	root.decryptEntry.config(highlightbackground = bgcolor, state = 'readonly')

	root.messageEntry.grid(row = 21, column = 1, columnspan = 3, sticky = "NEWS")
	root.encryptEntry.grid(row = 22, column = 1, columnspan = 3, sticky = "NEWS")
	root.decryptEntry.grid(row = 23, column = 1, columnspan = 3, sticky = "NEWS")

	encryptButton.config(highlightbackground = bgcolor)
	decryptButton.config(highlightbackground = bgcolor)

	encryptButton.grid(row = 21, column = 4)
	decryptButton.grid(row = 22, column = 4)

	emptyLabel1.grid(row = 24, columnspan = 5)

	root.finalLabel.grid(row = 25, columnspan = 5)

	horSeparator.grid(row = 26, columnspan = 5, sticky = "EW")

def handle_sync():

	root.K = int(root.kEntry.get())
	root.N = int(root.nEntry.get())
	root.L = int(root.lEntry.get())

	MAX_ITERATIONS = 1000
	SEED = 12345

	delay = float(root.delayEntry.get())

	root.maxIter = MAX_ITERATIONS

	root.maxIterEntry.config(state = 'normal')
	root.maxIterEntry.delete(0, END)
	root.maxIterEntry.insert(0, str(root.maxIter))
	root.maxIterEntry.config(state = 'readonly')

	tempA, tempB, tempiter = ex.sync_weights(root, root.K, root.N, root.L, MAX_ITERATIONS, SEED, delay)

	root.weightA = tempA
	root.weightB = tempB

	print(root.weightA)
	print(root.weightB)

	root.totalIter = tempiter

	root.totalIterEntry.config(state = 'normal')
	root.totalIterEntry.delete(0, END)
	root.totalIterEntry.insert(0, str(root.totalIter))
	root.totalIterEntry.config(state = 'readonly')


	root.keyLength = 32

	root.keyA, root.hexkey = generate_key(root.weightA)
	root.keyB, temp = generate_key(root.weightB)

	root.keyLengthEntry.config(state = 'normal')
	root.keyLengthEntry.delete(0, END)
	root.keyLengthEntry.insert(0, str(root.keyLength))
	root.keyLengthEntry.config(state = 'readonly')

	root.keyEntry.config(state = 'normal')
	root.keyEntry.delete(0, END)
	root.keyEntry.insert(0, str(root.hexkey))
	root.keyEntry.config(state = 'readonly')


def generate_key(W):

	stream_W = W.ravel()
	hash = SHA256.new()
	hash.update(stream_W)
	return hash.digest(), hash.hexdigest()

def handle_encrypt():

	root.message = root.messageEntry.get()
	root.message = pad(root.message)

	iv = Random.new().read(AES.block_size)
	mode = AES.MODE_CBC
	
	cipher = AES.new(root.keyA, mode, iv)
	root.cipher_text = iv + cipher.encrypt(root.message)
	root.cipher_text = base64.b64encode(root.cipher_text)

	root.encryptEntry.config(state = 'normal')
	root.encryptEntry.delete(0, END)
	root.encryptEntry.insert(0, root.cipher_text)
	root.encryptEntry.config(state = 'readonly')

	root.finalLabel['text'] = ""


def handle_decrypt():

	root.cipher_text = root.encryptEntry.get()
	root.cipher_text = base64.b64decode(root.cipher_text)
	iv = root.cipher_text[:AES.block_size]
	mode = AES.MODE_CBC
	cipher = AES.new(root.keyB, mode, iv)
	root.plain_text = cipher.decrypt(root.cipher_text[AES.block_size:])
	root.plain_text = unpad(root.plain_text).decode('utf-8')

	root.decryptEntry.config(state = 'normal')
	root.decryptEntry.delete(0, END)
	root.decryptEntry.insert(0, root.plain_text)
	root.decryptEntry.config(state = 'readonly')

	if root.messageEntry.get() == root.plain_text:
		root.finalLabel['text'] = "Communication between Alice and Bob successful!"
	else:
		root.finalLabel['text'] = "Communication between Alice and Bob unsuccessful!"



root = Tk()

root.title("Communication using Neural Cryptography")
root.geometry("800x800")
root.resizable(width = False, height = False)
root.configure(background = bgcolor)

for i in range(5):
	root.grid_columnconfigure(i, weight = 1)

create_param(root)
create_weights(root)
create_result(root)
create_message(root)


root.mainloop()
	