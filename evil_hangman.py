from itertools import chain, combinations
import random

def load_words():
	with open("english-words/words_alpha.txt") as word_file:
		valid_words = set(word_file.read().split())

	return valid_words

def powerset(iterable):
	xs = list(iterable)
	return chain.from_iterable(combinations(xs,n) for n in range(len(xs) + 1))

def check_pattern(pattern, word, letter) :
	for i in range(len(pattern)) :
		if pattern[i] == '_' :
			if word[i] == letter :
				return False
		else :
			if word[i] != pattern[i] :
				return False

	return True

class PuzzleState :
	def __init__(self, length, word_list):
		self.currentDisplay = ""
		for _ in range(length) :
			self.currentDisplay += '_'
		self.checkedLetters = ""
		self.numWrongGuesses = 0
		self.word_list = [word for word in word_list if len(word) == length]
		print self.currentDisplay

	def guess(self, guessedLetter):
		"""Check if guess is valid"""
		if guessedLetter in self.checkedLetters :
			print "You guessed that already."
			return
		elif len(guessedLetter) != 1 or guessedLetter not in "qwertyuiopasdfghjklzxcvbnm":
			print "Not a real guess. Try again."
			return
		else :
			self.checkedLetters += guessedLetter

		"""get positions of blank spots, then find all subsets of these positions, then make patterns to represent these subsets"""
		blankSpots = []
		for letter, i in zip(self.currentDisplay, range(len(self.currentDisplay))) :
			if letter == '_' :
				blankSpots.append(i)

		blankSpotsSubsets = powerset(blankSpots)
		possiblePatterns = dict()
		for subset in blankSpotsSubsets :
			possibleGuess = ""
			for letter, i in zip(self.currentDisplay, range(len(self.currentDisplay))) :
				if letter == '_' :
					if i in subset :
						possibleGuess += guessedLetter
					else :
						possibleGuess += '_'
				else :
					possibleGuess += letter
			possiblePatterns[possibleGuess] = 0

		"""for each possible pattern, count number of words that fill it"""
		for word in self.word_list :
			for pattern, _ in possiblePatterns.items() :
				if check_pattern(pattern, word, guessedLetter) :
					possiblePatterns[pattern] += 1
					break

		"""find pattern with most words that fit it"""
		maxNum = 0
		bestPattern = ""
		for pattern, num in possiblePatterns.items() :
			if num > maxNum :
				bestPattern = pattern
				maxNum = num

		if bestPattern == self.currentDisplay :
			self.numWrongGuesses += 1
			print "Nope. That's not in there. You have " + str(self.numWrongGuesses) + " wrong guesses."
		else :
			print "You got one, you scrub!"
			self.currentDisplay = bestPattern

		self.word_list = [word for word in self.word_list if check_pattern(bestPattern, word, guessedLetter)]
		print self.currentDisplay




if __name__ == "__main__" :
	word_list = load_words()
	print "I hear you're the worst Hangman player ever."
	print "I bet you couldn't win a game with 15 chances!"

	length = 0
	length = random.randint(3, 8)
	puzzleState = PuzzleState(length, word_list)
	while True :
		theirGuess = str(raw_input("Gimme a guess: ")).lower()
		puzzleState.guess(theirGuess)
		if puzzleState.numWrongGuesses == 15 :
			print "LOSER! The right answer was OBVIOUSLY " + random.choice(puzzleState.word_list) + "!"
			print "Better luck next time!"
			break
		if '_' not in puzzleState.currentDisplay :
			print "Okay, that was an easy one. NEXT TIME you won't be so lucky."
			break
