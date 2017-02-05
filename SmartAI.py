import Board
import Mechanics
import numpy as np
import RandomAI
import pickle
import random
import time

pieces = [("Pawn", 1), ("Bishop", 1), ("Rook", 1), ("Lance", 1), ("Knight", 1), ("Silver General", 1), ("Gold General", 1), ("King", 1),
		  ("Pawn", 2), ("Bishop", 2), ("Rook", 2), ("Lance", 2), ("Knight", 2), ("Silver General", 2), ("Gold General", 2), ("King", 2)]

piece_val = {"Pawn" : 1, "Lance" : 5, "Knight" : 10, "Silver General" : 20, "Gold General" : 25, "Bishop" : 30, "Rook" : 30, "King" : 50}

class SmartAI(object):

	def __init__(self, p, filename = None, learning = 0.7):
		if filename is None:
			self.model = dict()
		else:
			self.model = load(filename)
		self.prev_moves = list()
		self.player = p
		self.learning = learning
		self.reward = {"win": 100, "loss": -100}
		self.prev_key = None
		self.thr = 0.2

	def save_model(self, filename):
		save(self.model, filename)

	def load_model(self, filename):
		self.model = load(filename)

	def reset(self):
		self.prev_moves = list()
		self.prev_key = None

	def get_board_encoding(self, board):
		return encode_board(board, self.player)

	def update_key(self, board):

		new_key = self.get_board_encoding(board)
		self.model[self.prev_key][1].append(new_key)
		# if len(self.model[self.prev_key][1]) != len(np.atleast_1d(self.model[self.prev_key][0])):
		self.model[self.prev_key][0].append(0)

	def predict_move(self, board):
		bp1 = len(board.player_one_holder)
		bp2 = len(board.player_two_holder)
		key = self.get_board_encoding(board)
		self.prev_key = key
		values = self.model.get(key, -1)
		self.prev_moves.append(key)
		rand = random.uniform(0, 1)
		# print rand
		if values == -1:
			self.model[key] = [list(), list()]
			RandomAI.ai_turn(board, self.player, True)
			if self.player == 1:
				if bp1 < len(board.player_one_holder):
					self.back_prop(rew = piece_val[board.player_one_holder[-1].identifier])
			if self.player == 2:
				if bp1 < len(board.player_two_holder):
					self.back_prop(rew = piece_val[board.player_two_holder[-1].identifier])
			return 1
		elif rand < self.thr:
			RandomAI.ai_turn(board, self.player, True)
			if self.player == 1:
				if bp1 < len(board.player_one_holder):
					self.back_prop(rew = piece_val[board.player_one_holder[-1].identifier])
			if self.player == 2:
				if bp1 < len(board.player_two_holder):
					self.back_prop(rew = piece_val[board.player_two_holder[-1].identifier])
			return 1
			# self.model[key][1].append(self.get_board_encoding(board))
		else:
			index = np.argmax(np.array(self.model[key][0]))
			# print self.model[key][0]
			# print self.model[key][1]
			pick = 0
			new_key = self.model[key][1][index]
			mo = key ^ new_key
			move = "{0:01296b}".format(mo)
			prev = "{0:01296b}".format(key & mo)
			new = "{0:01296b}".format(mo & new_key)
			ind = get_one_index(move, self.player)
			p = get_one_index(prev, self.player)
			n = get_one_index(new, self.player)
			# print ind, p[pick], n[pick]
			print "ORG ", organize(ind)
			# int("S")
			# if len(ind) > 1  and len(ind) % 2 == 0 or len(n) == 0:
			print ind, p, n
			if len(p) == 0 or len(n) == 0:
				RandomAI.ai_turn(board, self.player, True)
				if self.player == 1:
					if bp1 < len(board.player_one_holder):
						self.back_prop(rew = piece_val[board.player_one_holder[-1].identifier])
				if self.player == 2:
					if bp1 < len(board.player_two_holder):
						self.back_prop(rew = piece_val[board.player_two_holder[-1].identifier])
				return -1
			r_old, c_old = get_row_col(p[pick])
			r_new, c_new = get_row_col(n[pick])
			tmp_board = RandomAI.make_tmp_board(board)
			tmp_board, openings = board.board[r_old][c_old].highlight(tmp_board)
			moved = board.board[r_old][c_old].move(c_new, r_new, board.board, tmp_board, board, True)
			if moved == False:
				RandomAI.ai_turn(board, self.player, True)
				# return -1
			# elif len(ind) % 2 == 1:
				# ind = organize(ind)
				# print ind, n
				# if len(n) == 0 and len(p) != 0:
				# n = get_one_index(organize(n), self.player)
				# else:
				# print "DROP PIECE"
				# print ind
				# print p
				# print n 
				# print n[pick]
				# print n[pick] / 81
				# piece = pieces[n[pick] / 81]
				# if self.player is 1:
					# holder = board.player_one_holder
				# else:
					# holder = board.player_two_holder
				# for i in range(len(holder)):
					# if holder[i].name == piece:
						# break
				# r_new, c_new = get_row_col(n[0])
				# board.drop(r_new, c_new, self.player, i)
		if self.player == 1:
			if bp1 < len(board.player_one_holder):
				self.back_prop(rew = piece_val[board.player_one_holder[-1].identifier])
		if self.player == 2:
			if bp1 < len(board.player_two_holder):
				self.back_prop(rew = piece_val[board.player_two_holder[-1].identifier])
		return 0

	def back_prop(self, winner = -1, rew = -1):
		adjust = 0
		if winner == -1:
			if rew != -1:
				adjust = rew
		elif self.player == winner:
			adjust = self.reward["win"]
		else:
			adjust = self.reward["loss"]
		del self.prev_moves[-1]
		length = len(self.prev_moves)
		# print length
		for i in range(length):
			# print i
			key = self.prev_moves[i]
			if i != length - 1:
				next_key = self.prev_moves[i+1]
			else:
				break
			if i != length - 1:
				next_key = self.prev_moves[i+1]
				try:
					index_next_key = self.model[key][1].index(next_key)
				except Exception:

					print "SORRY"

					
				# print "H"
				# print len(np.atleast_1d(self.model[key][0]))
				# print index_next_key
				# print len(self.model[key][1])
				# print self.model[key][0]
				# print self.model[key][1]
				# f self.model[key][0].shape >= len(np.atleast_1d(self.model[key][0])):
					# self.model[key][0] = np.append(self.model[key][0], 0)
				# print index_next_key
				# print i, length, self.model[next_key][0]
				# print self.model[key][0][index_next_key] 
				# print self.learning 
				# print adjust
				# print (1/float(length))
				# print np.max(np.array(self.model[next_key][0])) 
				# print self.model[key][0][index_next_key]
				# time.sleep(0.5)
				# if adjust != 100 or adjust != -100:
					# print "upd"
					# time.sleep(2)
				value = self.model[key][0][index_next_key] + self.learning * (adjust + (1/float(length)) * np.max(np.array(self.model[next_key][0])) - self.model[key][0][index_next_key])
				
				# print value
				# print len(self.model[key][1])
				# print index_next_key, np.atleast_1d(self.model[key][0])
				self.model[key][0][index_next_key] = value
				print "VAL:", self.model[key][0][index_next_key]

