import random


class Game:
    """
    An implementation of the code-guessing game, Mastermind. The object of the game is to guess a 4-digit
    code, with each digit in the range [1,6], within a specified amount of tries.
    This game is played by a user against the computer, or vice versa. The computer and the user play against eachother
    for a user-defined number of rounds.

    The program is organized in a two-layer approach. Input/output handling and validation is done by the UI helper class,
    and game logic/simulation is handled by the Game class. The basic structure is as follows:
    A Game object calls game_loop, which starts a new game, asking the player how many rounds they'd like to play, and who will guess first. The game_loop
    then iterates for the number of rounds playing a game and keeping track of the user's and the computer's scores.
    After the number of rounds is reached, the overall winner is determined, and displayed to the user.
    The user then has the option to play a new game.
    """

    def __init__(self):
        """
        Setup for game start, initializes class variable for correct code, num_hints, the game_mode,
        num_guesses, a holder for the user's guess, and starts game_loop
        @joseph zieg & Yixiong Zhang
        """

        self.code = []
        self.num_hints = 0
        self.game_mode = "user_guess"
        self.num_guesses = 8
        self.guess = []
        self.temp_index = [0, 1, 2, 3]  # keep track of which index of the code has been "hinted"
        self.guess_set = []
        self.num_rounds = 1

        self.user_points = 0
        self.computer_points = 0

        self.UI = UI()  # Initializes UI iterface

    def game_loop(self):
        """
        Main loop for game operation. Initializes the answer code based on game_mode, as well as additional variables
        guess_set and an initial guess if the computer is playing.

        @joseph zieg
        :return: nothing
        """
        keep_playing = True

        while keep_playing:
            self.__init__()
            rounds_played = 0
            # Get user input on game mode and number of rounds to play.
            self.game_mode, self.num_rounds = self.UI.start_menu()
            result = ""
            while rounds_played < self.num_rounds:
                if self.game_mode == "user_guess":
                    self.code = self.generate_code()
                    # self.code = ['5', '5', '1', '2']  # Test code for bug checking

                elif self.game_mode == "computer_guess":
                    self.code = self.UI.user_generates_code().split()
                    self.num_guesses = 15  # Allows code solver a greater chance of winning
                    self.create_set()  # Creates set for eliminating non-possible numbers
                    self.guess = self.generate_guess()  # Generate initial guess

                result, guesses = self.play_game()  # Play game!
                if result == "quit":
                    break

                if self.game_mode == "user_guess":  # Add points to computer's score if user guesses
                    self.computer_points += guesses
                    self.computer_points += 1 if result == "lose" else 0  # Add one if user loses

                if self.game_mode == "computer_guess":  # Add points to user's score if computer guesses
                    self.user_points += guesses / 2  # reducing for computer's larger num_guesses
                    self.user_points += 1 if result == "lose" else 0  # Add one if computer loses

                # Display the outcome of that round
                self.UI.display_outcome(result, self.game_mode, self.code, self.user_points, self.computer_points)
                self.game_mode = "computer_guess" if self.game_mode == "user_guess" else "user_guess" # Change game_mode
                self.num_guesses = 8 if self.game_mode == "user_guess" else 14  # reset max guesses

                rounds_played += .5  # Each game played by computer/user is 1/2 a round
            if result != "quit":
                final_result = "win" if self.user_points > self.computer_points else "lose"
            else:
                final_result = "quit"
            self.save_stats(final_result)  # Write stats to file
            keep_playing = self.UI.end_menu(final_result)  # Go to end menu, display stats, and loop

    def play_game(self):
        """
        Game loop for user/computer guess operations. The user/computer is allowed to guess up to
        the num_guesses amount, then the loop ends. The loop calls functions to get new user/computer input for the
        guess, return feedback for the player, and determine if the game is won ro lost.

        @joseph zieg
        :return: "win" or "lose" based on outcome, the number of guesses i the player required
        """
        guesses = 0  # the number of guesses the player has made

        while guesses < self.num_guesses:
            # User Guesses
            if self.game_mode == "user_guess":

                response = self.UI.guess_menu()  # Get input from user to determine which operation to perform
                if response == "hint":
                    hint, index = self.generate_hint()
                    self.UI.hint(hint, index)  # Gives a hint using the user's most recent guess

                elif response == "quit":
                    return "quit", guesses  # end while loop, and take user to end_menu()

                else:  # if the user guesses a code, return feedback to the user on correctness
                    # print "code is: ", self.code  # PRINTS ANSWER, REMOVE IN FINAL
                    self.guess = response.split()  # Add user's guess to list of guesses

                    correct_pos, correct_num = self.code_analysis()
                    if correct_pos == len(self.code):
                        return "win", guesses  # end while loop, and take user to end_menu()
                    else:
                        self.UI.feedback(correct_pos, correct_num)
                    guesses += 1

            # Computer Guesses
            elif self.game_mode == "computer_guess":

                correct_pos, correct_num = self.code_analysis()
                self.UI.display_guess(self.guess)
                if correct_pos == len(self.code):
                    return "win", guesses  # end while loop, and take user to end_menu()
                else:
                    self.UI.feedback(correct_pos, correct_num)
                    self.reduce_guesses(correct_pos, correct_num)  # Reduce search space for possible guesses
                    self.guess = self.generate_guess()  # Make new, random guess

                guesses += 1
        return "lose", guesses  # end while loop, and take user to end_menu()

    def code_analysis(self):
        """
        Analyses the user's current guess against the code to return feedback for the computer or player,
        so that they can make a new educated guess.
        Does not test for correct guess format.

        @ Yujia Zhang & Yixiong Zhang
        :return: int values for the correct values in the correct position (correct_pos),
        and the number of correct values in the guess (correct_num) , mutually exclusive.
        """
        correct_pos = 0
        correct_num = 0
        temp_code_index = [0, 1, 2, 3]
        temp_code = self.code[:]                # make a copy of the original code

        for i in range(4):                      # Loop over each digit in the most recent guess and the correct code
            if self.guess[i] == self.code[i]:   # Test to find a correct digit in the correct place
                correct_pos += 1
                temp_code_index.remove(i)       # remove the index to avoid double check in "correct_num"
                temp_code[i] = None             # remove the correct digit from the code

        for i in temp_code_index:               # Loop over each digit in the most recent guess and the correct code
            if self.guess[i] in temp_code:
                correct_num += 1
                temp_code[temp_code.index(self.guess[i])] = None  # remove 1st occurrence of correct digit in the code

        return correct_pos, correct_num

    def generate_code(self):
        """
        Generates a random, 4-digit code with each value in the range [1,6]

        @ Yixiong Zhang
        :return: the randomly generated code.
        """
        code = []

        for i in range(4):
            code.append(str(random.randrange(1, 7)))

        return code

    def generate_hint(self):
        """
        Gives the player a hint about the correct code. The method iterates over the user's most recent guess to determine
        if they have guessed a number that exists in the answer, and if so, returns the correct position of that number.

        If the user does not have a correct number in their guess, return a random correct number from the answer, and
        its position.

        @ Yujia Zhang
        :return: A correct number in the answer, and its position in the answer as ints.
        """

        if len(self.temp_index) == 0:  # all digits in the code have been hinted to the user
            return 0, 0

        elif len(self.guess) != 0:  # if the user has given any guess
            for i in self.guess[len(self.guess) - 1]:  # for each digit i
                try:
                    index = self.code.index(i)  # if i is in the code and hasn't been given
                    self.temp_index.remove(index)
                    return i, index  # give i as a hint

                except ValueError:  # if i is not in the code or has been given
                    temp_hint_index = random.choice(self.temp_index)  # randomly generate another hint
                    temp_hint = self.code[temp_hint_index]
                    self.temp_index.remove(temp_hint_index)
                    return temp_hint, temp_hint_index

        else:  # if the user hasn't given any guess
            temp_hint_index = random.choice(self.temp_index)  # randomly generate another hint
            temp_hint = self.code[temp_hint_index]
            self.temp_index.remove(temp_hint_index)
            return temp_hint, temp_hint_index

    def reduce_guesses(self, correct_pos, correct_num):
        """
        Reduces the possible search space based upon feedback from code_analysis(). Numbers that would not generate a
        correct answer because of 0 correct numbers, or 0 correct positions will be removed from self.guess_set. This
        is then used by generate guess to make a new code guess based on the reduced search space.

        @joseph zieg
        :param correct_pos:
        :param correct_num:
        :return:
        """
        old_guess = self.guess

        #print self.guess_set
        if correct_pos == 0:
            for i in range(len(old_guess)):
                if old_guess[i] in self.guess_set[i]:
                    self.guess_set[i].remove(old_guess[i])
                elif correct_num == 0:  # If there are no correct numbers at all, then remove all numbers in the guess
                    for j in range(1, len(self.guess_set)):  # from guess set.
                        if old_guess[j] in self.guess_set[j]:
                            self.guess_set[j].remove(old_guess[j])

    def generate_guess(self):
        """
        Generates a random code to guess what the correct code is, from a the pool of guesses possible.

        @joseph zieg
        :return: the 4-digit code with each value in the range [1,6]
        """
        new_code = []
        for i in self.guess_set:
            new_code.append(i[random.randrange(0, len(i))]) if len(i) > 1 else new_code.append(i[0])

        return new_code

    def create_set(self):
        """
        Generates the initial possible search space for code combinations that can be generated by the computer.

        @joseph zieg
        :return: nothing
        """
        for i in range(4):
            self.guess_set.append(["1", "2", "3", "4", "5", "6"])

    def save_stats(self, result):
        """
        Saves game statistics to a save file for aggregating player data over time. This includes the user's win/loss
        and the computer's win/loss, and the average number of guesses the player takes to find the answer.

        @joseph zieg
        :param result: The outcome of the game
        :param guesses: The number of guesses needed to find the correct answer
        :return: nothing
        """
        with open("statistics.txt", "r") as file_in:
            statistics = file_in.read().splitlines()

            for i in statistics:
                statistics[statistics.index(i)] = int(i)  # Cast each line as an int for additions

            if self.game_mode == "user_guess":
                statistics[0] += 1 if result == "win" else 0  # add 1 to win or loss for user
                statistics[1] += 1 if result == "lose" else 0

            if self.game_mode == "computer_guess":
                statistics[2] += 1 if result == "win" else 0  # add 1 to win or loss for computer
                statistics[3] += 1 if result == "lose" else 0

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

        @ Yujia Zhang
        :return: the game mode as a string
        """
        welcome_message = "\nWelcome to MasterMind"
        introduction = "This is a number-guessing game. The code is a four-digit number and there are six options for each digit." \
                       "\nThe one who guesses the code correctly under certain tries wins the game!"
        print(welcome_message)
        print(introduction)

        game_mode = self.get_first()
        num_rounds = self.get_num_rounds()

        return game_mode, num_rounds

    def get_first(self):
        """
        To initiating the game, ask the user for the user guess or the computer guess first

        @ Yujia Zhang
        :return: the game mode (user_guess/computer_guess)
        """
        valid_input = False

        while valid_input == False:

            game_mode = raw_input("Enter '1' for user guess first, enter '2' for computer guess first : ")

            if game_mode == '1':
                valid_input = True
                return "user_guess"

            elif game_mode == '2':
                valid_input = True
                return "computer_guess"

            else:
                print("Invalid input.")


    def get_num_rounds(self):
        """
        ask the user for the number of rounds

        @ Yujia Zhang
        :return: the number of rounds
        """

        valid_input = False

        while not valid_input:

            num_rounds = raw_input("Enter the number of rounds you would like to play: ")

            try:
                num_rounds = int(num_rounds)
                if num_rounds > 0:
                    return num_rounds
                else:
                    print("\nYou must play at least one round.")

            except ValueError:
                print("\nInvalid input.")


    def guess_menu(self):
        """
        Display in-game options for user or the next code guess,
        including hint or quit options, and prompt for user's input.

        Input should check for correct exit/hint statements and valid guesses.

        @ Yujia Zhang
        :return: valid guess or instruction (hint/quit)
        """
        input_instruction = "\nEnter your guess as a four-digit number separated by space (i.e. 2 2 2 2).\n" \
                            "Or enter 'hint' for a hint.\n" \
                            "Or enter 'quit' to quit."
        valid_input = False

        while not valid_input:

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

        @ Yujia Zhang
        :return: nothing
        """
        if hint == 0 and index == 0:
            print "You have asked for a hint 4 times! The answer is right there! Think!"

        else:
            print "Number {} is located at place {}".format(hint, index + 1)

    def user_generates_code(self):
        """
        In the "computer_guess" mode, ask the user to input the code and validate the code

        @ Yujia Zhang
        :return: the user generated code
        """
        valid_input = False

        while not valid_input:
            code = str(raw_input("\nEnter the code as a four-digit number separated by space (i.e. 2 2 2 2):"))
            valid_input = self.validate(code)

        return code

    def feedback(self, num_correct_pos, num_correct):
        """
        Display computer feedback on user's code guess

        @ Yujia Zhang
        :return: nothing
        """
        print("\nThe number of the correct positions is {}.".format(num_correct_pos))
        print("The number of the correct numbers is {}.".format(num_correct))

    def display_guess(self, guess):
        """
        displays the computer's guess for the player to see

        @joseph zieg
        :param guess: The computer's current guess
        :return: nothing
        """
        print "My guess was {0} {1} {2} {3}".format(*guess)

    def display_outcome(self, result, game_mode, code, user_points, computer_points):
        """
        displays the computer's guess for the player to see

        @joseph zieg
        :param guess: The computer's current guess
        :return: nothing
        """

        player = "\nYou" if game_mode == "user_guess" else "\nI"
        print "{} {} this round!".format(player, result)
        print "The correct code was {} {} {} {}".format(*code)
        print "\nI have {} points".format(computer_points)
        print "You have {} points".format(user_points)

    def end_menu(self, final_result):
        """
        End the game
        Display Win/Loss and gameplay statistics

        @ Yujia Zhang
        :return: boolean, "True" for starting a new game, "False" for leaving this game
        """

        with open("statistics.txt", "r") as file_in:
            statistics = file_in.read().splitlines()

        print "\nYou {}!".format(final_result)
        print "\nThe user's number of wins is: ", statistics[0]
        print "The user's number of losses is: ", statistics[1]
        print "The computer's number of wins is: ", statistics[2]
        print "The computer's number of losses is: ", statistics[3]

        start_a_new_game = raw_input("Do you want to start a new game? Enter 'yes' to start or others to quit: ")

        if start_a_new_game == 'yes':
            return True
        else:
            print "\nThanks for playing!"
            return False

    def validate(self, input):
        """
        Validate either the code or the guess from the user's input.
        It should be a four-digit integer separated by space.

        @ Yujia Zhang
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
        return True


game = Game()
game.game_loop()
