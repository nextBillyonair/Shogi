import numpy as np 
import scipy
import dill as pickle
import Board
import RandomAI
import Mechanics
import random
import json
from keras.models import model_from_json
from keras import initializations
from keras.initializations import normal, identity
from collections import deque
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD , Adam


REPLAY_MEMORY = 50000 # number of previous transitions to remember
BATCH = 32 # size of minibatch
OBSERVE = 3200


pieces = [("Pawn", 1), ("Bishop", 1), ("Rook", 1), ("Lance", 1), ("Knight", 1), ("Silver General", 1), ("Gold General", 1), ("King", 1),
		  ("Pawn", 2), ("Bishop", 2), ("Rook", 2), ("Lance", 2), ("Knight", 2), ("Silver General", 2), ("Gold General", 2), ("King", 2)]

rewards = {"P": 1, "+P": 10, "L":4, "+L": 9, "N":5, "+N":9, "S":7, "+S":8, "G":8, "B":11, "+B":14, "R":13, "+R":16, "K":1000, "CHECK":-5}

class NeuralNet(object):

	def __init__(self, p=1, load=False, t=0.3):
		self.player = p
		self.thresh = t
		self.prev_moves = list()
		self.__create_model(load)
	
	def __create_model(self, load):		

		self.model = Sequential()
		self.model.add(Convolution2D(32, 8, 8, subsample=(4,4),init=lambda shape, name: normal(shape, scale=0.01, name=name), border_mode='same',input_shape=(32,9,9)))
		self.model.add(Activation('relu'))
		self.model.add(Convolution2D(64, 4, 4, subsample=(2,2),init=lambda shape, name: normal(shape, scale=0.01, name=name), border_mode='same'))
		self.model.add(Activation('relu'))
		self.model.add(Convolution2D(64, 3, 3, subsample=(1,1),init=lambda shape, name: normal(shape, scale=0.01, name=name), border_mode='same'))
		self.model.add(Activation('relu'))
		self.model.add(Flatten())
		self.model.add(Dense(512, init=lambda shape, name: normal(shape, scale=0.01, name=name)))
		self.model.add(Activation('relu'))
		self.model.add(Dense(1,init=lambda shape, name: normal(shape, scale=0.01, name=name)))

		adam = Adam(lr=1e-6)
		self.model.compile(loss='mse',optimizer=adam)
		if load:
			self.load_model()
			
	def load_model(self):
		self.model = load("model.file")
		# self.model.load_weights("model.h5")
		# adam = Adam(lr=1e-6)
		# self.model.compile(loss='mse',optimizer=adam)

	def move(self, board_obj, not_show = True):
		# current state
		p1len = len(board_obj.player_one_holder) 
		p2len = len(board_obj.player_two_holder)
		rand = random.uniform(0, 1)
		# print rand
		self.thresh = 0
		if rand < self.thresh:
			RandomAI.ai_turn(board_obj, self.player, not_show)
			prev_piece = None
			if p1len < len(board_obj.player_one_holder):
				prev_piece = board_obj.player_one_holder[p1len]
			if p2len < len(board_obj.player_two_holder):
				prev_piece = board_obj.player_two_holder[p2len]
			rew = assign_reward(board_obj, self.player, prev_piece)
			terminal = Mechanics.checkmate(board_obj)				
			return board_obj, rew, terminal

		# TODO Starting for here
		future_states = list()
		boards = list()
		for i in range(9):
			for j in range(9):
				if board_obj.board[i][j] is not None:
					piece = board_obj.board[i][j]
					temp_board = RandomAI.make_tmp_board(board_obj)
					temp_board, opening = piece.highlight(temp_board)
					self.inner_loop(board_obj, temp_board, opening, future_states, i, j, boards)
					
		max_index = -1
		max_val = 0

		val = self.model.predict(np.array(boards))

		if self.player == 1:
			max_val = np.max(val)
			max_index = np.argmax(val)
		else:
			max_val = np.min(val)
			max_index = np.argmin(val)
		# TODO ending here, make function called predict_move(board, player_num) 
		# Returns future_state, max_val

		b, i, j, ii, jj = future_states[max_index]
		temp_board = RandomAI.make_tmp_board(board_obj)
		temp_board, opening = board_obj.board[i][j].highlight(temp_board)
		prev_piece = board_obj.board[i][j]
		board_obj.board[i][j].move(jj, ii, board_obj.board, temp_board, board_obj, nn=True)
		rew = assign_reward(board_obj, self.player, prev_piece)
		terminal = Mechanics.checkmate(board_obj)

		return board_obj, rew, terminal

	def inner_loop(self, board_obj, temp_board, opening, future_states, i, j, boards):
		count = 0
		for ii in range(9):
			for jj in range(9):
				if count == opening:
					return
				if 'X' in temp_board[ii][jj]:
					if board_obj.board[ii][jj] is None:
						board_obj.save_move_info(i, j, ii, jj, board_obj.board[i][j], board_obj.board[ii][jj], board_obj.board[i][j].promoted, None, board_obj.board[i][j].player)
					else:
						board_obj.save_move_info(i, j, ii, jj, board_obj.board[i][j], board_obj.board[ii][jj], board_obj.board[i][j].promoted, board_obj.board[ii][jj].promoted, board_obj.board[i][j].player)

					board_obj.board[i][j].move(jj, ii, board_obj.board, temp_board, board_obj, nn=True)
					b = encode_board(board_obj)
					future_states.append([b,i,j,ii,jj])
					boards.append(b)
					count += 1
					# print board_obj.display()
					board_obj.undo()
					# print board_obj.display()
					# raise Exception
		
		return

	def train(self):
		D = deque()
		t = 0
		b = Board.Board()
		self.player = 1
		while True:

			b_prev = encode_board(b)
			b, reward, terminal = self.move(b)
			b_next = encode_board(b)

			D.append((b_prev, b_next, reward, terminal))

			if len(D) > REPLAY_MEMORY:
				D.popleft()

			if t > OBSERVE:
				minibatch = random.sample(D, BATCH)

				inputs = np.zeros((BATCH, b_prev.shape[0], b_prev.shape[1], b_prev.shape[2]))
				targets = np.zeros((BATCH, 1))

				for i in range(len(minibatch)):
					state_t0 = minibatch[i][0]
					state_t1 = minibatch[i][1]
					reward_t = minibatch[i][2]
					terminal = minibatch[i][3]

					inputs[i] = state_t0

					targets[i] = self.model.predict(np.array([state_t0]))
					Q_sa = self.model.predict(np.array([state_t1]))

					if terminal:
						targets[i] = reward_t
					else:
						targets[i] = np.max(targets[i], reward_t - GAMMA * Q_sa[0])

			
			# SAVE WEIGHS EVERY X ITERATIONS, YOU DECIDE X
			if t % 100 == 0:
				save(self.model, "model.file") #.save_weights("model.h5", overwrite=True)
				with open("model.json", "w") as outfile:
					json.dump(self.model.to_json(), outfile)
			
			t += 1
			if self.player == 1:
				self.player = 2
			else:
				self.player = 1
			if t > OBSERVE:
				print "TIME ", t, "\nReward ", reward_t, "\nQ_Max ", np.max(Q_sa)







		

