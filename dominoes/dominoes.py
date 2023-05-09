import random
import sys


class NotAllowedToPlace(Exception):
    pass


class DominoesStart:
    """Represents the initial state of a dominoes game,
     including the stock, player hands, snake, and game status."""
    def __init__(self) -> None:
        """Initializes the starting state of the Dominoes game."""
        self.stock = self.start_stock_generator()
        self.user_hand = self.player_hand_generator()
        self.computer_hand = self.player_hand_generator()
        self.snake = []
        self.status_counter = self.check_biggest_double_and_status_setter()
        self.status = "Computer is about to make a move." \
            if self.status_counter % 2 == 0 \
            else "It's your turn to make a move."

    @staticmethod
    def start_stock_generator() -> list:
        """Generates the initial stock of dominoes.

        Returns:
        list: The initial stock of dominoes.
        """
        start_hand = []
        for i in range(0, 7):
            for b in range(i, 7):
                start_hand.append([i, b])
        return start_hand

    def status_update(self) -> None:
        """Updates the game status based on the status counter."""
        self.status = "Computer is about to make a move." \
            if self.status_counter % 2 == 0 \
            else "It's your turn to make a move."

    def player_hand_generator(self) -> list:
        """Generates a hand of dominoes for a player.

        Returns:
        list: The generated hand of dominoes.
        """
        player_hand = []
        for p in range(7):
            player_hand.append(self.stock.pop(random.choice(list(range(len(self.stock))))))
        return player_hand

    def check_biggest_double_and_status_setter(self) -> int:
        """Checks for the biggest double domino and sets the starting player.

        Returns:
        int: The index of the starting player.
        """
        players = [self.user_hand, self.computer_hand]
        help_list = [[-1, -1], [-1, -1]]
        for b in range(2):
            for i in range(0, len(players[b])):
                if players[b][i][0] == players[b][i][1] and players[b][i][0] > help_list[b][0]:
                    help_list[b] = players[b][i]
        if help_list == [[-1, -1], [-1, -1]]:
            self.stock = self.start_stock_generator()
            self.user_hand = self.player_hand_generator()
            self.computer_hand = self.player_hand_generator()
            self.check_biggest_double_and_status_setter()
        else:
            if help_list[0][0] > help_list[1][0]:
                players[0].remove(help_list[0])
                self.snake.append(help_list[0])
                return 0
            else:
                players[1].remove(help_list[1])
                self.snake.append(help_list[1])
                return 1


class Interface(DominoesStart):
    """Provides methods for displaying game information to the user,
     such as stock size, player hands, and the domino snake."""

    def user_pieces_out(self) -> str:
        """Returns a string representation of the user's hand.

        Returns:
        str: The string representation of the user's hand.
        """
        hand = ''
        iterat = 1
        for i in self.user_hand:
            hand += str(iterat) + "." + str(i) + "\n"
            iterat += 1
        return hand

    def snake_out(self) -> str:
        """Returns a string representation of the snake.

        Returns:
        str: The string representation of the snake.
        """
        snake_to_show = ""
        if len(self.snake) > 6:
            for i in range(3):
                snake_to_show += str(self.snake[i])
            snake_to_show += "..."
            for i in range(-3, 0, 1):
                snake_to_show += str(self.snake[i])
        else:
            snake_to_show = str(self.snake)
        return snake_to_show

    def information_output(self) -> str:
        """Returns a formatted string with the game information.

        Returns:
        str: The formatted string with the game information.
        """
        return f'''
======================================================================
Stock size # {len(self.stock)}
Computer pieces # {len(self.computer_hand)}
Domino snake # {self.snake_out()}
        
Your pieces:
{self.user_pieces_out()}
Status # {self.status}
        '''


