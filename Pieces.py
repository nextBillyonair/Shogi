"""
Shogi Pieces
"""
import random

class Piece(object):

	def __init__(self, player, x, y, promoted=False, cp = True):
		self.x = x
		self.y = y
		self.player = player
		self.promoted = promoted
		self.can_promote = cp
		self.identifier = "Generic Piece"
		self.codes = {0:"A", 1:"B", 2:"C", 3:"D", 4:"E", 5:"F", 6:"G", 7:"H", 8:"I"}
		self.rev_codes = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7, "I": 8}

	def move(self, x, y, board, tmp_board, board_obj, ai=False, nn=False):
		if "X" not in tmp_board[y][x]:
			print "Invalid Move: %s at %s%s cannot move to %s%s" % (self.name, self.codes[self.y], self.x, self.codes[y], x)
			return False
		print "Player %d moved %s at %s%s to %s%s" % (self.player, self.name, self.codes[self.y], self.x, self.codes[y], x)
		# add stuff to handle capture
		if self.player is 1:
			if board[y][x] is not None and "!" in tmp_board[y][x]:
				board[y][x].y = -1
				board[y][x].x = -1
				board[y][x].player = 1
				if board[y][x].name == "King":
					board_obj.p2_king["row"] = -1
					board_obj.p2_king["col"] = -1
				if board[y][x].can_promote and board[y][x].promoted:
					board[y][x].demote()
				board_obj.player_one_holder.append(board[y][x])
				print "Player %d captured %s" % (self.player, board[y][x].name)
		else:
			if board[y][x] is not None and "^" in tmp_board[y][x]:
				board[y][x].y = -1
				board[y][x].x = -1
				board[y][x].player = 2
				if board[y][x].name == "King":
					board_obj.p1_king["row"] = -1
					board_obj.p1_king["col"] = -1
				if board[y][x].can_promote and board[y][x].promoted:
					board[y][x].demote()
				board_obj.player_two_holder.append(board[y][x])
				print "Player %d captured %s" % (self.player, board[y][x].name)
		board[y][x] = board[self.y][self.x]
		board[self.y][self.x] = None
		board[y][x].x = x
		board[y][x].y = y
		if self.can_promote and not self.promoted and self.in_promo_zone(x, y):
			if ai is False and nn is False:
				choice = str(raw_input("Available to Promote. Would you like too? (y/n) "))
			elif ai is True and nn is False:
				lst = ["y", "n"]
				choice = lst[random.randint(0, 1)]
			elif nn is True:
				choice = "y"
			else:
				choice = "n"
			if choice.lower() == "y":
				self.promote()
				board[y][x] = self
		return True

	def in_promo_zone(self, x, y):
		if self.player is 1:
			if y < 3 or self.y < 3:
				return True
			return False
		if y > 5 or self.y > 5:
			return True
		return False

	def highlight_standard_promoted(self, board):
		# most common move set for piece
		row = self.y
		col = self.x
		if self.player is 1:
			lookout = "!"
		else:
			lookout = "^"
		openings = 0

		if self.player is 1:
			if row != 0:
				if board[row - 1][col] is '':
					board[row - 1][col] = "X"
					openings += 1
				elif lookout in board[row - 1][col]:
					board[row - 1][col] += "X"
					openings += 1

				if col != 0:
					if board[row - 1][col - 1] is '':
						board[row - 1][col - 1] = "X"
						openings += 1
					elif lookout in board[row - 1][col - 1]:
						board[row - 1][col - 1] += "X"
						openings += 1

				if col != 8:
					if board[row - 1][col + 1] is '':
						board[row - 1][col + 1] = "X"
						openings += 1
					elif lookout in board[row - 1][col + 1]:
						board[row - 1][col + 1] += "X"
						openings += 1

			if col != 0:
				if board[row][col - 1] is '':
					board[row][col - 1] = "X"
					openings += 1
				elif lookout in board[row][col - 1]:
					board[row][col - 1] += "X"
					openings += 1
			if col != 8:
				if board[row][col + 1] is '':
					board[row][col + 1] = "X"
					openings += 1
				elif lookout in board[row][col + 1]:
					board[row][col + 1] += "X"
					openings += 1
			if row != 8:
				if board[row + 1][col] is '':
					board[row + 1][col] = "X"
					openings += 1
				elif lookout in board[row + 1][col]:
					board[row + 1][col] += "X"
					openings += 1
		else: # player 2
			if row != 8:
				if board[row + 1][col] is '':
					board[row + 1][col] = "X"
					openings += 1
				elif lookout in board[row + 1][col]:
					board[row + 1][col] += "X"
					openings += 1

				if col != 0:
					if board[row + 1][col - 1] is '':
						board[row + 1][col - 1] = "X"
						openings += 1
					elif lookout in board[row + 1][col - 1]:
						board[row + 1][col - 1] += "X"
						openings += 1

				if col != 8:
					if board[row + 1][col + 1] is '':
						board[row + 1][col + 1] = "X"
						openings += 1
					elif lookout in board[row + 1][col + 1]:
						board[row + 1][col + 1] += "X"
						openings += 1

			if col != 0:
				if board[row][col - 1] is '':
					board[row][col - 1] = "X"
					openings += 1
				elif lookout in board[row][col - 1]:
					board[row][col - 1] += "X"
					openings += 1
			if col != 8:
				if board[row][col + 1] is '':
					board[row][col + 1] = "X"
					openings += 1
				elif lookout in board[row][col + 1]:
					board[row][col + 1] += "X"
					openings += 1
			if row != 0:
				if board[row - 1][col] is '':
					board[row - 1][col] = "X"
					openings += 1
				elif lookout in board[row - 1][col]:
					board[row - 1][col] += "X"
					openings += 1

		return board, openings
		