def encode_board(board_obj, p):
	vector = np.zeros((16, 9, 9))
	encoding = ""
	for i in range(16): # for each piece/player combo
		for j in range(9): # for each row
			for k in range(9): # for each col
				piece = board_obj.board[j][k]
				if piece is not None and piece.identifier == pieces[i][0] and piece.player == pieces[i][1]:
					vector[i][j][k] = 1
					encoding += "1"
				else:
					encoding += "0"

	# for i in range(8):
	return int(encoding, 2)		

def save(obj, filename):
	try:
		with open(filename, 'wb') as writer:
			pickle.dump(obj, writer)
	except IOError:
		raise Exception("Exception while writing to the file %s." % filename)        
	except pickle.PickleError:
		raise Exception("Exception while dumping pickle.")

def load(filename):
	obj = None
	try:
		with open(filename, 'rb') as reader:
			obj = pickle.load(reader)
	except IOError:
		raise Exception("Exception while reading the file %s." % filename)
	except pickle.PickleError:
		raise Exception("Exception while loading pickle.")
	return obj

def get_one_index(string, p):
	pick = 0
	lower = 648
	# print p
	if p == 2:
		# print 
		pick = 647
		lower = 1298
	# print pick
	lst = [i for i, ltr in enumerate(string) if (ltr == "1" and i >= pick and i <= lower)]
	return lst

def organize(lst):
	diffs = list()
	for i in range(len(lst)):
		if i != len(lst) - 1:
			diffs.append(abs(int(lst[i]) - int(lst[i+1])))
	lows = list()
	lowest = 1297
	lowest_ind = -1
	second_lowest = 1297
	sec_ind = -1
	for i in range(len(diffs)):
		if lowest_ind == -1:
			lowest = diffs[i]
			lowest_ind = i
			continue
		elif sec_ind == -1:
			second_lowest = diffs[i]
			sec_ind = i
			continue
		elif diffs[i] < lowest:
			tmp = lowest
			tmp_ind = lowest_ind
			lowest = diffs[i]
			lowest_ind = i
			if tmp < second_lowest:
				second_lowest = tmp
				sec_ind = tmp_ind
			continue
		elif diffs[i] > lowest and diffs[i] < second_lowest:
			second_lowest = diffs[i]
			sec_ind = i
			continue
	lows = [lst[lowest_ind], lst[lowest_ind+1], lst[sec_ind], lst[sec_ind+1]]
	return lows


def get_row_col(index):
	return (index - (index / 81) * 81) / 9, index % 9
					