import cx_Freeze

executables = [cx_Freeze.Executable("HangmanGUI.py")]

cx_Freeze.setup(
    name="Hangman program",
    options={"build_exe": {"packages":["pygame", "sys"],
                           "include_files":["0-score.png", "1-score.png", "2-score.png", "3-score.png", "4-score.png", "5-score.png", "6-score.png", "A-letter.png", "background.png", "blank.png", "B-letter.png", "button-back.png", "button-back-hover.png", "button-highscores.png", "button-highscores-hover.png", "button-instructions.png", "button-instructions-hover.png", "button-play.png", "button-play-hover.png", "button-quit.png", "button-quit-hover.png", "C-letter.png", "dictionary.txt", "D-letter.png", "E-letter.png", "F-letter.png", "gameicon.png", "G-letter.png", "graphic-blank.png", "graphic-head.png", "graphic-leftarm.png", "graphic-leftleg.png", "graphic-post.png", "graphic-rightarm.png", "graphic-rightleg.png", "graphic-torso.png", "hangmanFunctions.py", "HighScores.txt", "highscores-box.png", "H-letter.png", "I-letter.png", "instructions-box.png", "J-letter.png", "K-lettter.png", "L-letter.png", "M-letter.png", "N-letter.png", "O-letter.png", "P-letter.png", "Q-letter.png", "R-letter.png", "S-letter.png", "title.png", "T-letter.png", "U-letter.png", "V-letter.png", "W-letter.png", "X-letter.png", "Y-letter.png", "Z-letter.png"]}},
    executables = executables

    )
