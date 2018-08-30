import resources
import itertools

def get_unused_three_letter_combos():
	alphabet = list(resources.letter_values.keys())
	alphabet.pop()
	alpha_iterations = list(itertools.permutations(alphabet, 3))
	unused = []
	for iteration in alpha_iterations:
		used = False
		alpha_str = str(iteration).upper()
		print(alpha_str)
		for word in resources.word_dict:
			if alpha_str in word:
				used = True
				break

		if (not used):
			unused.append("".join(list(alpha_str)))

	return unused

#print(get_unused_three_letter_combos())
print(type(resources.letter_values['A']))