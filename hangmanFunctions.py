import random

def loadDict():
	'''Open an english dictionary file and create a list of all the words in it'''
	
	dictFile = open("dictionary.txt")
	words = []
	for word in dictFile.read().split("\n"):
		if word != "" and len(word) < 9:
			words.append(word.lower())
	dictFile.close()
	return words

ENGLISH_WORDS = loadDict()

def loadHighScores():
	'''Open a high scores top ten file and create a dictionary of the scores in it'''

	highScoreFile = open("HighScores.txt")
	scores = {}
	contents = highScoreFile.read().split("\n")
	# scores dict has each score's location in the list as the key and the score itself as the value
	for line in range(10):
		scores[line] = contents[line]
	highScoreFile.close()
	return scores


def saveHighScores(newFileLines):
	'''Open a high scores top ten file and write the new high scores to it'''

	highScoreFile = open("HighScores.txt", "w")
	scores = []
	for value in sorted(newFileLines.values()):
		scores.append(str(value) + "\n")
	scores = scores[0:10]
	scores[-1] = scores[-1][:-1]
	highScoreFile.writelines(scores[0:10])
	highScoreFile.close()


def getLocationInHighScores(newScore):
	'''Get a score's location in the top ten'''

	highScores = loadHighScores()
	for pos, score in sorted(highScores.items()):
		# Check if the new score is better than a score in the list
		if newScore < int(score):
			return pos
	# The given score isn't greater than any of the scores in the file, return None
	return None


def isWordFound(completeWord, wordSoFar):
	'''Check if the guesser has found the correct word'''

	if completeWord == wordSoFar:
		return True


def isGuessCorrect(completeWord, letter):
	'''Check if a certain letter is in the word.'''
	return letter in completeWord


def getComputerWord():
	'''Returns random English word'''

	return random.choice(ENGLISH_WORDS)
