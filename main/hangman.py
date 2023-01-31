import os
import random

# Setting the work directory
path = '/projects/tdd_linkedin'
os.chdir(path)

class Hangman():

    fetched_words = []

    def __init__(self, score: int = 0, remaining_trials: int = 10) -> None:
        self.score = score
        self.remaining_trials = remaining_trials

    def count_letters(self, word, letter):
        self.word = word
        self.letter = letter

        # Count apperances in a dictionary
        letters = dict()
        for i in word:
            letters[i] = letters.get(i, 0) + 1

        return letters.get(letter)

    def collect_words(self, fileLocation, word_size):

        self.fileLocation = fileLocation
        self.word_size = word_size

        print(f'Fetching words of size: {word_size}')
        with open(fileLocation, 'r') as read_file:

            while True:
                # Read the file line by line
                line = read_file.readline()
                words_inLine = line.split()

                # Iterate over the words of each line
                # Return the first word that matches
                with open('main/fetched_words.txt', 'r') as read_file2:

                    for word in words_inLine:
                        if len(word) == word_size and word not in read_file2.read():
                            with open('main/fetched_words.txt', 'a') as write_file:
                                write_file.write(word+'\n')
                                write_file.close()

                    read_file2.close()
                            
                # If EOF, exit the loop
                if line == '':
                    break

            read_file.close()

    def generate_size(self):
        return random.randint(5, 10)

    def fetch_unique_word(self):

        # Return words from text file
        with open('main/fetched_words.txt', 'r') as read_file:
            words = read_file.read().split()

            # Verify that these words are unique
            # unique words are words that are not in self.fetched_words
            for word in words:
                if word not in self.fetched_words:
                    self.fetched_words.append(word)
                    return word

    def generate_clue(self, solution):

        self.solution = solution

        clue =  '_ ' * len(solution)
        clue = clue[0:-1]
        return clue

    def cleanUp(self):

        with open('main/fetched_words.txt', 'w') as write_file:
            write_file.write('')
            write_file.close()


    def get_user_input(self):
        self.cleanUp()
        user_input = input('Guess a letter...')
        if isinstance(user_input, str) == False:
            raise TypeError('Please enter a string')
        else:
            return user_input

    def calculate_appearances(self, user_input, clue):

        input_counter = 0
        for i in clue:
            if user_input in clue:
                input_counter += 1
        return input_counter
        
    def calculate_score(self, solution, clue):

        score = 0
        for i in zip(solution, clue):
            if '_' not in i and ' ' not in i:
                score += 10

        self.score = score


    def update_clue(self, clue: str, solution: str, user_input: str) -> str:

        self.clue = clue
        self.solution = solution
        self.user_input = user_input
        
        skip_index = 0
        # Case #1 - User input is correct
        if user_input in solution:

            if user_input in clue:
                skip_index = solution.index(user_input, skip_index) + 1
            else:
                skip_index = 0

            input_index = solution.index(user_input, skip_index) # Grab the index
            # Replace the underscore in the clue with the user input
            clue_list = clue.split()
            clue_list[input_index] = user_input
            clue = ' '.join(clue_list[0:input_index+1]) + ' ' + ' '.join(clue_list[input_index+1:]) 

            # Update user score and remaining trials
            current_score = self.score
            self.calculate_score(clue, solution)
            self.remaining_trials -= 1

            if self.score > current_score:
                print('Correct. You gained 10 points!')
            else:
                print('Letter Already exists!')

        # Case #3 - User is wrong
        else:

            # Store the input in a file
            with open('main/user_choices', 'a') as write_file:
                write_file.write(user_input)
                write_file.close()
            
            # Update remining trials
            self.remaining_trials -= 1
            print(f'Wrong. You have {self.remaining_trials} Trials Remaining.')
            
        return clue

    def playGame(self):

        # Generate words
        word_size = self.generate_size()
        fileLocation='main/test.txt'
        self.collect_words(fileLocation, word_size)

        # Generate solution, clue
        solution = self.fetch_unique_word()
        print(solution)
        clue = self.generate_clue(solution=solution)

        # First Round
        print(clue)
        user_input = self.get_user_input()
        new_clue = self.update_clue(clue=clue, solution=solution, user_input=user_input)

        # Play till the end
        while self.remaining_trials > 0 or self.score < 10*word_size:
            print(new_clue)
            user_input = self.get_user_input()
            new_clue = self.update_clue(clue=new_clue, solution=solution, user_input=user_input)
            
        # Clean up
        self.cleanUp()


        
def main():

    hangman = Hangman()
    
    hangman.playGame()


if __name__ == '__main__':
    main()