from random import randrange

class Game:
    """
    An implementation of the code-guessing game, Mastermind. The object of the game is to guess a 4-digit
    code, with each digit in the range [1,6], within a specified amount of tries.
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
            code += randrange(1, 6)

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

        # This is the guess generated by the computer,
        # the UI is meant to get the guess from the user.
        # while numbers!= guesses:
        #     # ask user to guess the 4 values
        #     guesses = [
        #         int(input("guess the first number:" )),
        #         int(input("guess the second number: ")),
        #         int(input("guess the third number: ")),
        #         int(input("guess the fourth number: "))
        #     ]
        #
        #     num_guess +=1

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

        :return: the game mode (user_guess/computer_guess)
        """
        valid_input = False

        while valid_input == False:
            
            game_mode = input("Enter '1' for 'User Guess' mode, enter '2' for 'Computer Guess' mode: ") 
            
            if game_mode == "1":
                valid_input == True
                return "user_guess"  # These values should be returned, not set

            elif game_mode == "2":
                valid_input == True
                return == "computer_guess"  # Return, don't set value

            else:
                print("Invalid input.")
        
    def guess_menu(self):
        """
        Display in-game options for user or the next code guess,
        including hint or quit options, and prompt for user's input.

        Input should check for correct exit/hint statements and valid guesses.

        :return: valid guess or instruction (hint/quit)
        """
        input_instruction = "Enter your guess as a four-digit number separated by space (i.e. 2 2 2 2).\n"
                            "Or enter 'hint' for a hint.\n"
                            "Or enter 'quit' to quit."
        valid_input = False

        while valid_input == False:

            print(input_instruction)
            instruction = input("Your input: ")

            if instruction == "hint":
                valid_input == True
            
            elif instruction == "quit":
                valid_input == True
                   
            else:
                valid_input = self.validate(instruction)

        return instruction

   
    def hint(self, hint):
        """
        Display the hint

        :return: nothing
        """

        print("The hint is: ", hint)

    def user_generates_code(self):
        """
        In the "computer_guess" mode, ask the user to input the code and validate the code

        :return: the user generated code
        """
        valid_input = False

        while valid_input == False:
            code = input("Enter the code as a four-digit number seperated by space (i.e. 2 2 2 2):")
            valid_input == self.validate(code)

        return code
            

    def feedback(self, num_correct_pos, num_correct):
        """
        Display computer feedback on user's code guess

        :return: nothing
        """
        print("The number of the correct positions is {}.".format(num_correct_pos))
        print("The number of the correct numbers is {}.".format(num_correct))


    def end_menu(self):
        """
        End the game
        Display Win/Loss and gameplay statistics

        :return: boolean, "True" for starting a new game, "False" for leaving this game
        """
        
        file = open(“statistics.txt”, “r”)
        statistics = file.readlines()
        print("The number of wins is: ", statistics[0])
        print("The number of loses is: ", statistics[1])
        print("The numebr of guesses is: ", statistics[2])
        
        start_a_new_game = input("Do you want to start a new game? Enter 'yes' to start or others to quit.")
        if start_a_new_game == 'yes':
            return True
        else:
            return False
    

     def validate(self, input):
        """
        Validate either the code or the guess from the user's input.
        It should be a four-digit integer separated by space.

        :return: boolean, "True" for validated input, "False" for invalidated input
        """

        output = input.split()
        valid_digit = ["1", "2", "3", "4", "5", "6"]

        if len(output) != 4:
            print("Invalid input.")
            return False

        elif for e in output:
            if e not in valid_digit:
                print("Invalid input.")
                return False
        else:
            return True

game = Game()  # Creates a game instance, and starts play

