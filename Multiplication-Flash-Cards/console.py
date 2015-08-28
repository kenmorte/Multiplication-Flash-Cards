import random, tkinter

class Multiplication:
    def __init__(self):
        """Creates counters, correct streaks, and number limits."""
        self._wrong_counter = 0
        self._right = 0
        self._min_num, self._max_num = (0,12) # Default number limits from 0-12
        self._streak = 0    # Default number for counters = 0
        
    def console_start(self):
        """
        Console version of application. Starts flash cards application in its console-form.
        Most basic form includes randomized questions, error-checking, and game over message.
        """
        self._name = input('What is your name? ') # Asks input for player's name
        while True:
            try:
                self._count_choice = int(input('How many times do you want to get wrong or else game over? (Choose number 1 or more) '))
                if self._valid_count_choice(self._count_choice):
                    print('You must choose a number 1 or more!')
                    continue
                break
            except ValueError: 
                print('\nThat\'s not a valid number!') # Error-checking for user entering non-number
                
        while not self.game_is_over(self._count_choice, self._wrong_counter):
            first, second = self.choose_numbers()
            answer = self.get_answer(first, second)
            if self.correct(answer, first, second):
                print("That's correct! Good job {}!".format(self._name))
                self.inc_right()
            else:
                print("Oh no! That's wrong {}! The correct answer was {}!".format(self._name,first*second))
                self.inc_wrong()
        print('Game over! {} got {} questions right!'.format(self._name,self._right))
                
                
    def choose_numbers(self):
        """
        Randomly chooses two sets of numbers, with the first being strictly in between the number limits.
        The second number is chosen between 0 and 12.
        """
        first = random.randint(self._min_num, self._max_num) 
        return (first, random.randint(0,12))
    
    def get_answer(self, first, second):
        """Returns user's answer input with error-checking."""
        while True:
            try:
                return int(input('What is {} times {}? '.format(first,second)))
            except ValueError:
                print('That\'s not a valid number!')
        
    
    def valid_count_choice(self, count):
        """Returns True if count is still 0."""
        return count < 1
    
    def correct_answer(self,first,sec):
        """Returns the correct answer for a specific multiplication problem."""
        return first*sec
    
    def correct(self, answer, first, second):
        """Returns True if user's answer was correct."""
        return answer == self.correct_answer(first, second)
    
    def inc_right(self):
        """Increments correct counter by 1."""
        self._right += 1
        
    def inc_wrong(self):
        """Increments wrong counter by 1."""
        self._wrong_counter += 1
        
    def inc_streak(self):
        """Increments correct-streak counter by 1."""
        self._streak += 1
        
    def reset_streak(self):
        """Resets correct-streak counter to 0."""
        self._streak = 0
        
    def reset_counter(self):
        """Resets both wrong and correct counter to 0."""
        self._right, self._wrong_counter = (0,0)
    
    def game_is_over(self):
        """Returns True if game is over when wrong counter equals wrong limit."""
        return self._wrong_counter == self._count_choice
