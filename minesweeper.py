import random
import os
import itertools
import msvcrt

clear = lambda: os.system('cls')

tiles = { # tiles used for display
	0:  "  -  ",
	1:  "  1  ",
	2:  "  2  ",
	3:  "  3  ",
	4:  "  4  ",
	5:  "  5  ",
	6:  "  6  ",
	7:  "  7  ",
	8:  "  8  ",
	9:  "  9  ",
	10: "█████",
	11: "  +  "
}

# clear neighbours, for cascading discovery
def clear_neighbours(table, x, y):
	if (table[x][y]):
		return table
	else:
		for i in range(-1,2):
			for j in range(-1,2):
				if (x + i < 0 or y + j < 0):
					continue
				else:	
					try:
						table[x + i][j + i] = False
					except:
						pass 
	return table

# find neighbouring bombs
def neighbour(table, x, y):
	count = 0

	for i in range(-1,2):
		for j in range(-1,2):
			if (x + i < 0 or y + j < 0):
				continue
			else:	
				try:
					count += 1 if table[x + i][y + j] else 0
				except:
					pass 
	return count

# display function
def printTable(table, _mask):
	top_index = []
	for i in range(len(table[0])):
		index = str(i + 1)
		index = " " + index + " " if int(index) < 10 else " " + index
		top_index.append("[" + index + "]")
	print("[y\\x]" + "".join(top_index))

	for i in range(len(table)):
		y_index = str(i + 1)
		y_index = " " + y_index + " " if int(y_index) < 10 else " " + y_index # ternary to centre
		side_index = "[" + y_index + "]" # brackets
		print(side_index, end = "")
		for j in range(len(table)):
			if (_mask[i][j] == False):
				if (table[i][j]):
					neighbours = 11 # it's a mine
				else:
					neighbours = neighbour(table, i, j)

				print(tiles[neighbours], end = "") 
			else:
				print(tiles[10], end="") # not discovered yet
		print()

# main game loop
def main():
	# set up phase

	# declarations
	board = [] # gameboard
	mask = [] # undiscovered gamefield

	visible = False # If the board is visible or not (makes game unwinable)
	alive = True # self explanatory

	clear() # clear screen? I hope you didn't need to read this comment...

	print("Input board size(8): ", end = '')
	size = 8 # default size, you may change this

	try:
		size = int(input())
	except:
		pass

	print("Input difficulty(0-10, 5 by default): ", end = "")
	difficulty = 5 / 15 # default difficulty, you may change this
	try:
		difficulty = int(input()) / 15 # x / 15 = x * 0.66, aka two thirds, 0 is a free game, and 15 is straight up impossible (it´s a win by default)
	except:
		pass

	mines = 0

	# board filling (random)
	for i in range(size):
		line = [] # board line, the generation is linewise
		m_line = list(itertools.repeat(not visible, size)) # change to False if you want to see a clear board by default
		for j in range(size):
			line.append(True if random.random() < difficulty else False) 
		board.append(line)
		mines += line.count(True)
		mask.append(m_line)
	first_move = True
	# main loop
	while True: 
		clear()
		print ("Mines: ", mines)
		printTable(board, mask) # call display function
		if (not alive):
			lose()
			break

		if (mask == board and not first_move):
			win()
			break

		print("next move(x, y): ", end = "")
		a = input()
		if (a.lower() == "quit"):
			alive == False
			continue
		move = a.split(",")
		print(move)
		x = 0
		y = 0
		if (len(move) == 2): # validate move
			try:
				y = int(move[0]) - 1
				x = int(move[1]) - 1
			except:
				print("invalid move (NaN)")
				print("press any key...", end = "")
				msvcrt.getch()
				continue
		else:
			print("invalid move (not in the format [x,y])")
			print("press any key...", end = "")
			msvcrt.getch()
			continue

		if (not 0 <= x < size or not 0 <= y < size):
			print("invalid move (out of range)")
			print("press any key...", end = "")
			msvcrt.getch()
			continue

		print(move)

		if (mask[x][y]):
			mask[x][y] = False	

		if (first_move):
			if (board[x][y]):
				mines -= 1
			board[x][y] = False
			first_move = False

		if (board[x][y]):
			alive = False
			continue

		if (neighbour(board, x, y) == 0):
			mask = clear_neighbours(mask, x, y)
			for i in range(size):
				for j in range(size):
					if (mask[i][j]):
						continue
					else:
						if (neighbour(board, i, j) == 0):
							mask = clear_neighbours(mask, i, j)
			# for i in range(1, size + 1):
			# 	for j in range(1, size + 1):
			# 		if (mask[size - i][size - j]):
			# 			continue
			# 		else:
			# 			if (neighbour(board, i, j) == 0):
			# 				mask = clear_neighbours(mask, size - i, size - j)

def win():
	print("Congratulations, YOU won!")
	print("Thanks for playing")
	print("Play again? (y/n)")
	a = input().lower()
	if (a == "y" or a == "yes"):
		main()
	else:
		print("Goodbye!")

def lose():
	print("You lost...")
	print("Play again? (y/n)")
	a = input().lower()
	if (a == "y" or a == "yes"):
		main()
	else:
		print("Goodbye!")

main()