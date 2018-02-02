from random import randrange

class Game:
    """
    An implementation of the code-guessing game, Mastermind. The object of the game is to guess a 4-digit
    code, with each digit in the range [1,4], within a specified amount of tries.
    This game is played by a user against the computer.
    """

    def __init__(self):
        """
        Setup for game start, initializes class variable for correct code, num_hints, the game_mode,
        num_guesses, a holder for the user's guess, and starts game_loop
        """

        self.code = -1
        self.num_hints = 0
        self.game_mode = "user"
        self.num_guesses = 8
        self.guess = None

        self.UI = UI()  # Initializes UI iterface
        self.game_loop()  # Starts game


    def game_loop(self):
        """
        Main loop for game operation.

        :return: nothing
        """
        input = ""

        while input != "quit":
            self.game_mode, self.num_guesses = self.UI.start_menu()  # Get user input on game mode and max number of guesses.
            result = self.play_game()  # Play game!
            input = self.UI.end_menu(result)

    def play_game(self):
        i=0

        while i <= self.num_guesses:
            # User Guesses
            if self.game_mode == "user_guess":
                input = self.UI.guess_menu()  # Get input from user to determine which operation to perform
                if input == "hint":
                    self.UI.hint(self.generate_hint(self.guess))  # Gives a hint using the user's most recent guess

                elif input == "quit":
                    return "lose"  # end while loop, and take user to end_menu()

                else:  # if the user guesses a code, return feedback to the user on correctness
                    self.guess = input
                    correct_pos, correct_num = self.code_analysis(self.guess)
                    if correct_pos == len(self.code):
                        return "win" # end while loop, and take user to end_menu()
                    else:
                        self.UI.feedback(correct_pos, correct_num)
                    i += 1

            # Computer Guesses
            elif self.game_mode == "computer_guess":
                guess = self.generate_guess()
                correct_pos, correct_num = self.code_analysis(guess)
                if correct_pos == len(self.code):
                    return "win"  # end while loop, and take user to end_menu()
                else:
                    self.UI.feedback(correct_pos, correct_num)
                i += 1
        return "lose"  # end while loop, and take user to end_menu()


    def code_analysis(self, guess):
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
        code = None
        for i in range(4):
            code += randrange(1, 4)

        return code

    def generate_hint(self, guess):
        """
        Gives the player a hint about the correct code. The method iterates over the user's most recent guess to determine
        if they have guessed a number that exists in the answer, and if so, returns the correct position of that number.

        If the user does not have a correct number in their guess, return a random correct number from the answer, and
        its position.

        :return: A correct number in the answer, and its position in the answer as ints.
        """
        for i, j in guess, self.code:
            if i in self.code:
                return i, self.code.find(i)  # returns the correct number and it's position in the answer
            else:
                index = randrange(1,4)
                return self.code[index], index  # returns a correct number and its position if the user doesn't have any correct numbers

    def generate_guess(self):
        """
        Generates a random(for now) code to guess what the correct code is.
        :return: the 4-digit code with each value in the range [1,4]
        """

        This is the guess generated by the computer,
        the UI is meant to get the guess from the user.
        while numbers!= guesses:
            # ask user to guess the 4 values
            guesses = [
                int(input("guess the first number:" )),
                int(input("guess the second number: ")),
                int(input("guess the third number: ")),
                int(input("guess the fourth number: "))
            ]

            num_guess +=1

    """
    I'll be thinking about anything else we may need to add to this, but for now, it's a good start.
    
    We may want to add test codes
    """

