class Main_Menu:
    def __init__(self, width_of_ascii_art):
        """
        Defines the variables that are associated with this class object.
        :return: STR
        """
        self.num_of_lines_wanted = None  # Defines a class variable for the 'self.enter_rle' method
        self.width_of_ascii_art = width_of_ascii_art  # The width of the ASCII art the user is going to input

    def __repr__(self):
        """
        Returns information on the class object.
        :return: STR
        """
        return f'{self.__class__.__name__}'

    def run(self):
        """
        Runs the main loop of the main menu, displaying and giving all of the functionality of the main menu.
        :return: None
        """
        print("Welcome to the ASCII Art main menu!\n")

        choice = input('Here are your following options:\n\n'
                       'Enter RLE\nDisplay ASCII Art\nConvert to ASCII art\nConvert to RLE\nQuit\n\n') \
            .lower().strip().replace(' ', '')  # Offers a range of choices for the user, for them to chose.
        # 'choice' will need manual maintenance if another option is added.
        print('\n')

        if choice == 'quit':
            print('Goodbye, come back later!')
            quit()

        elif choice == 'enterrle':  # 'Enter RLE' option
            self.enter_rle()

        elif choice == 'displayasciiart':  # 'Display ASCII Art' option
            self.display_ascii_art()

        elif choice == 'converttoasciiart':  # 'Convert to ASCII art' option
            self.convert_to_ascii()

        elif choice == 'converttorle':  # 'Convert to RLE' option
            self.convert_to_rle()

        else:
            print('Sorry, that is not a valid option. Please pick an option, that is displayed!\n\n')

    def enter_rle(self):
        """
        Allows the user to enter raw text that is compressed under run-length-encoding and see the image that they typed
        , line by line.
        :return: None
        """
        while 1:
            self.num_of_lines_wanted = int(input('How many lines of RLE compressed data do you wish to enter?\n\n'))
            print('\n')
            if self.num_of_lines_wanted > 2:
                break
            else:
                print('Please enter a number greater than 2.\n')

        data_to_be_decompressed = []
        num_of_lines_entered = 0
        while num_of_lines_entered < self.num_of_lines_wanted:
            # Ensures that the user enters all of their lines of compressed RLE data
            line = input('Please enter the next line:\n\n')
            print('\n')
            data_to_be_decompressed.append(line)
            num_of_lines_entered += 1
        print('\n')

        decoded_data = []  # Holds all of the decompressed ASCII art
        for line in data_to_be_decompressed:
            string_to_append = ''
            line = line.strip('\n')
            for i in range(int(len(line) / (self.width_of_ascii_art+1))):
                # The number of sets rle coding e.g len(line) / 3 would be 2 digits maximum of a character
                current_rle = line[i * (self.width_of_ascii_art + 1):(i + 1) * (self.width_of_ascii_art + 1)]
                # Gets the current character of RLE that needs decompressing
                num_of_times = int(current_rle[:self.width_of_ascii_art])
                # The amount of times that character appears in a row
                char = current_rle[self.width_of_ascii_art]  # the character itself
                string_to_append += char * num_of_times
                # Add to that line the character multiplied by the amount of times it appears
            decoded_data.append(string_to_append)

        print(*decoded_data, sep='\n', end='\n\n')

    def display_ascii_art(self):
        """
        Displays ASCII art from a file that is given by the user.
        :return: NONE
        """
        name_of_file = input('Please type the exact name of the file that contains the ASCII art:\n\n')
        print('\n')
        try:
            with open(f'{name_of_file}.txt', 'r') as f:
                print(*f.readlines())

        except FileNotFoundError:
            print('Please type the name of the file correctly.\n\n')
            self.display_ascii_art()

    def convert_to_ascii(self):
        """
        Takes in a file from the user and decompresses the data to ASCII Art and then prints it.
        :return: NONE
        """
        name_of_file = input('Please type the exact name of the file that contains the RLE compressed data:\n\n')
        print('\n')
        decoded_data = []  # Holds all of the decompressed ASCII Art
        try:
            with open(f'{name_of_file}.txt', 'r') as f:  # Tries to open the file with the name given by the user
                for line in f.readlines():
                    line = line.strip('\n')  # Gets rid of the '\n' in every line
                    string_to_append = ''  # Holds all of the current line's decompressed ASCII Art
                    for i in range(int(len(line) / (self.width_of_ascii_art + 1))):  # Allows for limitless flexibility
                        # For loop gets the number of characters there are to be decompressed
                        current_rle = line[i * (self.width_of_ascii_art + 1):(i + 1) * (self.width_of_ascii_art + 1)]
                        # Gets the current part of the string that has to be decoded
                        num_of_times = int(current_rle[:self.width_of_ascii_art])
                        # Gets the number of times the character appears
                        char = current_rle[self.width_of_ascii_art]  # Gets the current character
                        string_to_append += char * num_of_times
                    decoded_data.append(string_to_append)
            print(*decoded_data, sep='\n', end='\n\n')

        except FileNotFoundError:
            print('Please type the name of the file correctly.\n\n')
            self.convert_to_ascii()

    def convert_to_rle(self):
        """
        Compresses and stores the ASCII Art in a different file, as well as comparing the number of characters in the
        original (decompressed) file and the new (compressed) file.
        :return: None
        """
        name_of_file = input('Please type the exact name of the file that contains the ASCII decompressed data:\n\n')
        print('\n')
        compressed_data = []
        try:
            with open(f'{name_of_file}.txt', 'r') as f:
                num_of_decoded_characters = len(f.read())
                f.seek(0)  # Ensures that the entire file gets re-read
                for line in f.readlines():
                    encoding = ''
                    prev_char = ''
                    count = 1
                    for i, char in enumerate(line):
                        if i == len(line) - 1:  # If it is the final character in the line
                            if (count_length := len(str(count))) < self.width_of_ascii_art:
                                # Ensures that any width of ASCII characters is dealt with and given the proper
                                # formatting.
                                count = (self.width_of_ascii_art - count_length) * '0' + str(count)
                            encoding += str(count) + prev_char
                            break

                        else:
                            if char != prev_char:  # If the current character is different to the previous character
                                if prev_char:  # If 'prev_char' has a value
                                    if (count_length := len(str(count))) < self.width_of_ascii_art:
                                        # Ensures that any width of ASCII characters is dealt with and given the proper
                                        # formatting.
                                        count = (self.width_of_ascii_art - count_length) * '0' + str(count)
                                    encoding += str(count) + prev_char
                                count = 1  # Resets the count
                                prev_char = char  # Starts the process again with the new character

                            else:  # If it is the same character
                                count += 1  # Increase the counter by 1

                    compressed_data.append(encoding)

            with open(f'{name_of_file} RLE Compressed.txt', 'w+') as f:
                # Writes all of the compressed data into a seperate file.
                f.write('\n'.join(compressed_data) + '\n')
                f.seek(0)  # Ensures that the entire file gets re-read
                num_of_encoded_characters = len(f.read())

            print('Successfully compressed and stored compressed data into a seperate file')
            print(f'Number of decompressed ASCII art characters: {num_of_decoded_characters}')
            print(f'Number of compressed RLE characters: {num_of_encoded_characters}')
            print(f'That is a decrease of {num_of_decoded_characters - num_of_encoded_characters} characters!\n\n')

        except FileNotFoundError:
            print('Please type the name of the file correctly.\n\n')
            self.convert_to_rle()


while 1:
    Main_Menu(2).run()
