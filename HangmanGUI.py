# Image sources - flickr.com (modified), commons.wikimedia.org (modified)
# Dictionary source - www01.sil.org

import pygame, sys, hangmanFunctions
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 800
WINDOWHEIGHT = 600

# Constants for the main menu screen GUI
MAINMENU_ELEMENTS = [pygame.image.load("title.png"), pygame.image.load("button-play.png"), pygame.image.load("button-instructions.png"), pygame.image.load("button-highscores.png"), pygame.image.load("button-quit.png")]
MAINMENU_INDEXTOELEMENTS = {"0":"play", "1":"instructions", "2":"highscores", "3":"quit"}
MAINMENU_HOVERELEMENTS = [pygame.image.load("button-play-hover.png"), pygame.image.load("button-instructions-hover.png"), pygame.image.load("button-highscores-hover.png"), pygame.image.load("button-quit-hover.png")]
MAINMENU_ELEMENTWIDTH = 275
MAINMENU_ELEMENTHEIGHT = 66
MAINMENU_RECTWIDTH = MAINMENU_ELEMENTWIDTH
MAINMENU_RECTHEIGHT = WINDOWHEIGHT/len(MAINMENU_ELEMENTS)
MAINMENU_XMARGIN = (WINDOWWIDTH - MAINMENU_RECTWIDTH)/2
MAINMENU_YMARGIN = (WINDOWHEIGHT - MAINMENU_RECTHEIGHT * len(MAINMENU_ELEMENTS))/2
MENURECT_XMARGIN = (MAINMENU_RECTWIDTH - MAINMENU_ELEMENTWIDTH)/2
MENURECT_YMARGIN = (MAINMENU_RECTHEIGHT - MAINMENU_ELEMENTHEIGHT)/2

INSTRUCTIONS_BOX = pygame.image.load("instructions-box.png")

BACK_BTN = pygame.image.load("button-back.png")
BACK_BTNHOVER = pygame.image.load("button-back-hover.png")

HIGHSCORES_BOX = pygame.image.load("highscores-box.png")
HIGHSCORES_BOXWIDTH = 440
HIGHSCORES_BOXHEIGHT = 440
HIGHSCORES_SCORETOIMAGE = {"0":pygame.image.load("0-score.png"), "1":pygame.image.load("1-score.png"), "2":pygame.image.load("2-score.png"), "3":pygame.image.load("3-score.png"), "4":pygame.image.load("4-score.png"), "5":pygame.image.load("5-score.png"), "6":pygame.image.load("6-score.png")}
# Distance of high score box from left edge of screen and top of screen
HIGHSCORES_BOX_X_DISTANCE = (WINDOWWIDTH - HIGHSCORES_BOXWIDTH)/2
HIGHSCORES_BOX_Y_DISTANCE = (WINDOWHEIGHT - HIGHSCORES_BOXHEIGHT)/2
# Width and height of scores in high score box
HIGHSCORES_SCOREWIDTH = 20
HIGHSCORES_SCOREHEIGHT = 25
# Top number's distance from x margin and y margin in the high scores box
HIGHSCORES_X_MARGIN = 34
HIGHSCORES_Y_MARGIN = 19
# Distance between the numbers in the high scores box
HIGHSCORES_GAPHEIGHT = 16

ALPHABET = list("abcdefghijklmnopqrstuvwxyz")
GAME_KEYPRESSEDTOLETTER = {K_a:"a", K_b:"b", K_c:"c", K_d:"d", K_e:"e", K_f:"f", K_g:"g", K_h:"h", K_i:"i", K_j:"j", K_k:"k", K_l:"l", K_m:"m", K_n:"n", K_o:"o", K_p:"p", K_q:"q", K_r:"r", K_s:"s", K_t:"t", K_u:"u", K_v:"v", K_w:"w", K_x:"x", K_y:"y", K_z:"z"}
GAME_WRONGGUESSESTOIMAGE = {"0":pygame.image.load("graphic-blank.png"), "1":pygame.image.load("graphic-post.png"), "2":pygame.image.load("graphic-head.png"), "3":pygame.image.load("graphic-torso.png"), "4":pygame.image.load("graphic-leftarm.png"), "5":pygame.image.load("graphic-rightarm.png"), "6":pygame.image.load("graphic-leftleg.png"), "7":pygame.image.load("graphic-rightleg.png")}
GAME_LETTERIMAGES = {}
for letter in ALPHABET:
	fileName = letter.upper() + "-letter.png"
	GAME_LETTERIMAGES[letter] = pygame.image.load(fileName)
