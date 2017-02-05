"""
Shogi Board
"""
from Pieces import *
import copy
import Mechanics

class Board(object):

	def __init__(self):
		self.board = [
			[Lance(2, 0, 0), Knight(2, 1, 0), Silver_General(2, 2, 0), Gold_General(2, 3, 0), King(2, 4, 0), Gold_General(2, 5, 0), Silver_General(2, 6, 0), Knight(2, 7, 0), Lance(2, 8, 0)],
			[None, Rook(2, 1, 1), None, None, None, None, None, Bishop(2, 7, 1), None], 
			[Pawn(2, 0, 2), Pawn(2, 1, 2), Pawn(2, 2, 2), Pawn(2, 3, 2), Pawn(2, 4, 2), Pawn(2, 5, 2), Pawn(2, 6, 2), Pawn(2, 7, 2), Pawn(2, 8, 2)],
			[None] * 9,
			[None] * 9,
			[None] * 9,
			[Pawn(1, 0, 6), Pawn(1, 1, 6), Pawn(1, 2, 6), Pawn(1, 3, 6), Pawn(1, 4, 6), Pawn(1, 5, 6), Pawn(1, 6, 6), Pawn(1, 7, 6), Pawn(1, 8, 6)],
			[None, Bishop(1, 1, 7), None, None, None, None, None, Rook(1, 7, 7), None],
			[Lance(1, 0, 8), Knight(1, 1, 8), Silver_General(1, 2, 8), Gold_General(1, 3, 8), King(1, 4, 8), Gold_General(1, 5, 8), Silver_General(1, 6, 8), Knight(1, 7, 8), Lance(1, 8, 8)]
			]
		self.dim = 9
		self.player_one_holder = list()
		self.player_two_holder = list()
		self.p1_king = {"row":8, "col":4}
		self.p2_king = {"row":0, "col":4}
		self.codes = {0:"A", 1:"B", 2:"C", 3:"D", 4:"E", 5:"F", 6:"G", 7:"H", 8:"I"}
		self.rev_codes = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7, "I": 8}
		# init board with pieces

	def assignment(self, board_obj):
		self.board = board_obj.board
		self.player_one_holder = board_obj.player_one_holder
		self.player_two_holder = board_obj.player_two_holder
		self.p1_king = board_obj.p1_king
		self.p2_king = board_obj.p2_king
	
	def deepcopy(self):
		return copy.deepcopy(self)

	def save_move_info(self, r, c, nr, nc, p1_piece, prev_piece, promote1, promote2, p):
		self.prev_move = [r, c, nr, nc, p1_piece, prev_piece, promote1, promote2, p]

	def undo(self):
		if self.prev_move is None:
			raise Exception
		row, col, nrow, ncol, piece, prev, promote1, promote2, p = self.prev_move
		self.board[row][col] = piece
		# self.board[nrow][ncol] = prev
		self.board[row][col].x = col
		self.board[row][col].y = row
		if promote1 == False and piece.promoted == True and piece.can_promote:
			self.board[row][col].demote()
		if prev is not None:
			if p == 1:
				lst = self.player_one_holder
				opp = 2
			else:
				lst = self.player_two_holder
				opp = 1
			for i in range(len(lst)):
				if lst[i].name == prev_piece.name:
					self.drop(nrow, ncol, opp, i)
			if prev.promoted == False and promote2 == True:
				board_obj.board[ii][jj].promote()

		else:
			self.board[nrow][ncol] = None

		if piece.name == "King":
			if piece.player is 1:
				self.p1_king["row"] = row
				self.p1_king["col"] = col
			else:
				self.p2_king["row"] = row
				self.p2_king["col"] = col
		elif prev is not None and prev.name == "King":
			if prev.player is 1:
				self.p1_king["row"] = row
				self.p1_king["col"] = col
			else:
				self.p2_king["row"] = row
				self.p2_king["col"] = col


		# self.board[row][col].name != "King"
		# Demote is not promoted, return other players piece, etc.



	def move(self, row, col):
		piece = self.board[row][col]
		temp_board = list()
		for row in range(self.dim):
			row_lst = list()
			for col in range(self.dim):
				row_lst.append(self.get_str(self.board[row][col]))
			temp_board.append(row_lst)
		temp_board, openings = piece.highlight(temp_board)
		if openings == 0:
			print "No Moves available for %s at %s%s" % (piece.name, self.codes[piece.y], piece.x)
			return False
		self.display_highlight(temp_board)
		print "%d Move(s) available for %s at %s%s" % (openings, piece.name, self.codes[piece.y], piece.x)
		row, col = self.get_coord()
		if row is None: return False
		if row < 0 or row > 8:
			print "Invalid row: %s" % row
			return False
		if col < 0 or col > 8:
			print "Invalid col: %s" % col
			return False
		did_move = piece.move(col, row, self.board, temp_board, self)
		if piece.name == "King" and did_move:
			if piece.player is 1:
				self.p1_king["row"] = row
				self.p1_king["col"] = col
			else:
				self.p2_king["row"] = row
				self.p2_king["col"] = col
		if piece.player == 1:
			opp = 2
		else:
			opp = 1
		c1 = Mechanics.check(self, opp)
		if c1:
			print "Invalid move: You are still in check! Please move your king to safety!"
			return False
		return did_move

	def get_coord(self):
		sel = str(raw_input("Selection: "))
		try:
			try:
				row = self.rev_codes.get(sel[0].upper(), -1)
				col = int(sel[1])
			except Exception:
				row = self.rev_codes.get(sel[1].upper(), -1)
				col = int(sel[0])
		except Exception:
			print "Invalid selection: %s" % sel
			return None, None
		return row, col

	def display_highlight(self, temp_board):
		output =  "                           Player 2\n"
		output += "   %4d  %4d  %4d  %4d  %4d  %4d  %4d  %4d  %4d" % (0,1,2,3,4,5,6,7,8) 
		output += "       Bucket: %s\n" % self.get_bucket_str(2)
		output += "   -------------------------------------------------------\n" # 14 _
		for row in range(self.dim):
			output += "%2s " % self.codes[row]
			for col in range(self.dim):
				output += "|%4s " % temp_board[row][col]
			output += "|%2s\n   -------------------------------------------------------\n" % self.codes[row] # 14 _
		output  += "   %4d  %4d  %4d  %4d  %4d  %4d  %4d  %4d  %4d" % (0,1,2,3,4,5,6,7,8) 
		output  += "       Bucket: %s\n" % self.get_bucket_str(1) 
		output  += "                           Player 1\n"
		print output

	def display(self):
		output =  "                           Player 2\n"
		output += "   %4d  %4d  %4d  %4d  %4d  %4d  %4d  %4d  %4d" % (0,1,2,3,4,5,6,7,8)
		output += "       Bucket: %s\n" % self.get_bucket_str(2) 
		output += "   -------------------------------------------------------\n" # 14 _
		for row in range(self.dim):
			output += "%2s " % self.codes[row]
			for col in range(self.dim):
				output += "|%4s " % self.get_str(self.board[row][col])
			output += "|%2s\n   -------------------------------------------------------\n" % self.codes[row] # 14 _
		output  += "   %4d  %4d  %4d  %4d  %4d  %4d  %4d  %4d  %4d" % (0,1,2,3,4,5,6,7,8)
		output  += "       Bucket: %s\n" % self.get_bucket_str(1) 
		output  += "                           Player 1\n"
		print output

	def drop(self, row, col, p, index):
		if p == 1:
			piece = self.player_one_holder[index]
		else: 
			piece = self.player_two_holder[index]
		piece.y = row
		piece.x = col
		piece.player = p
		self.board[row][col] = piece
		if p == 1:
			del self.player_one_holder[index]
		else:
			del self.player_two_holder[index]

	def get_bucket_str(self, ply):
		if ply is 1:
			list_str = ""
			max_len = len(self.player_one_holder)
			if max_len == 0:
				return "Empty"
			elif max_len == 1:
				return str(self.player_one_holder[0])
			for i in range(max_len):
				if i != max_len - 1:
					list_str += "%s, " % str(self.player_one_holder[i])
				else:
					list_str += "%s" % str(self.player_one_holder[i])
			return list_str
		list_str = ""
		max_len = len(self.player_two_holder)
		if max_len == 0:
			return "Empty"
		elif max_len == 1:
			return str(self.player_two_holder[0])
		for i in range(max_len):
			if i != max_len - 1:
				list_str += "%s, " % str(self.player_two_holder[i])
			else:
				list_str += "%s" % str(self.player_two_holder[i])
		return list_str

	def get_str(self, item):
		if item is not None:
			if item.player is 1:
				return str(item) + "^"
			return str(item) + "!"			
		return ""