def assign_reward(board_obj, player, prev_piece):
	if player == 1:
		sign = 1
	else:
		sign = -1
	num = 0
	if prev_piece is not None:
		code = prev_piece.condensed_string
		num = rewards[code]
	c1 = Mechanics.check(board_obj, player)
	if c1:
		num += rewards["CHECK"]
	return num * sign







def encode_board(board_obj):
	vector = np.zeros((32, 9,9))
	for i in range(16): # for each piece/player combo
		index = 2 * i
		for j in range(9): # for each row
			for k in range(9): # for each col
				temp_board = RandomAI.make_tmp_board(board_obj)
				
				piece = board_obj.board[j][k]
				if piece is not None and piece.identifier == pieces[i][0] and piece.player == pieces[i][1]:
					vector[index][j][k] = 1
					temp_board, opening = piece.highlight(temp_board)
				for jj in range(9):
					for kk in range(9):
						if 'X' in temp_board[jj][kk]:
							vector[index+1][jj][kk] += 1
		# print temp_board

	return vector

def save(obj, filename):
	"""
	Saves an object (obj) to filename via pickle.dump
	Throws IOError if cannot write to filename.
	Throws PickleError is pickle cannot dump obj.
	"""
	try:
		with open(filename, 'wb') as writer:
			pickle.dump(obj, writer)
	except IOError:
		raise Exception("Exception while writing to the file %s." % filename)        
	except pickle.PickleError:
		raise Exception("Exception while dumping pickle.")

def load(filename):
	"""
	Loads an item from filename.
	Returns the object that was saved in filename.
	Throws IOError if File DNE.
	Throws PickleError is file cannot be opened via pickle.
	"""
	obj = None
	try:
		with open(filename, 'rb') as reader:
			obj = pickle.load(reader)
	except IOError:
		raise Exception("Exception while reading the file %s." % filename)
	except pickle.PickleError:
		raise Exception("Exception while loading pickle.")
	return obj
	