GAME_LETTERIMAGEWIDTH = 100
GAME_LETTERIMAGEHEIGHT = 100
GAME_BLANKIMAGE = pygame.image.load("blank.png")
GAME_BLANKIMAGEWIDTH = 100
GAME_BLANKIMAGEHEIGHT = 100
GAME_LETTERBOXWIDTH = 500
GAME_LETTERBOXHEIGHT = 400
GAME_LETTERBOXCOLOR = (0, 20, 255) # blue

MAXWRONGGUESSES = 7

FONTCOLOR = (0, 0, 0) # black
FONTRECTCOLOR = (55, 160, 170) # light blue

def main():
	global DISPLAYSURF, FPSCLOCK, FONTOBJ
	pygame.init()

	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	FONTOBJ = pygame.font.Font("freesansbold.ttf", 40)
    
	pygame.display.set_caption("Hangman")
	pygame.display.set_icon(pygame.image.load("gameicon.png"))
    
	mainMenu()


def mainMenu():
	'''The main menu of the game, with the title and buttons leading to different screens'''

	mousex = None
	mousey = None

	while True:
		mouseClicked = False

		drawBackground()
		guiRect = pygame.Rect(MAINMENU_XMARGIN, MAINMENU_YMARGIN, MAINMENU_RECTWIDTH, MAINMENU_RECTHEIGHT)

		for element in MAINMENU_ELEMENTS:
			DISPLAYSURF.blit(element, guiRect)
			guiRect.top += MAINMENU_RECTHEIGHT

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEMOTION:
				mousex, mousey = event.pos
			elif event.type == MOUSEBUTTONUP:
				mousex, mousey = event.pos
				mouseClicked = True

		if mousex != None and mousey != None:
			guiBtnIndex, btnRect = getMainMenuBtnAtPixel(mousex, mousey)
			if guiBtnIndex != None:
				DISPLAYSURF.blit(MAINMENU_HOVERELEMENTS[guiBtnIndex], btnRect)
				if mouseClicked:
					screenIndex = str(guiBtnIndex)
					if MAINMENU_INDEXTOELEMENTS[screenIndex] == "play":
						gameScreen()
					elif MAINMENU_INDEXTOELEMENTS[screenIndex] == "instructions":
						instructionsScreen()
					elif MAINMENU_INDEXTOELEMENTS[screenIndex] == "highscores":
						highScoresScreen()
					elif MAINMENU_INDEXTOELEMENTS[screenIndex] == "quit":
						pygame.quit()
						sys.exit()

		pygame.display.update()
		FPSCLOCK.tick(FPS)