class King(Piece):

	def __init__(self, player, x, y, promoted=False):
		super(King, self).__init__(player, x, y, promoted, False)
		self.name = "King"
		self.condensed_string = "K"
		self.identifier = "King"

	def highlight(self, board):
		row = self.y
		col = self.x
		if self.player is 1:
			lookout = "!"
		else:
			lookout = "^"
		openings = 0
		if row != 0 and board[row - 1][col] is '':
			board[row - 1][col] = "X"
			openings += 1
		elif row != 0 and lookout in board[row - 1][col]:
			board[row - 1][col] += "X"
			openings += 1
		
		if row != 8 and board[row + 1][col] is '':
			board[row + 1][col] = "X"
			openings += 1
		elif row != 8 and lookout in board[row + 1][col]:
			board[row + 1][col] += "X"
			openings += 1
		
		if row != 0 and col != 0 and board[row - 1][col - 1] is '':
			board[row - 1][col - 1] = "X"
			openings += 1
		elif row != 0 and col != 0 and lookout in board[row - 1][col - 1]:
			board[row - 1][col - 1] += "X"
			openings += 1
		
		if row != 0 and col != 8 and board[row - 1][col + 1] is '':
			board[row - 1][col + 1] = "X"
			openings += 1
		elif row != 0 and col != 8 and lookout in board[row - 1][col + 1]:
			board[row - 1][col + 1] += "X"
			openings += 1
		
		if col != 0 and board[row][col - 1] is '':
			board[row][col - 1] = "X"
			openings += 1
		elif col != 0 and lookout in board[row][col - 1]:
			board[row][col - 1] += "X"
			openings += 1
		
		if col != 8 and board[row][col + 1] is '':
			board[row][col + 1] = "X"
			openings += 1
		elif col != 8 and lookout in board[row][col + 1]:
			board[row][col + 1] += "X"
			openings += 1
		
		if col != 0 and row != 8 and board[row + 1][col - 1] is '':
			board[row + 1][col - 1] = "X"
			openings += 1
		elif col != 0 and row != 8 and lookout in board[row + 1][col - 1]:
			board[row + 1][col - 1] += "X"
			openings += 1
		
		if col != 8 and row != 8 and board[row + 1][col + 1] is '':
			board[row + 1][col + 1] = "X"
			openings += 1
		elif col != 8 and row != 8 and lookout in board[row + 1][col + 1]:
			board[row + 1][col + 1] += "X"
			openings += 1

		return board, openings

	def __str__(self):
		return self.condensed_string


