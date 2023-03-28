# plain bold italic header link inline-code ordered-list unordered-list new-line

class Text_editor:
    """
    Provides user with ability to manipulate with a text files
    """
    def printing(self):
        """
        Prints the text from text.txt and creates it if there is no text.txt file found
        """

        f = open("./text.txt", mode="r")
        print(f.read())
        f.close()

    def redactor(self, operation):
        """
        Gives user ability to write information to text.txt

        Parameters:
        operation (str): string to write into text.txt
        """
        with open("./text.txt", mode="a") as f:
            f.write(operation)
            f.close()


    def clearing(self):
        """
        Clear files before new session or creates new files
        """
        file_to_delete = open("output.md", 'w')
        file_to_delete.close()
        file_to_delete = open("text.txt", 'w')
        file_to_delete.close()


class Markdown:
    """
    Provides user with ability to manipulate with a text itself and turn it into Markdown format
    """
    def plain(self, inputting) -> str:
        """Convert text to plain text

            Parameters:
            inputting (str): string to be converted

            Returns:
            str

           """
        return inputting

    def bold(self, inputting) -> str:
        """Convert text to bold text

            Parameters:
            inputting (str): string to be converted

            Returns:
            str
           """
        return f'**{inputting}**'

    def italic(self, inputting):
        """Convert text to italic text

            Parameters:
            inputting (str): string to be converted

            Returns:
            str
           """
        return f'*{inputting}*'

    def header(self, inputting):
        """Convert text to header text of different sizes

            Parameters:
            inputting (str): string to be converted

            Returns:
            str

           """
        self.size = int(input("Enter size:>"))
        if 6 < self.size or self.size < 1:
            return "incorrect size value"
        sharps = ''
        for i in range(self.size):
            sharps += '#'
        return f"{sharps}{inputting}{sharps}\n"
    def link(self, inputting):
        """Convert text to link with url inside

            Parameters:
            inputting (str): string to be converted

            Returns:
            str

           """
        self.url = str(input("URL:>"))
        return f"[{inputting}]({self.url})"

    def inline_code(self, inputting):
        """Convert text to inline code

            Parameters:
            inputting (str): string to be converted

            Returns:
            str
           """
        return f"'{inputting}'"

    def ordered_list(self, rows):
        """Convert text into ordered list

            Parameters:
            rows (int): number of rows in the list

            Returns:
            str
           """
        answer = ''
        for i in range(rows):
            answer = answer + f'{i + 1}.' + input(f'Row #{i + 1}:>')
            answer += '\n'
        return answer

    def unordered_list(self, rows):
        """Convert text into unordered list

            Parameters:
            rows (int): number of rows in the list

            Returns:
            str: answer
           """
        answer = ''
        for i in range(rows):
            answer = answer + '- ' + input(f'Row #{i + 1}:>')
            answer += '\n'
        return answer

    def new_line(self):
        """Add a new line to text.txt

            Returns:
            str
           """
        return '\n'

    def help(self):
        """
        Returns information about available options for user
        """
        return """Available formatters: plain bold italic header link inline-code ordered list unordered-list new-line
        Special commands: !help !done"""


class Menu(Markdown, Text_editor):
    """
    Provides user with ability to choose options of text formatting into Markdown format
    """
    def __init__(self):
        self.commands = {'plain': self.plain, 'bold': self.bold, 'italic': self.italic, 'header': self.header,
                         'link': self.link, 'inline-code': self.inline_code,
                         'ordered-list': self.ordered_list,
                         'unordered-list': self.unordered_list, 'new-line': self.new_line,
                         "!help": self.help(), "!done": None}

    def start_menu(self):
        """Main interface for user`s actions"""
        while True:
            self.command = input('choose a formatter:>')
            try:
                i = self.commands[self.command]
            except KeyError:
                print("Unknown formatting type or command")
                self.start_menu()
            finally:
                break
        if self.command == "!help":
            print(self.help())
            self.start_menu()
        elif self.command == 'ordered-list' or self.command == 'unordered-list':
            rows = int(input('Number of rows: > '))
            if rows <= 0:
                print('The number of rows should be greater than zero')
                self.start_menu()
            else:
                self.redactor(self.commands[self.command](rows))
                self.printing()
                self.start_menu()
        elif self.command != "!done":
            inputting = input("Text:>")
            self.redactor(self.commands[self.command](inputting))
            self.printing()
            self.start_menu()
        else:
            with open('text.txt') as file:
                for line in file:
                    with open('output.md', mode="a") as k:
                        k.write(line)
                        k.close()
            print('execution is over, file is saved')


menu = Menu()
menu.clearing()
#если удалить text.txt и output.md, то они здесь создадутся и не вызовут никаких ошибок
menu.start_menu()

