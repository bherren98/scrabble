import csv
import itertools
import resources # word_dict, letter_values, initial_letter_counts, board_multipliers, tile_combos
from time import strftime
import time

start = time.time()
local_path = "C:\\Users\\brand\\Documents\\scrabble_testing\\"

# Read-in board
board = []
with open('test_board.csv', 'r') as csvfile:
	board_reader = csv.reader(csvfile)
	for row in board_reader:
		board.append(row)

letters = ['I', 'N', 'N', 'N', 'L', 'I', 'N']
for i, letter in enumerate(letters):
	if (letter == "*"):
		letters[i] = 'S'

def find_all_hand_possibilities(hand):
	possibilities = []
	real_words = []

	for i in range(1, len(letters)):
		possibilities = possibilities + list(itertools.permutations(letters, i))
	for possibility in possibilities:
		possibility = ''.join(possibility)
		if (possibility in resources.word_dict):
			real_words.append(possibility)

	return real_words

def find_all_iterations(hand):
	iterations = []
	for i in range(1, len(letters)+1):
		iterations = iterations + list(itertools.permutations(letters, i))

	return iterations

def segment_hand_possibilities_by_length(hand_possibilities):
	by_length = [[], [], [], [], [], [], [], []]
	for possibility in hand_possibilities:
		by_length[len(possibility)].append(possibility)

	return by_length

def get_board_cols(board):
	cols = []
	for i in range(15):
		cols.append([])
	for row in board:
		for i, tile in enumerate(row):
			cols[i].append(tile)

	return cols

def find_adjacent_spots(board):
	adjacent_spots = []
	for row in range(15):
		for col in range(15):
			adjacent_tiles = ['0', '0', '0', '0'] #[up, down, left, right]
			if (row != 0): # up
				adjacent_tiles[0] = board[row-1][col]
			if (row != 14): # down
				adjacent_tiles[1] = board[row+1][col]
			if (col != 0): # left
				adjacent_tiles[2] = board[row][col-1]
			if (col != 14): # right
				adjacent_tiles[3] = board[row][col+1]

			for tile in adjacent_tiles:
				if (tile != '0' and board[row][col] == '0'):
					adjacent_spots.append([row, col])

	uniques = []
	for spot in adjacent_spots:
		if (spot not in uniques):
			uniques.append(spot)

	return uniques

def is_consecutive(num_list):
	for i in range(len(num_list)-1):
		if (num_list[i] + 1 != num_list[i+1]):
			return False
	return True

