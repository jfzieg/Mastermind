
import random
from random import randrange

class Game:
    """
    An implementation of the code-guessing game, Mastermind. The object of the game is to guess a 4-digit
    code, with each digit in the range [1,4], within a specified amount of tries.
    This game is played by a user against the computer.
    """

    def __init__(self, code=-1, num_hints=0, computer_guess=-1, game_mode="user", num_guesses=8):

        """
        Setup for game start, initializes class variable for correct code, and starts game_loop
        :param code: The correct code to be guessed by either the user or the computer. Must be a 4-digit int with each
        digit in the range [1,4] inclusive
        :param num_hints: The number of hints the user has asked for.
        :param computer_guess: The variable to be used if the computer is guessing the code.
        """

        self.game_loop()
        self.UI = UI()
        

    def game_loop(self):

    
        """
        Main loop for game operation.
        :return: nothing
        """
        self.UI.start_menu()  # Display start menu to player and get player input on game mode and number of guesses
        self.game_mode, self.num_guesses = self.UI.start_menu()

    def code_anaylsis(self, guess):
        """
        Analyses the code to return feedback for the computer or player,
        so that they can make a new educated guess on what the code is.
        Does not test for correct guess format.
        :param guess: int input of a code guess to be evaluated against the correct code.
        :return: int values for the correct values in the correct position (correct_pos),
        and the number of correct values in the guess (correct_num) , mutually exclusive.
        """
        correct_pos = 0
        correct_num = 0
        
        for i, j in guess, self.code:  # Loop over each digit in the guess and the code
            if i == j:  # Test to find a correct digit in the correct place
                    correct_pos += 1
            if i in self.code:  # Test to find a digit in the guess in the correct code
                correct_num += 1
        correct_num -= correct_pos  # Done to eliminate the overlap of digits that are correct and in correct position

        return correct_pos, correct_num

    def generate_code(self):
        
        """
        Generates a random, 4-digit code with each value in the range [1,4]
        :return: the randomly generated code.
        """
        for x in range(4):
            print random.randint(1,4)
            
        return self.generate_code

    def generate_hint(self):

        """
        Gives the player a hint about the correct code
        :return:
        """
        
        for i range(4):
            if self.guess !=self.code:
                print("Do you wanna a hint?")
                        

    def generate_guess(self):

        random_number == randrange(1,4)
        print random_number()
        count = 0
        while count <4:
            if self.guess == random_number():
                print("Your win")

        else:
            print "You lose"
        
            
        """
        Generates a random(for now) code to guess what the correct code is.
        :return: the 4-digit code with each value in the range [1,4]
        """
               
                                 
    """
    I'll be thinking about anything else we may need to add to this, but for now, it's a good start.
    
    We may want to add test codes
    """
    
    def validate(self, input):
        
        """
        Validate either the code or the guess from the user's input.
        It should be a four-digit integer seperated by space.
        :return: a list of each digit as a string (i.e ["1","2","3","4"])
        """
        if self.generate_code == input:
            print("You guessed correctly")
            
        else self.generate_code!= input:
            print("You guessed wrongly" )
        
        return self.game
        
