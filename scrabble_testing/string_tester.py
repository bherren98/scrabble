import resources
import itertools

letters = ['A', 'L', 'S', 'E', 'R', 'W', 'H']

def find_all_combinations(hand):
	combinations = []
	for i in range(1, len(letters)+1):
		combinations = combinations + list(itertools.combinations(letters, i))
	for combination in combinations:
		print(combination)
		is_possible = False
		word_found = ""
		for word in resources.word_dict:
			is_match = True
			for letter in combination:
				if (letter not in word):
					is_match = False
					break
			if (is_match):
				is_possible = True
				word_found = word
				break
		if (is_possible):
			print(word)
			print(combination)


def find_all_iterations(hand):
	iterations = []
	for i in range(1, len(letters)+1):
		iterations = iterations + list(itertools.permutations(letters, i))
	for iteration in iterations:
		if len(iteration) == 7:
			print(iteration)

	return iterations

combinations = find_all_combinations(letters)