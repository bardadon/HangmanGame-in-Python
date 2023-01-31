import pytest
from main.hangman import Hangman
import os

# Setting the work directory
path = '/projects/tdd_linkedin'
os.chdir(path)

class TestHangman:  

    def test_CountLettersInAWord(self):
        word = 'hello'
        letter = 'l'
        hangman = Hangman()
        result = hangman.count_letters(word, letter)

        assert result == 2

    def test_CollectWordsOfSizeX(self):

        hangman = Hangman()
        word_size = 5
        fileLocation='main/test.txt'

        hangman.collect_words(fileLocation, word_size)

        with open('main/fetched_words.txt', 'r') as read_file:
            assert 'hello' in read_file.read()

    def test_GenerateRandomSize(self):
        hangman = Hangman()
        result_size = hangman.generate_size()
        assert result_size >= 5


    def test_GrabThreeUniqueWords(self):

        hangman = Hangman()
        word_size = hangman.generate_size()
        fileLocation='main/test.txt'

        # Generate words
        hangman.collect_words(fileLocation, word_size)

        # Grab unique word
        unique_word1 = hangman.fetch_unique_word()
        unique_word2 = hangman.fetch_unique_word()
        unique_word3 = hangman.fetch_unique_word()
        assert unique_word1 == 'hello'
        assert unique_word2 == 'asdvf'
        assert unique_word3 == 'dsacv' 

    def test_generate_clue(self):

        hangman = Hangman()
        word_size = hangman.generate_size()
        fileLocation='main/test.txt'

        # Generate words
        hangman.collect_words(fileLocation, word_size)
        unique_word = 'hello'

        # Generate clue
        result_clue = hangman.generate_clue(unique_word)
        assert result_clue == '_ _ _ _ _'

    def test_user_turn(self):

        hangman = Hangman()
        word_size = hangman.generate_size()
        fileLocation='main/test.txt'

        # Generate words
        hangman.collect_words(fileLocation, word_size)

        # Generate clue, solution and user_input
        solution = 'hello'
        clue = hangman.generate_clue(solution)
        user_input = 'h'
        updated_clue = hangman.update_clue(clue=clue, solution=solution, user_input= user_input)

        assert updated_clue == 'h _ _ _ _'

    def test_raiseExceptionUserInputOnlyStrings_EnteringString(self, monkeypatch):

        hangman = Hangman()

        # Use monkeypath to "select" the input: h
        monkeypatch.setattr('builtins.input', lambda _: "h")
        user_input = hangman.get_user_input()

        assert isinstance(user_input, str)

    def test_raiseExceptionUserInputOnlyStrings_EnteringInt(self, monkeypatch):

        hangman = Hangman()

        # Use monkeypath to "select" the input: h
        monkeypatch.setattr('builtins.input', lambda _: 50)
        
        with pytest.raises(TypeError, match='Please enter a string') as exception:
            user_input = hangman.get_user_input()

        assert exception.type == TypeError
        assert exception.value.args[0] == 'Please enter a string'


    # 1. Each correct letter gussed is worth 10 points
    def test_CorrectAnswerWorth10Points(self, monkeypatch):

        hangman = Hangman()

        # Users start with score = 0 
        assert hangman.score == 0

        # Generate words
        word_size = hangman.generate_size()
        fileLocation='main/test.txt'
        hangman.collect_words(fileLocation, word_size)

        # Generate clue, solution 
        solution = 'hello'
        clue = hangman.generate_clue(solution)

        # Simulate user input using monkeypatch
        monkeypatch.setattr('builtins.input', lambda _: 'h')
        user_input = hangman.get_user_input()

        # Guess a correct letter
        updated_clue = hangman.update_clue(clue=clue, solution=solution, user_input= user_input)
        assert hangman.score == 10

    # 2. Users have 10 trials to guess the letters
    def test_RemainingTrials(self, monkeypatch):

        hangman = Hangman()

        # Users start with 10 trials 
        assert hangman.remaining_trials == 10

        # Generate words
        word_size = hangman.generate_size()
        fileLocation='main/test.txt'
        hangman.collect_words(fileLocation, word_size)

        # Generate clue, solution 
        solution = 'hello'
        clue = hangman.generate_clue(solution)

        # Simulate user input using monkeypatch
        monkeypatch.setattr('builtins.input', lambda _: 'h')
        user_input = hangman.get_user_input()

        # Guess a correct letter
        updated_clue = hangman.update_clue(clue=clue, solution=solution, user_input= user_input)
        assert hangman.remaining_trials == 9


    # let a player guess letters until they either get it right or run out of remining trials
    def test_gameFlow_GuessingAllLetters_Winning(self, monkeypatch):

        hangman = Hangman()

        # Generate words
        word_size = hangman.generate_size()
        fileLocation='main/test.txt'
        hangman.collect_words(fileLocation, word_size)

        # Generate clue, solution 
        solution = 'hello'
        clue = hangman.generate_clue(solution)

        # Simulate user input using monkeypatch
        monkeypatch.setattr('builtins.input', lambda _: 'h')
        monkeypatch.setattr('builtins.input', lambda _: 'e')
        monkeypatch.setattr('builtins.input', lambda _: 'l')
        monkeypatch.setattr('builtins.input', lambda _: 'l')
        monkeypatch.setattr('builtins.input', lambda _: 'o')
        hangman.playGame()

        assert self.score == 50



    #def test_gameFlow_GuessingFinishingRemainingTrials_Losing(self):
     #   pass