class Rook(Piece):

	def __init__(self, player, x, y, promoted=False):
		super(Rook, self).__init__(player, x, y, promoted)
		if promoted is True:
			self.name = "Promoted Rook"
			self.condensed_string = "+R"
		else:
			self.name = "Rook"
			self.condensed_string = "R"
		self.identifier = "Rook"

	def highlight(self, board):	
		row = self.y
		col = self.x
		if self.player is 1:
			lookout = "!"
			own = "^"
		else:
			lookout = "^"
			own = "!"
		openings = 0

		if self.promoted:
			if row != 0 and col != 0 and board[row - 1][col - 1] is '':
				board[row - 1][col - 1] = "X"
				openings += 1
			elif row != 0 and col != 0 and lookout in board[row - 1][col - 1]:
				board[row - 1][col - 1] += "X"
				openings += 1
			if row != 0 and col != 8 and board[row - 1][col + 1] is '':
				board[row - 1][col + 1] = "X"
				openings += 1
			elif row != 0 and col != 8 and lookout in board[row - 1][col + 1]:
				board[row - 1][col + 1] += "X"
				openings += 1
			if row != 8 and col != 0 and board[row + 1][col - 1] is '':
				board[row + 1][col - 1] = "X"
				openings += 1
			elif row != 8 and col != 0 and lookout in board[row + 1][col - 1]:
				board[row + 1][col - 1] += "X"
				openings += 1
			if row != 8 and col != 8 and board[row + 1][col + 1] is '':
				board[row + 1][col + 1] = "X"
				openings += 1
			elif row != 8 and col != 8 and lookout in board[row + 1][col + 1]:
				board[row + 1][col + 1] += "X"
				openings += 1

		# orientation does not matter
		flag_up, flag_down, flag_left, flag_right = True, True, True, True
		for i in range(1, 9):
			if row + i < 9:
				if flag_down:
					if board[row + i][col] is '':
						board[row + i][col] = "X"
						openings += 1
					elif lookout in board[row + i][col]:
						board[row + i][col] += "X"
						openings += 1
						flag_down = False
					elif own in board[row + i][col]:
						flag_down = False
			if row - i >= 0:
				if flag_up:
					if board[row - i][col] is '':
						board[row - i][col] = "X"
						openings += 1
					elif lookout in board[row - i][col]:
						board[row - i][col] += "X"
						openings += 1
						flag_up = False
					elif own in board[row - i][col]:
						flag_up = False
			if col - i >= 0:
				if flag_left:
					if board[row][col - i] is '':
						board[row][col - i] = "X"
						openings += 1
					elif lookout in board[row][col - i]:
						board[row][col - i] += "X"
						openings += 1
						flag_left = False
					elif own in board[row][col - i]:
						flag_left = False
			if col + i < 9:
				if flag_right:
					if board[row][col + i] is '':
						board[row][col + i] = "X"
						openings += 1
					elif lookout in board[row][col + i]:
						board[row][col + i] += "X"
						openings += 1
						flag_right = False
					elif own in board[row][col + i]:
						flag_right = False
		return board, openings
	
	def promote(self):
		self.promoted = True
		self.name = "Promoted Rook"
		self.condensed_string = "+R"

	def demote(self):
		self.promoted = False
		self.name = "Rook"
		self.condensed_string = "R"

	def __str__(self):
		return self.condensed_string