class UI:
    """
    A User Interface (UI) for the game Mastermind. Utilizes the console for text input/output, to be used for gameplay.
    """
    def __init__(self):
        """
        Initializes a class instance for use by the Game class.
        """
        self.game_mode = None               # "user guess" or "computer guess"
        self.user_generated_code = None     # in "computer guess" mode, the user creates the code
        self.user_guess = None              # in "user guess" mode, the user guesses the code
        self.code = None
        self.game = Game()
        
    def start_menu(self):
        """
        Display start menu text for user, prompt for input on game mode (computer or player),
        and max number of guesses.
        :return: the game mode as a string, and max number of guesses as an int.
        """
        welcome_message = "Welcome to MasterMind"
        introduction = "Introduction to this game (to be added)"
        print(welcome_message)
        print(introduction)
        
        game_mode = self.ask_user_for_game_mode()
        
        game_start_message = "You choose {} game mode! Game start!".format(self.game_mode)
        
        num_guesses = 8  # input the number of attempts allowed to guess the code

        return game_mode, num_guesses
    
    def ask_user_for_game_mode(self):
        """
        To initiating the game, ask the user for the game mode
        :return: nothing
        """
        while self.game_mode == None: 
            
            game_mode = input("Enter '1' for 'User Guess' mode, enter '2' for 'Computer Guess' mode: ") 
            
            if game_mode == "1":
                self.game_mode == "user_guess"  # These values should be returned, not set

            elif game_mode == "2":
                self.game_mode == "computer_guess"  # Return, don't set value

            else:
                print("Invalid input.")
        
    def guess_menu(self):
        """
        in the "user guess" mode,
        Display in-game options for user or the next code guess,
        including hint or quit options, and prompt for user's input.

        Input should check for correct exit/hint statements and valid guesses.

        :return: nothing
        """

        # This method should get user input and check that it is valid, then return that input.
        # Allow the method in Game to change what happens next.

        # Additionally, why is the user guess formatted as # # # #?
        # It will be easier to analyse and return input in the form ####.
        if self.game_mode == "user_guess":
            
            input_instruction = "Enter your guess as a four-digit number separated by space (i.e. 2 2 2 2).\n" \
                                "Or enter 'hint' for a hint.\n" \
                                "Or enter 'quit' to quit."
            print(input_instruction)
            instruction = input("Your input: ")
  
            if instruction == "hint":  # Should just return input, not call methods for hint(), endmenu(), etc
                self.hint()
            
            elif instruction == "quit":
                self.end_menu()
                   
            else:
                guess = self.game.validate(instruction)
                self.user_guess = guess
   
    def hint(self, hint):
        """
        In the "user guess" mode, the user can ask for a hint, then move to the next step (guess/hint/quit)
        :return: nothing
        """
        if self.game_mode == "user_guess":
            #hint = self.game.generate_hint()
            print("The hint is {}.".format(hint))
            #self.guess_menu()                       # ask for input again. Not sure if it works tho.....
                                                     # This loop operation should be handled in Game
    def user_generates_code(self):
        """
        In the "computer_guess" mode, ask the user to input the code and validate the code
        :return: nothing
        """
        if self.game_mode == "computer_guess":
            code = input("Enter the code as a four-digit number seperated by space (i.e. 2 2 2 2):")
            self.code = self.game.validate(code)  # Let Game class take care of validation
                                                  # and call user input again if needed.
            
    def feedback(self, num_correct_pos, num_correct):
        """
        Display computer feedback on user's code guess
        :return: nothing
        """

    def end_menu(self):
        """
        1. if the user chooses to quit the current game
        2. if the user gets the code
        3. if computer gets the code
       
        End the game
        Display Win/Loss and gameplay statistics
        Ask the user if he/she wants to start a new game
        :return: nothing
        """
        self.game_mode == None
        
        # display statistics
        
        start_a_new_game = input("Do you want to start a new game? Enter 'yes' to start or others to quit.")
        if start_a_new_game == 'yes':
            self.initialize_new_game()  # Return yes/no and let Game class restart itself
        else:
            print("Hope you had fun playing MasterMind. Bye.") # end completely
    
    def initialize_new_game(self):  # Unnecessary method, is covered by game_loop method in Game
        """
        Restart the game if the user chooses to start a new game
        :return: nothing
        """
        self.__init__()
        self.start_menu()

game = Game()  # Creates a game instance, and starts play

