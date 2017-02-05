"""
Shogi Main File
"""
from Board import Board
from Mechanics import *
import RandomAI
import time
import NeuralNet
import numpy as np

def main():

	num_players = get_num_players()
	players = setup_players(num_players, 0)
	board = Board()

	turn_num = 0
	start_time = time.time()
	while True:
		if players[0] == 0:
			human_turn(board, 1)
		elif players[0] == 2:
			RandomAI.ai_turn(board, 1)

		ret = checkmate(board)
		if ret == 1:
			print "\nPlayer 1 Has Won the Game!!!!"
			break
		elif ret == 2:
			print "\nPlayer 2 Has Won the Game!!!!"
			break

		if players[1] == 0:
			human_turn(board, 2)
		elif players[1] == 2:
			RandomAI.ai_turn(board, 2)

		ret = checkmate(board)
		if ret == 1:
			print "\nPlayer 1 Has Won the Game!!!!"
			break
		elif ret == 2:
			print "\nPlayer 2 Has Won the Game!!!!"
			break
			
		turn_num += 1

	elasped_time = time.time() - start_time

	print "\nFinal Board Layout:\n"
	board.display()
	print "\nStats:"
	print "Winner: Player %d" % ret
	print "Number of Turns: %d" % turn_num
	print "Time Taken: %s" % format_time(elasped_time)
	print "Average Time per Turn: %s" % format_time(elasped_time / float(turn_num))
	print "Turns per Second: %f" % (float(turn_num) / elasped_time)


def train_mode():
	nn = NeuralNet.NeuralNet()
	nn.train()


def format_time(seconds):
	m, s = divmod(seconds, 60)
	h, m = divmod(m, 60)
	formated = ""
	if h != 0:
		if h == 1:
			formated += "1 hour"
		else:	
			formated += "%d hours" % h
	if m != 0:
		if len(formated) != 0:
			formated += ", "
		if m == 1:
			formated += "1 minute"
		else:
			formated += "%d minutes" % m
	if s != 0:
		if len(formated) != 0:
			formated += ", "
		if s == 1:
			formated += "1 second"
		elif int(s) == s:
			formated += "%d seconds" % s 
		else:
			formated += "%.3f seconds" % s 
	return formated

def get_num_players():
	success = False
	while not success:
		try:
			literal = raw_input("How many human players? (0, 1, 2): ")
			players = int(literal)
			success = True
			if players < 0 or players > 2:
				print "Invalid Number of Players: %d" % players
				success = False
		except Exception:
			print "Invalid: Input not an Integer: %s" % literal
			success = False
	# smart = int(raw_input("How many Smart AI? "))
	# add error checking later
	return players

def setup_players(num_human, num_smart):
	# 0 = Human, 1 = SmartAI, 2 = RandomAI
	# Will change if add NN AI.
	if num_human == 2:
		return [0, 0]
	if num_human == 1:
		if num_smart == 1:
			return [0, 1]
		else:
			return [0, 2]
	if num_smart == 2:
		return [1, 1]
	elif num_smart == 1:
		return [1, 2]
	else:
		return [2, 2]

if __name__ == '__main__':
	choice = raw_input("(t)rain or (p)lay? ")
	if choice == "p":
		main()
	elif choice == "t":
		train_mode()