def gameScreen():
	'''The screen for playing the game itself'''

	backBtnRect = BACK_BTN.get_rect()
	backBtnRect.topright = (WINDOWWIDTH, 0)

	mousex = None
	mousey = None

	incorrectGuesses = 0
	guessedLetters = []
	letterPressed = None
	highScore = False
	
	gameWon = False
	gameLost = False

	word = list(hangmanFunctions.getComputerWord())
	wordLength = len(word)
	wordSoFar = []
	for space in range(wordLength):
		wordSoFar.append("")
	while True:
		mouseClicked = False

		drawBackground()
		DISPLAYSURF.blit(BACK_BTN, backBtnRect)
		drawBlanks(wordLength)
		drawLetters(wordSoFar)
		drawHangman(incorrectGuesses)
		drawLetterBox(guessedLetters)

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEMOTION:
				mousex, mousey = event.pos
			elif event.type == MOUSEBUTTONUP:
				mousex, mousey = event.pos
				mouseClicked = True
			elif event.type == KEYUP and not gameWon and not gameLost:
				if event.key in GAME_KEYPRESSEDTOLETTER:
					letterPressed = GAME_KEYPRESSEDTOLETTER[event.key]
					if letterPressed in guessedLetters:
						letterPressed = None

		if mousex != None and mousey != None:
			if backBtnRect.collidepoint(mousex, mousey):
				DISPLAYSURF.blit(BACK_BTNHOVER, backBtnRect)
				if mouseClicked:
					mainMenu()

		if letterPressed:
			guessedLetters.append(letterPressed)
			guessedLetters.sort()
			if hangmanFunctions.isGuessCorrect(word, letterPressed):
				letterIndex = 0
				for letter in word:
					if letter == letterPressed:
						wordSoFar[letterIndex] = letterPressed
					letterIndex += 1
			else:
				incorrectGuesses += 1
			letterPressed = None

		if not gameWon and not gameLost and hangmanFunctions.isWordFound(word, wordSoFar):
			gameWon = True
			scoreLocation = hangmanFunctions.getLocationInHighScores(incorrectGuesses)
			if scoreLocation != None:
				newScores = hangmanFunctions.loadHighScores()
				newScores[scoreLocation] = str(incorrectGuesses)
				hangmanFunctions.saveHighScores(newScores)
		elif not gameWon and not gameLost and incorrectGuesses >= MAXWRONGGUESSES:
			gameLost = True
			wordSoFar = word

		if gameWon:
			drawWinMsg(scoreLocation)
		elif gameLost:
			drawLoseMsg()

		pygame.display.update()
		FPSCLOCK.tick(FPS)


def drawWinMsg(highScore):
	winMsg = "Congratulations, you won!"
	msgSurface = FONTOBJ.render(winMsg, True, FONTCOLOR, FONTRECTCOLOR)
	msgRect = msgSurface.get_rect()
	msgRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
	DISPLAYSURF.blit(msgSurface, msgRect)


def drawLoseMsg():
	loseMsg = "Sorry, you lost!"
	msgSurface = FONTOBJ.render(loseMsg, True, FONTCOLOR, FONTRECTCOLOR)
	msgRect = msgSurface.get_rect()
	msgRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
	DISPLAYSURF.blit(msgSurface, msgRect)

def drawBlanks(wordLength):
	blankLeft = 0
	blankBottom = WINDOWHEIGHT
	for blank in range(wordLength):
		blankRect = pygame.Rect(0, 0, GAME_BLANKIMAGEWIDTH, GAME_BLANKIMAGEHEIGHT)
		blankRect.bottomleft = (blankLeft, blankBottom)
		DISPLAYSURF.blit(GAME_BLANKIMAGE, blankRect)
		blankLeft += GAME_BLANKIMAGEWIDTH


def drawLetters(wordSoFar):
	letterLeft = 0
	letterBottom = WINDOWHEIGHT - 15
	for letter in wordSoFar:
		if letter != "":
			letterRect = pygame.Rect(0, 0, GAME_LETTERIMAGEWIDTH, GAME_LETTERIMAGEHEIGHT)
			letterRect.bottomleft = (letterLeft, letterBottom)
			DISPLAYSURF.blit(GAME_LETTERIMAGES[letter], letterRect)
		letterLeft += GAME_LETTERIMAGEWIDTH


def drawHangman(incorrectGuesses):
	hangmanImage = GAME_WRONGGUESSESTOIMAGE[str(incorrectGuesses)]
	DISPLAYSURF.blit(hangmanImage, (60, 60))


def drawLetterBox(guessedLetters):
	pygame.draw.rect(DISPLAYSURF, GAME_LETTERBOXCOLOR, (WINDOWWIDTH - GAME_LETTERBOXWIDTH, 70, GAME_LETTERBOXWIDTH, GAME_LETTERBOXHEIGHT), 5)
	startingLeft = WINDOWWIDTH - GAME_LETTERBOXWIDTH + 5
	startingTop = 70 + 5
	for letter in guessedLetters:
		DISPLAYSURF.blit(GAME_LETTERIMAGES[letter], (startingLeft, startingTop))
		if startingLeft + GAME_LETTERIMAGEWIDTH > WINDOWWIDTH:
			startingLeft = WINDOWWIDTH - GAME_LETTERBOXWIDTH + 5
			startingTop += GAME_LETTERIMAGEHEIGHT
		else:
			startingLeft += GAME_LETTERIMAGEHEIGHT