class Bishop(Piece):

	def __init__(self, player, x, y, promoted=False):
		super(Bishop, self).__init__(player, x, y, promoted)
		if promoted is True:
			self.name = "Promoted Bishop"
			self.condensed_string = "+B"
		else:
			self.name = "Bishop"
			self.condensed_string = "B"
		self.identifier = "Bishop"

	def highlight(self, board):
		row = self.y
		col = self.x
		if self.player is 1:
			lookout = "!"
			own = "^"
		else:
			lookout = "^"
			own = "!"
		openings = 0

		if self.promoted:
			if row != 0 and board[row - 1][col] is '':
				board[row - 1][col] = "X"
				openings += 1
			elif row != 0 and lookout in board[row - 1][col]:
				board[row - 1][col] += "X"
				openings += 1
			if row != 8 and board[row + 1][col] is '':
				board[row + 1][col] = "X"
				openings += 1
			elif row != 8 and lookout in board[row + 1][col]:
				board[row + 1][col] += "X"
				openings += 1
			
			if col != 0 and board[row][col - 1] is '':
				board[row][col - 1] = "X"
				openings += 1
			elif col != 0 and lookout in board[row][col - 1]:
				board[row][col - 1] += "X"
				openings += 1
			if col != 8 and board[row][col + 1] is '':
				board[row][col + 1] = "X"
				openings += 1
			elif col != 8 and lookout in board[row][col + 1]:
				board[row][col + 1] += "X"
				openings += 1

		#orientation does not matter, max move is 8
		flag_ur, flag_dr, flag_ul, flag_dl = True, True, True, True
		for i in range(1, 9):
			if row + i < 9 and col + i < 9:
				if flag_dr:
					if board[row + i][col + i] is '':
						board[row + i][col + i] = "X"
						openings += 1
					elif lookout in board[row + i][col + i]:
						board[row + i][col + i] += "X"
						openings += 1
						flag_dr = False
					elif own in board[row + i][col + i]:
						flag_dr = False
			if row - i >= 0 and col - i >= 0:
				if flag_ul:
					if board[row - i][col - i] is '':
						board[row - i][col - i] = "X"
						openings += 1
					elif lookout in board[row - i][col - i]:
						board[row - i][col - i] += "X"
						openings += 1
						flag_ul = False
					elif own in board[row - i][col - i]:
						flag_ul = False
			if row + i < 9 and col - i >= 0:
				if flag_dl:
					if board[row + i][col - i] is '':
						board[row + i][col - i] = "X"
						openings += 1
					elif lookout in board[row + i][col - i]:
						board[row + i][col - i] += "X"
						openings += 1
						flag_dl = False
					elif own in board[row + i][col - i]:
						flag_dl = False
			if row - i >= 0 and col + i < 9:
				if flag_ur:
					if board[row - i][col + i] is '':
						board[row - i][col + i] = "X"
						openings += 1
					elif lookout in board[row - i][col + i]:
						board[row - i][col + i] += "X"
						openings += 1
						flag_ur = False
					elif own in board[row - i][col + i]:
						flag_ur = False
		return board, openings
	
	def promote(self):
		self.promoted = True
		self.name = "Promoted Bishop"
		self.condensed_string = "+B"

	def demote(self):
		self.promoted = False
		self.name = "Bishop"
		self.condensed_string = "B"

	def __str__(self):
		return self.condensed_string


class Gold_General(Piece):

	def __init__(self, player, x, y, promoted=False):
		super(Gold_General, self).__init__(player, x, y, promoted, False)
		self.name = "Gold General"
		self.condensed_string = "G"
		self.identifier = "Gold General"

	def highlight(self, board):
		return self.highlight_standard_promoted(board)

	def __str__(self):
		return self.condensed_string


