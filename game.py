from random import randrange
import random
import fileinput


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

        self.code = []
        self.num_hints = 0
        self.game_mode = "user_guess"
        self.num_guesses = 8
        self.guess = []

        self.temp_index = [0, 1, 2, 3]  # keep track of which index of the code has been "hinted"



        self.UI = UI()  # Initializes UI iterface
        # self.game_loop()  # Starts game

    def game_loop(self):
        """
        Main loop for game operation.
        :return: nothing
        """
        input = ""

        while input != "quit":
            self.game_mode, self.num_guesses = self.UI.start_menu()  # Get user input on game mode and max number of guesses.

            if self.game_mode == "user_guess":
                self.code = self.generate_code()
            elif self.game_mode == "computer_guess":
                self.code = self.UI.user_generates_code().split()

            result, guesses = self.play_game()  # Play game!

            self.save_stats(result, guesses)
            input = self.UI.end_menu(result)



    def play_game(self):

        i=0

        i = 0
        if self.game_mode == "user_guess":
            self.code = self.generate_code()
        elif self.game_mode == "computer_guess":
            self.code = self.UI.user_generates_code().split()


        while i <= self.num_guesses:
            # User Guesses
            if self.game_mode == "user_guess":

                input = self.UI.guess_menu()  # Get input from user to determine which operation to perform
                if input == "hint":
                    hint, index = self.generate_hint()
                    self.UI.hint(hint, index)  # Gives a hint using the user's most recent guess

                elif input == "quit":
                    return "lose", i  # end while loop, and take user to end_menu()

                else:  # if the user guesses a code, return feedback to the user on correctness
                    print "code is: ", self.code  # PRINTS ANSWER, REMOVE IN FINAL
                    self.guess.append(input.split())  # Add user's guess to list of guesses

                    correct_pos, correct_num = self.code_analysis(self.guess)
                    if correct_pos == len(self.code):
                        return "win", i  # end while loop, and take user to end_menu()
                    else:
                        self.UI.feedback(correct_pos, correct_num)
                    i += 1

            # Computer Guesses
            elif self.game_mode == "computer_guess":

                guess = self.generate_guess()
                correct_pos, correct_num = self.code_analysis(guess)
                if correct_pos == len(self.code):
                    return "win", i  # end while loop, and take user to end_menu()
                else:
                    self.UI.feedback(correct_pos, correct_num)
                i += 1
        return "lose", i  # end while loop, and take user to end_menu()



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
        correct_nums = []


        for i in range(4):  # Loop over each digit in the most recent guess and the correct code
            # for j in guess:
            digit = self.guess[len(self.guess) - 1][i]
            if self.code[i] == digit:  # Test to find a correct digit in the correct place
                correct_pos += 1
                correct_num += 1
                correct_nums.append(digit)


            elif (digit in self.code) and (digit not in correct_nums):

                correct_nums.append(digit)  # If the number hasn't already been found, increment correct_num and add to list to eliminate duplicates

        return correct_pos, correct_num

    def generate_code(self):
        """
        Generates a random, 4-digit code with each value in the range [1,6]
        :return: the randomly generated code.
        """
        code = []

        for i in range(4):
            code.append(str(randrange(1, 6)))

        return code

    def generate_hint(self):
        """
        Gives the player a hint about the correct code. The method iterates over the user's most recent guess to determine
        if they have guessed a number that exists in the answer, and if so, returns the correct position of that number.
        If the user does not have a correct number in their guess, return a random correct number from the answer, and
        its position.
        :return: A correct number in the answer, and its position in the answer as ints.
        """

        if len(self.temp_index) == 0:                       # all digits in the code have been hinted to the user
            return 0,0

        elif len(self.guess) != 0:                          # if the user has given any guess
            for i in self.guess[len(self.guess) - 1]:       # for each digit i
                try:
                    index = self.code.index(i)              # if i is in the code and hasn't been given
                    self.temp_index.remove(index)
                    return i, index                         # give i as a hint

                except ValueError:                          # if i is not in the code or has been given
                    temp_hint_index = random.choice(self.temp_index)  # randomly generate another hint
                    temp_hint = self.code[temp_hint_index]
                    self.temp_index.remove(temp_hint_index)
                    return temp_hint, temp_hint_index

        else:                                               # if the user hasn't given any guess
            temp_hint_index = random.choice(self.temp_index)     # randomly generate another hint
            temp_hint = self.code[temp_hint_index]
            self.temp_index.remove(temp_hint_index)
            return temp_hint, temp_hint_index

    def generate_guess(self):


        """
        Generates a random(for now) code to guess what the correct code is.
        :return: the 4-digit code with each value in the range [1,6]
        """

        code = []
        for i in range(4):
            code.append(str(randrange(1, 6)))

        return code

    def save_stats(self, result, guesses):

        with open("statistics.txt", "r") as file_in:
            statistics = file_in.read().splitlines()

            for i in statistics:
                statistics[statistics.index(i)] = float(i)  # Cast each line as an int for additions

            if self.game_mode == "user_guess":
                statistics[0] += 1 if result == "win" else 0  # add 1 to win or lose for user
                statistics[1] += 1 if result == "lose" else 0
                statistics[2] = (statistics[2] + guesses) / 2.0  # Running average of user's guesses

            if self.game_mode == "computer_guess":
                statistics[3] += 1 if result == "win" else 0  # add 1 to win or lose for computer
                statistics[4] += 1 if result == "lose" else 0

            for i in statistics:
                statistics[statistics.index(i)] = str(i)  # Cast each line as an str for file writing

        with open("statistics.txt", "w") as file_out:
            file_out.write("\n".join(statistics))  # Write statistics as a concatenated string with \n as separator

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
        welcome_message = "\nWelcome to MasterMind"
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
        :return: the game mode (user_guess/computer_guess)
        """
        valid_input = False

        while valid_input == False:

            game_mode = input("Enter '1' for 'User Guess' mode, enter '2' for 'Computer Guess' mode: ")

            if game_mode == 1:
                valid_input = True
                return "user_guess"

            elif game_mode == 2:
                valid_input = True
                return "computer_guess"

            else:
                print("Invalid input.")

    def guess_menu(self):
        """
        Display in-game options for user or the next code guess,
        including hint or quit options, and prompt for user's input.
        Input should check for correct exit/hint statements and valid guesses.
        :return: valid guess or instruction (hint/quit)
        """
        input_instruction = "Enter your guess as a four-digit number separated by space (i.e. 2 2 2 2).\n" \
                            "Or enter 'hint' for a hint.\n" \
                            "Or enter 'quit' to quit."  # The backslashes allow the string to be multiline for readability
        valid_input = False

        while valid_input == False:

            print(input_instruction)
            instruction = str(raw_input("Your input: "))

            if instruction == "hint":
                valid_input = True

            elif instruction == "quit":
                valid_input = True

            else:
                valid_input = self.validate(instruction)

        return instruction

    def hint(self, hint, index):
        """
        Display the hint
        :return: nothing
        """
        if hint==0 and index==0:
            print "You have asked hint 4 time! The answer is right there! Think!"


        else:
            print "Number {} is located at place {}".format(hint, index +1)



    def user_generates_code(self):
        """
        In the "computer_guess" mode, ask the user to input the code and validate the code
        :return: the user generated code
        """
        valid_input = False

        while valid_input == False:
            code = str(raw_input("Enter the code as a four-digit number seperated by space (i.e. 2 2 2 2):"))
            valid_input = self.validate(code)

        return code

    def feedback(self, num_correct_pos, num_correct):
        """
        Display computer feedback on user's code guess
        :return: nothing
        """
        print("The number of the correct positions is {}.".format(num_correct_pos))
        print("The number of the correct numbers is {}.".format(num_correct))

    def end_menu(self, result):
        """
        End the game
        Display Win/Loss and gameplay statistics
        :return: boolean, "True" for starting a new game, "False" for leaving this game
        """
        print("You {}!".format(result))
        file = open("statistics.txt", "r")
        statistics = file.read().splitlines()
        file.close()

        print "The user's number of wins is: ", statistics[0]
        print "The user's number of loses is: ", statistics[1]

        print "The average number of user guesses: ", statistics[2]

        print "The number of guesses for this game was: ", statistics[2]


        print "The computer's number of wins is: ", statistics[3]
        print "The computer's number of loses is: ", statistics[4]



        start_a_new_game = raw_input("Do you want to start a new game? Enter 'yes' to start or others to quit.")

        if start_a_new_game == 'yes':
            return True
        else:
            return 'quit'

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

        elif len(output) == 4:
            for e in output:
                if e not in valid_digit:
                    print("Invalid input.")
                    return False
        else:
            return True


game = Game()

game.game_loop()