def find_all_moves(hand, board, possibilities_by_length):
	# move template: [[row, col], word, score, defensive_cost_est]
	tile_combos = resources.tile_combos
	moves = []
	best_move = ""
	best_score = 0
	# checking if board is empty
	is_empty = True
	for row in board:
		for tile in row:
			if (tile != '0'):
				is_empty = False
				break
		if (not is_empty):
			break
	# going through each row
	for row_index, row in enumerate(board):
		adjacent_indices = []
		empty_indices = []
		empty_index_adjacent_indices = []
		empty_count = 0
		# determining empty tiles, adjacent tiles
		for i, tile in enumerate(row):
			before = '0'
			after = '0'
			above = '0'
			below = '0'
			if (i != 0):
				before = row[i-1]
			if (i != 14):
				after = row[i+1]
			if (row_index != 0):
				above = board[row_index-1][i]
			if (row_index != 14):
				below = board[row_index+1][i]
			if (tile == '0'):
				if (before != '0' or after != '0' or above != '0' or below != '0'):
					adjacent_indices.append(i)
					empty_index_adjacent_indices.append(empty_count)
				empty_indices.append(i)
				empty_count += 1
		if (is_empty and row_index == 7):
			adjacent_indices.append(7)
			empty_index_adjacent_indices.append(7)

		row_words = []
		for combo in tile_combos:
			if (combo[len(combo)-1] < len(empty_indices)+1):
				for index in empty_index_adjacent_indices:
					if (index in combo):
						for possibility in possibilities_by_length[len(combo)-1]:
							row_temp = row.copy()
							
							for i, letter in enumerate(possibility):
								row_temp[empty_indices[combo[i]]] = letter

							word = row_temp[empty_indices[index]]
							for a in range(empty_indices[index]+1, 15):
								if (row_temp[a] != '0'):
									word = word + row_temp[a]
								else:
									break
							beginning_temp = ""
							for b in range(0, empty_indices[index]):
								if (row_temp[b] != '0'):
									beginning_temp = beginning_temp + row_temp[b]
								else:
									beginning_temp = ""

							word = beginning_temp + word
							if (word in resources.word_dict):
								side_words = []
								word_location = [word, empty_indices[combo[0]]]
								if (word_location not in row_words):
									side_okay = True
									side_bonus_score = 0
									letter_subtraction = 0
									for i, letter in enumerate(possibility):
										col = empty_indices[combo[i]]
										side_word = row_temp[empty_indices[combo[i]]]
										for a in range(row_index+1, 15):
											if (board[a][col] != '0'):
												side_word = side_word + board[a][col]
											else:
												break
										b_temp2 = ""
										for b in range(0, row_index):
											if (board[b][col] != '0'):
												b_temp2 = b_temp2 + board[b][col]
											else:
												b_temp2 = ""

										side_word = b_temp2 + side_word

										if (side_word in resources.word_dict or len(side_word) == 1):
											if (len(side_word) > 1):
												side_words.append(side_word)
												multiplier = resources.board_multipliers[empty_indices[combo[i]]]
												if (multiplier == 'DW'):
													side_bonus_score += resources.letter_values[letter] * 2
													letter_subtraction += resources.letter_values[letter]
												if (multiplier == 'TW'):
													side_bonus_score += resources.letter_values[letter] * 3
													letter_subtraction += resources.letter_values[letter]
										else:
											side_okay = False
											break

									if (side_okay):
										# score calculating
										beginning_index = empty_indices[index] - len(beginning_temp)
										base_score = 0
										multiplier = 1
										for i, letter in enumerate(word):
											base_value = resources.letter_values[letter]
											if ((beginning_index + i) in empty_indices):
												board_multiplier = resources.board_multipliers[row_index][beginning_index+i]
												if (board_multiplier == 'DL'):
													base_value *= 2
												if (board_multiplier == 'TL'):
													base_value *= 3
												if (board_multiplier == 'DW'):
													multiplier *= 2
												if (board_multiplier == 'TW'):
													multiplier *= 3
											base_score += base_value
										score = base_score * multiplier

										side_score = side_bonus_score * multiplier
										for word in side_words:
											for letter in word:
												side_score += resources.letter_values[letter]
										score += side_score - letter_subtraction
										# scrabble "bingo" for using all 7 letters
										#if (len(combo) == 8):
										#	score += 50

										word_stats = {
											"word": word,
											"row": row_index,
											"col": word_location[1],
											"side_words": side_words,
											"score": score
										}
										if (score > best_score):
											best_move = word_location[0] + ": (" + str(row_index) + ", " + str(word_location[1]) + "), Score: " + str(score) + ", " + str(side_words)
											best_score = score

										moves.append(word_stats)
										row_words.append(word_location)
										#print(word_location[0] + ": (" + str(row_index) + ", " + str(word_location[1]) + "), Score: " + str(score) + ", " + str(side_words))
										word_end = time.time()
										if (word_end - start > 4.6):
											print("Total Moves Found: " + str(len(moves)))
											print("Best Move: " + best_move)
											return [moves, best_move, best_score]
						break
										
	print("Total Moves Found: " + str(len(moves)))
	print("Best Move: " + best_move)
	return [moves, best_move, best_score]

def choose_best_move(board):
	num_tiles = 0
	for row in board:
		for tile in row:
			if (tile != '0'):
				num_tiles += 1

	board_cols = get_board_cols(board)
	board_rows = board
	hand_iterations = find_all_iterations(letters)
	possibilities_by_length = segment_hand_possibilities_by_length(hand_iterations)

	print("searching vertical moves...")
	vertical_moves = find_all_moves(letters, board_cols, possibilities_by_length)
	print("-----------------------------")
	vertical_end = time.time()
	if (vertical_end - start < 4.2):
		print("searching horizontal moves...")
		horizontal_moves = find_all_moves(letters, board_rows, possibilities_by_length)
		if (horizontal_moves[2] > vertical_moves[2]):
			print("-----------------------------")
			print("Move chosen: " + horizontal_moves[1])
		else:
			print("-----------------------------")
			print("Move chosen: " + vertical_moves[1])
	else:
		print("-----------------------------")
		print("Move chosen: " + vertical_moves[1])

choose_best_move(board)