class Silver_General(Piece):

	def __init__(self, player, x, y, promoted=False):
		super(Silver_General, self).__init__(player, x, y, promoted)
		if promoted is True:
			self.name = "Promoted Silver General"
			self.condensed_string = "+S"
		else:
			self.name = "Silver General"
			self.condensed_string = "S"
		self.identifier = "Silver General"

	def highlight(self, board):
		if self.promoted:
			board, openings = self.highlight_standard_promoted(board)
			return board, openings
		row = self.y
		col = self.x
		if self.player is 1:
			lookout = "!"
		else:
			lookout = "^"
		openings = 0

		if self.player is 1:
			if row != 0:
				if board[row - 1][col] is '':
					board[row - 1][col] = "X"
					openings += 1
				elif lookout in board[row - 1][col]:
					board[row - 1][col] += "X"
					openings += 1

				if col != 0:
					if board[row - 1][col - 1] is '':
						board[row - 1][col - 1] = "X"
						openings += 1
					elif lookout in board[row - 1][col - 1]:
						board[row - 1][col - 1] += "X"
						openings += 1

				if col != 8:
					if board[row - 1][col + 1] is '':
						board[row - 1][col + 1] = "X"
						openings += 1
					elif lookout in board[row - 1][col + 1]:
						board[row - 1][col + 1] += "X"
						openings += 1
			if row != 8:
				if col != 0:
					if board[row + 1][col - 1] is '':
						board[row + 1][col - 1] = "X"
						openings += 1
					elif lookout in board[row + 1][col - 1]:
						board[row + 1][col - 1] += "X"
						openings += 1
				if col != 8:
					if board[row + 1][col + 1] is '':
						board[row + 1][col + 1] = "X"
						openings += 1
					elif lookout in board[row + 1][col + 1]:
						board[row + 1][col + 1] += "X"
						openings += 1
		else:
			if row != 8:
				if board[row + 1][col] is '':
					board[row + 1][col] = "X"
					openings += 1
				elif lookout in board[row + 1][col]:
					board[row + 1][col] += "X"
					openings += 1

				if col != 0:
					if board[row + 1][col - 1] is '':
						board[row + 1][col - 1] = "X"
						openings += 1
					elif lookout in board[row + 1][col - 1]:
						board[row + 1][col - 1] += "X"
						openings += 1

				if col != 8:
					if board[row + 1][col + 1] is '':
						board[row + 1][col + 1] = "X"
						openings += 1
					elif lookout in board[row + 1][col + 1]:
						board[row + 1][col + 1] += "X"
						openings += 1
			if row != 0:
				if col != 0:
					if board[row - 1][col - 1] is '':
						board[row - 1][col - 1] = "X"
						openings += 1
					elif lookout in board[row - 1][col - 1]:
						board[row - 1][col - 1] += "X"
						openings += 1
				if col != 8:
					if board[row - 1][col + 1] is '':
						board[row - 1][col + 1] = "X"
						openings += 1
					elif lookout in board[row - 1][col + 1]:
						board[row - 1][col + 1] += "X"
						openings += 1

		return board, openings

	def promote(self):
		self.promoted = True
		self.name = "Promoted Silver General"
		self.condensed_string = "+S"

	def demote(self):
		self.promoted = False
		self.name = "Silver General"
		self.condensed_string = "S"

	def __str__(self):
		return self.condensed_string


class Knight(Piece):

	def __init__(self, player, x, y, promoted=False):
		super(Knight, self).__init__(player, x, y, promoted)
		if promoted is True:
			self.name = "Promoted Knight"
			self.condensed_string = "+N"
		else:
			self.name = "Knight"
			self.condensed_string = "N"
		self.identifier = "Knight"

	def highlight(self, board):
		if self.promoted:
			board, openings = self.highlight_standard_promoted(board)
			return board, openings
		row = self.y
		col = self.x
		if self.player is 1:
			lookout = "!"
		else:
			lookout = "^"
		openings = 0

		if self.player == 1:
			if row > 1 and col > 0 and board[row - 2][col - 1] is '':
				board[row - 2][col - 1] = "X"
				openings += 1
			elif row > 1 and col > 0 and lookout in board[row - 2][col - 1]:
				board[row - 2][col - 1] += "X"
				openings += 1
			if row > 1 and col < 8 and board[row - 2][col + 1] is '':
				board[row - 2][col + 1] = "X"
				openings += 1
			elif row > 1 and col < 8 and lookout in board[row - 2][col + 1]:
				board[row - 2][col + 1] += "X"
				openings += 1	
			return board, openings
		else:
			if row < 7 and col > 0 and board[row + 2][col - 1] is '':
				board[row + 2][col - 1] = "X"
				openings += 1
			elif row < 7 and col > 0 and lookout in board[row + 2][col - 1]:
				board[row + 2][col - 1] += "X"
				openings += 1
			if row < 7 and col < 8 and board[row + 2][col + 1] is '':
				board[row + 2][col + 1] = "X"
				openings += 1
			elif row < 7 and col < 8 and lookout in board[row + 2][col + 1]:
				board[row + 2][col + 1] += "X"
				openings += 1	
			return board, openings
		if openings == 0:
			if self.player == 1:
				if row < 2:
					self.promote()
					board, openings = self.highlight_standard_promoted(board)
					return board, openings
			else:
				if row > 6:
					self.promote()
					board, openings = self.highlight_standard_promoted(board)
					return board, openings
		return board, openings

	def promote(self):
		self.promoted = True
		self.name = "Promoted Knight"
		self.condensed_string = "+N"

	def demote(self):
		self.promoted = False
		self.name = "Knight"
		self.condensed_string = "K"

	def __str__(self):
		return self.condensed_string


