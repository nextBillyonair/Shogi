import Board
import Mechanics
from random import shuffle

def ai_turn(board, player_num, show_bd = False):
	if player_num is 1: 
		opp = 2
	else:
		opp = 1 
	c1 = Mechanics.check(board, opp)
	c2 = Mechanics.check(board, player_num)
	print "\nPlayer %d's Turn" % player_num
	if c1:
		print "You are in check!"
	if c2:
		print "Player %d is in check!" % opp
	if not show_bd:
		board.display()
	pieces = get_piece_list(board, player_num)
	pieces = shuffle_list(pieces)
	tmp_board = make_tmp_board(board)
	openings = 0
	index = 0
	dropped = False
	while openings == 0:
		if pieces[index].y == -1:
			openings, dropped = ai_drop(board, pieces[index], tmp_board, player_num)
		else:
			tmp_board, openings = pieces[index].highlight(tmp_board)
		if openings == 0:
			index += 1
	if not dropped:
		row, col = shuffle_list(get_move_list(tmp_board))[0]
		r, c = pieces[index].y, pieces[index].x
		board.board[r][c].move(col, row, board.board, tmp_board, board,True)
	# time.sleep(1)
	return True

def ai_drop(board, piece, tmp_board, player_num):
	drop_list = list()
	for row in range(9):
		for col in range(9):
			if not tmp_board[row][col]:
				drop_list.append((row, col))
	drop_list = shuffle_list(drop_list)
	row, col = drop_list[0]
	if player_num is 1:
		if (piece.name == "Pawn" or piece.name == "Lance" or piece.name == "Knight") and row == 0:
			print "Invalid: Cannot place %s on furthest rank" % piece.name
			return 0, False
		if piece.name == "Knight" and row == 1:
			print "Invalid: Cannot place Knight on player's 8th rank (second to last row forward)"
			return 0, False
	else:
		if (piece.name == "Pawn" or piece.name == "Lance" or piece.name == "Knight") and row == 8:
			print "Invalid: Cannot place %s on furthest rank" % piece.name
			return 0, False
		if piece.name == "Knight" and row == 7:
			print "Invalid: Cannot place Knight on player's 8th rank (second to last row forward)"
			return 0, False
		
	if piece.name == "Pawn":
		# Nifu
		for index in range(0, 9):
			if board.board[index][col] is not None and board.board[index][col].name == "Pawn" and board.board[index][col].player == player_num:
				print "Nifu! Pawn cannot be dropped on column with another unpromoted pawn of yours!"
				return 0, False
	# if success 1, True
	if player_num is 1:
		holder = board.player_one_holder
	else:
		holder = board.player_two_holder
	for i in range(len(holder)):
		if holder[i].name == piece.name:
			break
	board.drop(row, col, player_num, i)
	return 1, True

def get_move_list(temp_board):
	valid = list()
	for row in range(9):
		for col in range(9):
			if "X" in temp_board[row][col]:
				valid.append((row, col))
	return valid

def make_tmp_board(board):
	temp_board = list()
	for row in range(board.dim):
		row_lst = list()
		for col in range(board.dim):
			row_lst.append(board.get_str(board.board[row][col]))
		temp_board.append(row_lst)
	return temp_board

def get_piece_list(board_obj, player_num):
	lst_of_pieces = list()
	for i in range(9):
		for j in range(9):
			piece = board_obj.board[i][j]
			if piece is not None:
				if piece.player == player_num:
					lst_of_pieces.append(piece)
	if player_num == 1:
		holder = board_obj.player_one_holder
	else:
		holder = board_obj.player_two_holder
	for i in holder:
		lst_of_pieces.append(i)
	return lst_of_pieces

def shuffle_list(lst):
	shuffle(lst)
	return lst