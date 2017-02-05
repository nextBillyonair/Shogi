"""
Shogi Mechanics File
"""

codes = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7, "I": 8}
rev_codes = {0:"A", 1:"B", 2:"C", 3:"D", 4:"E", 5:"F", 6:"G", 7:"H", 8:"I"}

def human_turn(board, player):
	# P1
	did_move = False
	if player == 1:
		opp = 2
	else:
		opp = 1
	c1 = check(board, opp)
	c2 = check(board, player)
	print "\nPlayer %d's Turn" % player
	if c1:
		print "You are in check!"
	if c2:
		print "Player %d is in check!" % opp
	first = False
	while not did_move:
		if first:
			print "\nPlayer %d's Turn" % player
		first = True
		tmp_board = board.deepcopy()
		board.display()
		selection = str(raw_input("Selected Position: "))
		did_move = interpret_selection(selection, tmp_board, player)
	board.assignment(tmp_board)
	return False

def interpret_selection(sel, board, p):
	if len(sel) > 2:
		print "Too many variables to parse..."
		if "d" in sel:
			print "Did you mean (d)rop?"
		if "h" in sel:
			print "Did you mean (h)elp?"
		return False
	if len(sel) == 1:
		if sel == "h":
			print_help()
			return False
		if sel == "d":
			return drop(board, p)
		return False
	row, col = get_coord(sel)
	if row is None: return False
	if row < 0 or row > 8:
		print "Invalid row: %s" % row
		return False
	if col < 0 or col > 8:
		print "Invalid col: %s" % col
		return False
	if board.board[row][col] is None:
		print "Invalid: No piece present at %s%s" % (rev_codes[row], col)
		return False
	if board.board[row][col].player is not p:
		print "Invalid: selected %s is owned by Player %d" % (board.board[row][col].name, board.board[row][col].player)
		return False

	moving = board.move(row, col)
	return moving

def get_coord(sel):
	try:
		try:
			row = codes.get(sel[0].upper(), -1)
			col = int(sel[1])
		except Exception:
			row = codes.get(sel[1].upper(), -1)
			col = int(sel[0])
	except Exception:
		print "Invalid selection: %s" % sel
		return None, None
	return row, col

def drop(board, p):
	if p is 1:
		bucket_len = len(board.player_one_holder)
	else:
		bucket_len = len(board.player_two_holder)

	if bucket_len is 0:
		print "Inavlid: Player %d's bucket is empty" % p
		return False
	print "Listing Player %d's available pieces:" % p
	print board.get_bucket_str(p)
	indexes = ""
	for i in range(bucket_len):
		indexes += "%d  " % i
	print indexes
	try:
		sel = raw_input("Select Index to Drop: ")
		i = int(sel)
	except Exception:
		print "Invalid: Selected index %s is not a number" % sel
		return False
	if i >= bucket_len or i < 0:
		print "Invalid: Index %d is out of range" % i 
		return False
	
	if p is 1:
		print "Player %d selected %s" % (p, board.player_one_holder[i].name)
	else:
		print "Player %d selected %s" % (p, board.player_two_holder[i].name)

	selection = str(raw_input("Selected Position: "))
	if len(selection) > 2:
		print "Too many variables to parse..."
		return False
	elif len(selection) < 2:
		print "Too little variables to parse..."
		return False
	else:
		row, col = get_coord(selection)
		if row is None: return False
		if row < 0 or row > 8:
			print "Invalid row: %s" % row
			return False
		if col < 0 or col > 8:
			print "Invalid col: %s" % col
			return False
		if board.board[row][col] is not None:
			print "Invalid: Selected position %s is occupied by Player %d's %s" % (selection, board.board[row][col].player, board.board[row][col].name)
			return False
		
		if p is 1:
			piece = board.player_one_holder[i]
			if (piece.name == "Pawn" or piece.name == "Lance" or piece.name == "Knight") and row == 0:
				print "Invalid: Cannot place %s on furthest rank" % piece.name
				return False
			if piece.name == "Knight" and row == 1:
				print "Invalid: Cannot place Knight on player's 8th rank (second to last row forward)"
				return False
		else:
			piece = board.player_two_holder[i]
			if (piece.name == "Pawn" or piece.name == "Lance" or piece.name == "Knight") and row == 8:
				print "Invalid: Cannot place %s on furthest rank" % piece.name
				return False
			if piece.name == "Knight" and row == 7:
				print "Invalid: Cannot place Knight on player's 8th rank (second to last row forward)"
				return False
		
		if piece.name == "Pawn":
			# Nifu
			for index in range(0, 9):
				if board.board[index][col] is not None and board.board[index][col].name == "Pawn" and board.board[index][col].player == p:
					print "Nifu! Pawn cannot be dropped on column with another unpromoted pawn of yours!"
					return False
			# Uchifuzume - no pawn drop to give immediate checkmate
			### IDEA: use check function on hypothetical board with supposed drop?
		# All Good
		board.drop(row, col, p, i)
		print "Player %d dropped %s at %s%s" % (p, piece.name, rev_codes[row], col)
		return True
			