class Lance(Piece):

	def __init__(self, player, x, y, promoted=False):
		super(Lance, self).__init__(player, x, y, promoted)
		if promoted is True:
			self.name = "Promoted Lance"
			self.condensed_string = "+L"
		else:
			self.name = "Lance"
			self.condensed_string = "L"
		self.identifier = "Lance"

	def highlight(self, board):
		if self.promoted:
			board, openings = self.highlight_standard_promoted(board)
			return board, openings
		row = self.y
		col = self.x
		if self.player is 1:
			lookout = "!"
			own = "^"
		else:
			lookout = "^"
			own = "!"
		openings = 0

		if self.player == 1:
			for i in range(1, 9):
				if row == 0:
					break
				if row - i > 0 and board[row - i][col] is '':
					board[row - i][col] = "X"
					openings += 1
				elif row - i > 0 and lookout in board[row - i][col]:
					board[row - i][col] += "X"
					openings += 1
					return board, openings
				elif row - i > 0 and own in board[row - i][col]:
					return board, openings 
		else:
			for i in range(1, 9):
				if row == 8:
					break
				if row + i < 8 and board[row + i][col] is '':
					board[row + i][col] = "X"
					openings += 1
				elif row + i < 8 and lookout in board[row + i][col]:
					board[row + i][col] += "X"
					openings += 1
					return board, openings
				elif row + i < 8 and own in board[row + i][col]:
					return board, openings 
			
		if openings == 0:
			if self.player == 1:
				if row == 0:
					self.promote()
					board, openings = self.highlight_standard_promoted(board)
					return board, openings
			else:
				if row == 8:
					self.promote()
					board, openings = self.highlight_standard_promoted(board)
					return board, openings
		return board, openings

	def promote(self):
		self.promoted = True
		self.name = "Promoted Lance"
		self.condensed_string = "+L"

	def demote(self):
		self.promoted = False
		self.name = "Lance"
		self.condensed_string = "L"

	def __str__(self):
		return self.condensed_string


class Pawn(Piece):

	def __init__(self, player, x, y, promoted=False):
		super(Pawn, self).__init__(player, x, y, promoted)
		if promoted is True:
			self.name = "Promoted Pawn"
			self.condensed_string = "+P"
		else:
			self.name = "Pawn"
			self.condensed_string = "P"
		self.identifier = "Pawn"

	def highlight(self, board):
		if self.promoted:
			board, openings = self.highlight_standard_promoted(board)
			return board, openings
		row = self.y
		col = self.x
		if self.player is 1:
			lookout = "!"
		else:
			lookout = "^"
		openings = 0

		if self.player == 1:
			if row != 0 and board[row - 1][col] is '':
				board[row - 1][col] = "X"
				openings += 1
			elif row != 0 and lookout in board[row - 1][col]:
				board[row - 1][col] += "X"
				openings += 1
			return board, openings
		else:
			if row != 8 and board[row + 1][col] is '':
				board[row + 1][col] = "X"
				openings += 1
			elif row != 8 and lookout in board[row + 1][col]:
				board[row + 1][col] += "X"
				openings += 1
			return board, openings
		if openings == 0:
			if self.player == 1:
				if row == 0:
					self.promote()
					board, openings = self.highlight_standard_promoted(board)
					return board, openings
			else:
				if row == 8:
					self.promote()
					board, openings = self.highlight_standard_promoted(board)
					return board, openings
		return board, openings

	def promote(self):
		self.promoted = True
		self.name = "Promoted Pawn"
		self.condensed_string = "+P"

	def demote(self):
		self.promoted = False
		self.name = "Pawn"
		self.condensed_string = "P"

	def __str__(self):
		return self.condensed_string