class Actions(DominoesStart):
    """Contains methods for performing game actions,such as choosing tiles,
     moving the snake, checking for winners or draws,
      and handling tile placement rules."""
    def user_choose(self, position: int) -> list:
        """Handles the user's choice of a domino from their hand.

        Parameters:
        position (int): The position of the chosen domino in the user's hand.

        Returns:
        list: The chosen domino.
        """
        if position == 0:
            self.user_hand.append(self.stock.pop(random.randint(0, len(self.stock))))
        elif position in range(-1 * len(self.user_hand), 0):
            return self.user_hand[-1 * position - 1]
        elif position in range(1, len(self.user_hand) + 1):
            return self.user_hand[position - 1]
        else:
            raise ValueError

    def moving_snake(self, position, element) -> None:
        """Moves the snake based on the position and element.

        Parameters:
        position (int): The position to place the domino in the snake.
        element (list): The domino to be placed in the snake.

        Returns:
        None
        """
        if position < 0:
            self.snake.insert(0, element)
        else:
            self.snake.append(element)

    def if_winner(self) -> None:
        """Checks if there is a winner in the game.

        Returns:
        None
        """
        if len(self.user_hand) == 0:
            print("\n\n The game is over. You won!")
            sys.exit()
        elif len(self.computer_hand) == 0:
            print("\n\n The game is over. The computer won!")
            sys.exit()

    def if_draw(self) -> None:
        """Checks if the game is a draw.

        Returns:
        None
        """
        left = self.snake[0][0]
        right = self.snake[-1][1]
        if left == right:
            count = 0
            for tile in self.snake:
                if left in tile:
                    count += 1
            if count == 8:
                print("\n\n The game is over. It's a draw!")
                sys.exit()

    def reverse_tile(self, element) -> list:
        """Reverses the order of the elements in the domino.

        Parameters:
        element (list): The domino to be reversed.

        Returns:
        list: The reversed domino.
        """
        buffer = []
        for i in [1,0]:
            buffer.append(element[i])
        return buffer

    def if_allowed_to_place_end(self, element) -> list:
        """Checks if a domino can be placed at the end of the snake.

        Parameters:
        element (list): The domino to be checked.

        Returns:
        list: The domino if allowed to place, after potential reversal.

        Raises:
        NotAllowedToPlace: If the domino is not allowed to be placed at the end of the snake.
        """
        if element[0] == self.snake[-1][1]:
            return element
        elif element[1] == self.snake[-1][1]:
            return self.reverse_tile(element)
        else:
            raise NotAllowedToPlace

    def if_allowed_to_place_start(self, element) -> list:
        """Checks if a domino can be placed at the start of the snake.

        Parameters:
        element (list): The domino to be checked.

        Returns:
        list: The domino if allowed to place, after potential reversal.

        Raises:
        NotAllowedToPlace: If the domino is not allowed to be placed at the start of the snake.
        """
        if element[1] == self.snake[0][0]:
            return element
        elif element[0] == self.snake[0][0]:
            return self.reverse_tile(element)
        else:
            raise NotAllowedToPlace

    def if_allowed_tiles_left(self) -> None:
        """Checks if there are any allowed tiles left for the current player.

        Returns:
        None

        Raises:
        SystemExit: If there are no allowed tiles left for either the user or the computer.
        """
        a = [self.user_hand, self.computer_hand]
        for i in [0,1]:
            buffer_list = [elem for sub in a[i] for elem in sub]
            if len(self.stock) == 0:
                if self.snake[0][0] not in buffer_list and self.snake[-1][1] not in buffer_list:
                    match i:
                        case 0:
                            print("\n\n The game is over. You have no tiles to place. The computer won!")
                            sys.exit()
                        case 1:
                            print("\n\n The game is over. Computer has no tiles to place. You won!")
                            sys.exit()

    def prioritised_list(self) -> list:
        """Generates a prioritized list of tiles for the computer's move.

        Returns:
        list: The prioritized list of tiles.
        """
        buffer_list = [elem for sub in self.computer_hand for elem in sub] \
                      + [elem for sub in self.stock for elem in sub]
        buffer_dict = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        for i in range(7):
            buffer_dict[i] += buffer_list.count(i)
        values_of_tiles = []
        for b in self.computer_hand:
            values_of_tiles.append(0)
            if b in self.user_hand:
                values_of_tiles[self.user_hand.index(b)] += sum(buffer_dict[elem] for elem in b)
        dict_with_priorities = dict(zip(values_of_tiles, self.computer_hand))
        sorted_list = [value for _, value in sorted(dict_with_priorities.items(), key=lambda x: x[0], reverse=True)]
        return sorted_list


class Menu(Interface, Actions):
    """Manages the main game loop and controls the flow of the game,
     including user and computer turns. Inherits from Interface and Actions."""

    def main(self) -> None:
        """Runs the main game loop and manages the game flow.

        Returns:
        None
        """
        print(self.information_output())
        while True:
            if self.status_counter % 2 == 0:
                while self.computer() is False:
                    self.if_allowed_tiles_left()
                    continue
            else:
                self.if_allowed_tiles_left()
                a = self.user()
                if a is False:
                    continue
            self.status_counter += 1
            self.status_update()
            self.if_winner()
            self.if_draw()
            print(self.information_output())

    def computer(self) -> bool:
        """Handles the computer's move in the game.

        Returns:
        bool: True if the computer made a move, False otherwise.
        """
        prioritised_tiles = self.prioritised_list()
        for tile in prioritised_tiles:
            if tile[0] == self.snake[-1][1]:
                self.computer_hand.remove(tile)
                self.moving_snake(1, tile)
                input("Press Enter to continue")
                return True
            elif tile[1] == self.snake[-1][1]:
                self.computer_hand.remove(tile)
                self.moving_snake(1, self.reverse_tile(tile))
                input("Press Enter to continue")
                return True
            elif tile[1] == self.snake[0][0]:
                self.computer_hand.remove(tile)
                self.moving_snake(-1, tile)
                input("Press Enter to continue")
                return True
            elif tile[0] == self.snake[0][0]:
                self.computer_hand.remove(tile)
                self.moving_snake(-1, self.reverse_tile(tile))
                input("Press Enter to continue")
                return True
        if len(self.stock) != 0:
            self.computer_hand.append(self.stock.pop(random.randint(0, len(self.stock) - 1)))
            input("Press Enter to continue")
            return True
        return False

    def user(self) -> bool:
        """Handles the user's move in the game.

        Returns:
        bool: True if the user made a move, False otherwise.
        """
        try:
            user_input_int = int(input(">"))
            if user_input_int != 0:
                user_input = self.user_choose(user_input_int)
                if user_input_int < 0:
                    new_user_input = self.if_allowed_to_place_start(user_input)
                    self.user_hand.remove(user_input)
                else:
                    new_user_input = self.if_allowed_to_place_end(user_input)
                    self.user_hand.remove(user_input)
                self.moving_snake(user_input_int, new_user_input)
            else:
                if len(self.stock) != 0:
                    self.user_choose(user_input_int)
                else:
                    print("Sorry, but stock is empty")
                    self.user()
        except (ValueError, IndexError):
            print("Incorrect input!")
            return False
        except NotAllowedToPlace:
            print("Illegal move. Please try again.")
            return False


game = Menu()
game.main()
