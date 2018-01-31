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

    def generate_hint(self):
        """
        Gives the player a hint about the correct code

        :return:
        """

    def generate_guess(self):
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
        
        game_start_message = "You choose {} game mode! Game start!".format(game_mode)
        
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
                self.game_mode == "user_guess"

            elif game_mode == "2":
                self.game_mode == "computer_guess"

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
        if self.game_mode == "user_guess":
            
            input_instruction = "Enter your guess as a four-digit number seperated by space (i.e. 2 2 2 2)." + 
                                "Or enter 'hint' for a hint." + 
                                "Or enter 'quit' to quit."
            print(input_instruction)
            instruction = input("Your input: ")
  
            if instruction == "hint":
                self.hint()
            
            elif instruction == "quit":
                self.end_menu()
                   
            else:
                guess = self.game.validate(instruction)
                self.user_guess = guess
   
    def hint(self):
        """
        In the "user guess" mode, the user can ask for a hint, then move to the next step (guess/hint/quit)
        :return: nothing
        """
        if self.game_mode == "user_guess":
            hint = self.game.generate_hint()
            print("The hint is {}.".format(hint))
            self.guess_menu()                       # ask for input again. Not sure if it works tho.....
        
    def user_generates_code(self):
        """
        In the "computer_guess" mode, ask the user to input the code and validate the code
        :return: nothing
        """
        if self.game_mode == "computer_guess":
            code = input("Enter the code as a four-digit number seperated by space (i.e. 2 2 2 2):")
            self.code = self.game.validate(code)
            
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
            self.initialize_new_game()
        else:
            print("Hope you had fun playing MasterMind. Bye.") # end completely
    
    def initialize_new_game(self):
        """
        Restart the game if the user chooses to start a new game
        :return: nothing
        """
        self.__init__()
        self.start_menu()

game = Game()  # Creates a game instance, and starts play
