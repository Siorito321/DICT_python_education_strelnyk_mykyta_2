import random
import json
import os.path


class Game:
    """
    A class that represents the game of Rock-Paper-Scissors.
    """

    def __init__(self, answer, name, variants) -> None:
        self.options = ["rock", "paper", "scissors"]
        self.variants = [a for a in variants.split(",")]
        self.comp_answer = random.choice(self.options)
        self.answer = answer
        self.action = True
        self.name = name
        self.scores = self.read_file()
        if self.name in self.scores:
            self.score = self.scores[self.name]
        else:
            self.score = 0

    def winner_chooser(self) -> str:
        """
        Choose the winner of the game based on the player's and computer's answers.

        Returns:
        str: A message describing the result of the game.
        """
        if self.variants == ['']:
            try:
                position_user = self.options.index(self.answer)
                position_comp = self.options.index(self.comp_answer)
                if position_comp == position_user :
                    result = f"There is a draw ({self.answer})"
                elif position_comp - position_user in [1, -2]:
                    result = f"Sorry, but the computer chose {self.comp_answer}"
                elif position_user - position_comp in [1, -2]:
                    result = f"Well done. The computer chose {self.comp_answer} and failed"
                self.update_score(result)
                return f"{result}"
            except ValueError:
                return "Incorrect input"
        else:
            try:
                position_user = self.variants.index(self.answer)
                list_variants = [a for a in self.variants if self.variants.index(a) != position_user]
                self.comp_answer = random.choice(list_variants)
                position_comp = list_variants.index(self.comp_answer)
                half_of_list_len = len(list_variants) / 2 if len(list_variants) % 2 == 0 \
                    else (len(list_variants) - 1) / 2
                if self.comp_answer == self.answer:
                    result = f"There is a draw ({self.answer})"
                elif position_comp in range(int(half_of_list_len)):
                    result = f"Well done. The computer chose {self.comp_answer} and failed"
                else:
                    result = f"Sorry, but the computer chose {self.comp_answer}"
                self.update_score(result)
                return f"{result}"
            except ValueError:
                return "Incorrect input"

    def if_exit(self) -> bool:
        """
        Check if player input is '!exit'.

        Returns:
        bool: True if user input is not '!exit', False otherwise.
        """
        if self.answer == "!exit":
            self.action = False
            return self.action

    def if_rating(self) -> str:
        """
        Provide player with the current user's score.

        Returns:
        str: The current user's score.
        """
        return f"Your rating: {self.score}"

    def read_file(self) -> dict:
        """
        Read scores from file and create it if needed.

        Returns:
        dict: A dictionary of scores read from the file.
        """
        with open("rating.txt", "a+") as f:
            f.seek(0)
            content = f.read()
            if len(content) == 0:
                scores = {}
            else:
                scores = json.loads(content)
            return scores

    def write_file(self, scores) -> None:
        """
        Writes the scores dictionary to the rating.txt file.

        Parameters:
        scores (dict): a dictionary containing player names and their scores.

        Returns:
        None
        """
        with open("rating.txt", "w") as f:
            content = json.dumps(scores)
            f.write(content)

    def update_score(self, result) -> None:
        """
        Updates the player's score based on the result of the game.

        Parameters:
        result (str): a string containing the game result.

        Returns:
        None
        """
        if "Well done" in result:
            self.score += 100
        elif "draw" in result:
            self.score += 50
        else:
            self.score += 0
        self.scores[self.name] = self.score


name = input("Enter your name:")
print(f"Hello, {name}")
variants = input(">")
print("Okay, let's start")
while True:
    game = Game(input("Enter your operation or figure:"), name, variants)
    if game.if_exit() is False:
        print("Bye!")
        break
    if game.answer == "!rating":
        print(game.if_rating())
    else:
        print(game.winner_chooser())
        game.write_file(game.scores)
