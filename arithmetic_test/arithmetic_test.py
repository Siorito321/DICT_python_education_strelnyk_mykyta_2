import random


# random.randint(2, 9)
class Test:

    mark_counter = 0
    level = 0

    def __init__(self):
        self.first_num = random.randint(2, 9)
        self.second_num = random.randint(2, 9)
        self.third_num = random.randint(11, 29)
        self.operations = [self.sum, self.sub, self.mult]

    def sum(self) -> int:
        """Generates an addition question using the two random numbers generated in the __init__ method.

        Parameters:
        None

        Returns:
        int: The correct answer to the addition question.
        """
        print(f"{self.first_num} + {self.second_num}")
        return self.first_num + self.second_num

    def sub(self) -> int:
        """Generates a subtraction question using the two random numbers generated in the __init__ method.

        Parameters:
        None

        Returns:
        int: The correct answer to the subtraction question."""
        print(f"{self.first_num} - {self.second_num}")
        return self.first_num - self.second_num

    def mult(self) -> int:
        """Generates a multiplication question using the two random numbers generated in the __init__ method.

        Parameters:
        None

        Returns:
        int: The correct answer to the multiplication question.
        """
        print(f"{self.first_num} * {self.second_num}")
        return self.first_num * self.second_num

    def square(self) -> int:
        """Generates a question asking for the square of a random number generated in the __init__ method.

        Parameters:
        None

        Returns:
        int: The correct answer to the square question.
        """
        print(f"{self.third_num} ^ 2")
        return int(self.third_num ** 2)

    def correct(self) -> None:
        """Asks the user a math question based on the level of difficulty set in the difficulty method.
        If the user enters an incorrect answer, it prompts them to try again until a correct answer is entered.

        Parameters:
        None

        Returns:
        None
        """
        try:
            if Test.level == 1:
                self.operation = self.operations[random.randint(0, 2)]()
                right_answer = int(self.operation)
                answer = int(input(">"))
                if answer == right_answer:
                    print("Correct!")
                    Test.mark_counter += 1
                else:
                    print("Incorrect!")
            elif Test.level == 2:
                right_answer = int(self.square())
                answer = int(input(">"))
                if answer == right_answer:
                    print("Correct!")
                    Test.mark_counter += 1
                else:
                    print("Incorrect!")
        except ValueError:
            print("Your answer should be a number!")
            self.correct()

    @classmethod
    def new_test(cls) -> None:
        """Resets the mark counter to 0 to start a new test.

        Parameters:
        None

        Returns:
        None
        """
        Test.mark_counter = 0

    @classmethod
    def difficulty(cls) -> None:
        """Prompts the user to select a level of difficulty for the test and sets the class level accordingly.

        Parameters:
        None

        Returns:
        None
        """
        try:
            hard_level = int(input("What level of difficulty you prefer? Type 1 or 2>"))
            if hard_level not in [1, 2]:
                raise ValueError
        except ValueError:
            print("Hard level should be a number (1 or 2)!")
            Test.difficulty()
        else:
            Test.level = int(hard_level)

    @classmethod
    def save_result(cls) -> None:
        """Prompts the user for their name and saves their score and name to a text file.

        Parameters:
        None

        Returns:
        None
        """
        name = input("Your name>")
        file = open("./result.txt", mode='w')
        file.write(f"{name}: {Test.mark_counter}/5 in level {Test.level}")
        print("Result is saved on result.txt file :)")
        file.close()


def test() -> str:
    """Runs the math test, asking the user five questions based on the difficulty level set in the difficulty method.
    At the end of the test, prompts the user to save their results and start over with a higher difficulty level.

    Parameters:
    None

    Returns:
    str: 'yes' or 'no' depending on whether the user wants to start over with a higher difficulty level.
    """
    for i in range(5):
        a = Test()
        a.correct()
    res = input(f"Your score is {Test.mark_counter}/5 ! Would you like to save the result? Enter yes or no>")
    if res == "yes":
        Test.save_result()
    again = input("would you like to start over with a higher difficulty level? yes or no>")
    return again


again = None
Test.difficulty()
while again != "no":
    again = test()
    if again == "yes":
        if Test.level != 2:
            Test.level += 1
        print("***if the difficulty level already set to 2 you will be tested at level 2 again***")