def instructionsScreen():
	'''The screen displaying the instructions for how to play the game'''

	instructionsRect = INSTRUCTIONS_BOX.get_rect()
	instructionsRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
	backBtnRect = BACK_BTN.get_rect()
	backBtnRect.topright = (WINDOWWIDTH, 0)

	mousex = None
	mousey = None

	while True:
		mouseClicked = False

		drawBackground()
		DISPLAYSURF.blit(INSTRUCTIONS_BOX, instructionsRect)
		DISPLAYSURF.blit(BACK_BTN, backBtnRect)

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEMOTION:
				mousex, mousey = event.pos
			elif event.type == MOUSEBUTTONUP:
				mousex, mousey = event.pos
				mouseClicked = True

		if mousex != None and mousey != None:
			if backBtnRect.collidepoint(mousex, mousey):
				DISPLAYSURF.blit(BACK_BTNHOVER, backBtnRect)
				if mouseClicked:
					mainMenu()

		pygame.display.update()
		FPSCLOCK.tick(FPS)


def highScoresScreen():
	'''Display the high scores of human players'''

	mousex = None
	mousey = None
	highScoresDict = hangmanFunctions.loadHighScores()

	highScoresRect = HIGHSCORES_BOX.get_rect()
	highScoresRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
	backBtnRect = BACK_BTN.get_rect()
	backBtnRect.topright = (WINDOWWIDTH, 0)
	
	while True:
		mouseClicked = False

		drawBackground()
		DISPLAYSURF.blit(HIGHSCORES_BOX, highScoresRect)
		DISPLAYSURF.blit(BACK_BTN, backBtnRect)

		scoreRectRight = HIGHSCORES_BOX_X_DISTANCE + HIGHSCORES_BOXWIDTH - HIGHSCORES_X_MARGIN
		scoreRectTop = HIGHSCORES_BOX_Y_DISTANCE + HIGHSCORES_Y_MARGIN
		scoreRect = pygame.Rect(scoreRectRight, scoreRectTop, HIGHSCORES_SCOREWIDTH, HIGHSCORES_SCOREHEIGHT)

		for scoreRank in range(10):
			score = highScoresDict[scoreRank]
			if int(score) < MAXWRONGGUESSES:
				scoreImage = HIGHSCORES_SCORETOIMAGE[score]
				DISPLAYSURF.blit(scoreImage, scoreRect)
			scoreRect.y += HIGHSCORES_SCOREHEIGHT + HIGHSCORES_GAPHEIGHT

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEMOTION:
				mousex, mousey = event.pos
			elif event.type == MOUSEBUTTONUP:
				mousex, mousey = event.pos
				mouseClicked = True

		if mousex != None and mousey != None:
			if backBtnRect.collidepoint(mousex, mousey):
				DISPLAYSURF.blit(BACK_BTNHOVER, backBtnRect)
				if mouseClicked:
					mainMenu()

		pygame.display.update()
		FPSCLOCK.tick(FPS)


def drawBackground():
	'''Draw the background image to the screen'''

	BGIMAGE = pygame.image.load("background.png")
	bgRect = BGIMAGE.get_rect()
	DISPLAYSURF.blit(BGIMAGE, bgRect)


def getMainMenuBtnAtPixel(x, y):
	'''Get the button from the main menu screen that the player's mouse is colliding with'''

	# Go through all the main menu GUI elements not including the title (leaving only the buttons)
	for guiBtnIndex in range(1, len(MAINMENU_ELEMENTS)):
		# Get the x and y coordinates of the rectangle surrounding the button
		elementRectX = MAINMENU_XMARGIN
		elementRectY = MAINMENU_YMARGIN + guiBtnIndex * MAINMENU_RECTHEIGHT
		# Get the x and y coordinates of the button
		btnRectX = elementRectX + MENURECT_XMARGIN
		btnRectY = elementRectY + MENURECT_YMARGIN
		btnRect = pygame.Rect(elementRectX, elementRectY, MAINMENU_ELEMENTWIDTH, MAINMENU_ELEMENTHEIGHT)

		if btnRect.collidepoint(x, y):
			# Subtract one from the guiBtnIndex so that the title element isn't included
			return guiBtnIndex-1, btnRect
	return None, None


if __name__ == "__main__":
	main()