def check(board, p):
	temp_board = list()
	for row in range(9):
		row_lst = list()
		for col in range(9):
			if board.board[row][col] is not None:
				row_lst.append(board.get_str(board.board[row][col]))
			else:
				row_lst.append("")				
		temp_board.append(row_lst)
	for r in range(9):
		for c in range(9):
			if board.board[r][c] is not None:
				if board.board[r][c].player == p:
					temp_board, openings = board.board[r][c].highlight(temp_board)
	if p is 2:
		row = board.p1_king["row"]
		col = board.p1_king["col"]
		if "X" in temp_board[row][col]:
			print "Ote! Player 2 has placed Player 1's King in Check!"
			return True
	else:
		row = board.p2_king["row"]
		col = board.p2_king["col"]
		if "X" in temp_board[row][col]:
			print "Ote! Player 1 has placed Player 2's King in Check!"
			return True
	return False
	

def checkmate(board):
	# IDEA: Return True if king captured, else False
	# P1
	row = board.p1_king["row"]
	col = board.p1_king["col"]
	if row == -1 and col == -1:
		print "Player 1's King has been Captured! Checkmate!"
		return 2
	# P2
	row = board.p2_king["row"]
	col = board.p2_king["col"]
	if row == -1 and col == -1:
		print "Player 2's King has been Captured! Checkmate!"
		return 1
	return 0

def print_help():
	print """Shogi is a Japanese board game played by two players.
The object of the game is to capture the opponent's King.
Shogi is played on a nine-by-nine board.\n
Each player has twenty pieces:
	1 (K)ing, 2 (G)old Generals, 2 (S)ilver Generals,
	2 k(N)ights, 2 (L)ances, 1 (R)ook,
	1 (B)ishop and 9 (P)awns.\n
THE MOVES
Standard:
	(K)ing            -> one step in any direction per move
	(G)old General    -> one step per move any way except diagonally backwards
	(S)ilver General  -> one step per move forwards or diagonally
	K(N)ight          -> one step to left or right, and two steps forward (may jump over others)
	(R)ook            -> moves vertically or horizontally any distance
	(B)ishop          -> moves diagonally any distance 
	(L)ance           -> moves forward any distance
	(P)awn            -> one step forward
Promoted:
	(+S)ilver General -> move as Gold
	K(+N)ight         -> move as Gold
	(+L)ance          -> move as Gold
	(+P)awn           -> move as Gold
	(+R)ook           -> standard Rook or one step in the diagonal directions
	(+B)ishop         -> standard Bishop or one step in orthogonal directions.

PROMOTION
The three rows furthest away from a player are called the promotion zone.
Apart from the King and the Gold, any piece can be promoted to a more powerful piece 
when it makes a move completely or partly in the promotion zone. 
Promotion is optional, provided that the piece still can make a legal move in case it is 
not promoted: if a Pawn or a Lance move to the last row, or a Knight moves to either of 
the last two rows, it must be promoted.

CAPTURING
When one piece moves onto the same square as an opponent's piece, the opponent's 
piece is captured. All pieces capture in the same way that they move. 
Captured pieces become part of the capturer's force. 

DROPPING
A player may put a piece that he has captured from his opponent back onto the board, in an empty square.
Pieces are always dropped unpromoted
THREE RESTRICTIONS:
	1) After dropping a piece it must be able to make a legal move.
	2) Attacking the King by dropping a Pawn on the square in front of him is 
	   not allowed if the King cannot prevent being captured on the following move
	3) A pawn may only be dropped on a file (vertical row) if there is no other 
	   unpromoted pawn of the same player on that file
"""