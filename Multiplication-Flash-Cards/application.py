import random, tkinter
from console import Multiplication

class MultiplicationApp(Multiplication):
    master = tkinter.Tk()
    
    def __init__(self, master=None):
        """Initializes Multiplication Flash Cards console functions and starts application."""
        Multiplication.__init__(self)
        self.start_screen()
        
    def start(self):
        """Opens separate window with flash cards application."""
        self.master.mainloop()
        
    def start_screen(self):
        """
        Starts the option screen before starting application.
        Different options include the name used, minimum/maximum limit, and wrong amount before game over.
        Default options are given for these choices, and includes start/quit buttons as well.
        """
        self._canvas = tkinter.Canvas(self.master)
        self._canvas.grid()
        self._top_level()
        
        self.reset_counter()
        self.reset_streak()
        
        _welcome = tkinter.Label(self._canvas, text='Welcome to Multiplication Flash Cards!',
                                      anchor=tkinter.N, background='green',
                                      font=('Arial',40,'bold'))
        _welcome.grid(row=0, column=1, columnspan=2)
        
        
        _name_label = tkinter.Label(self._canvas, text='Name:', font=('Arial',25,'bold'), justify='right',anchor=tkinter.E)
        _name_label.grid(row=1, column=0, columnspan=2)
        default_text = tkinter.StringVar(); default_text.set('What is your name?')
        self._name_entry = tkinter.Entry(self._canvas, textvariable=default_text, 
                                         font=('Arial',25), justify='center')
        self._name_entry.grid(row=1, column=1, columnspan=2, pady=10,)
        self._name_entry.bind('<Button-1>', lambda x: default_text.set('') if self._name_entry.get() == 'What is your name?'\
                                 else None)
        self._name_entry.bind('<Return>', lambda event: self._on_start_down())
        
        _num_range_label = tkinter.Label(self._canvas, text='What numbers\nto study?', 
                                         font=('Arial',25,'bold'), justify='right',anchor=tkinter.E)
        _num_range_label.grid(row=2, column=0, columnspan=2)
        self._min_num_listbox = tkinter.Listbox(self._canvas, exportselection=False)
        self._min_num_listbox.grid(row=2, column=1, columnspan=2, pady=10)
        self._min_num_listbox.bind('<Return>', lambda event: self._on_start_down())
        self._min_num_listbox.insert(0, 'ALL NUMBERS')
        self._min_num_listbox.insert(1, '6 AND ABOVE')
        self._min_num_listbox.insert(2, '6 AND BELOW')
        self._min_num_listbox.insert(3, 'DOUBLE DIGITS')
        for n in range(0,13):
            self._min_num_listbox.insert(tkinter.END, 'only {}\'s'.format(n))
        
        _wrong_label = tkinter.Label(self._canvas, text='How many can you \nonly get wrong?', 
                                     font='Arial 20 bold', justify='right',anchor=tkinter.E)
        _wrong_label.grid(row=3, column=0, columnspan=2)
        self._wrong_lb = tkinter.Listbox(self._canvas, exportselection=False)
        self._wrong_lb.grid(row=3, column=1, columnspan=2, pady=10)
        self._wrong_lb.bind('<Return>', lambda event: self._on_start_down())
        for n in range(1,6):
            self._wrong_lb.insert(tkinter.END, n)
        
        _start_button = tkinter.Button(self._canvas, text='Start!', font='Arial 18', command=self._on_start_down)
        _start_button.grid(row=4, column=1, columnspan=2, pady=10)
        
        _quit_button = tkinter.Button(self._canvas, text='Quit', font='Arial 18', command=self.master.destroy)
        _quit_button.grid(row=4, column=2, pady=10)
        
    def _on_start_down(self):
        """
        Starts application after user clicks the start button.
        Sets up various options derived from previous start screen and creates first problem for flash cards.
        """
        self._name = self._name_entry.get() if self._name_entry.get() != 'What is your name?' else 'PLAYER'
        self._count_choice = int(self._wrong_lb.get(tkinter.ACTIVE))
        number_range = self._min_num_listbox.get(tkinter.ACTIVE)
        if number_range == 'ALL NUMBERS':
            self._min_num, self._max_num = (0,12)
        elif number_range == '6 AND ABOVE':
            self._min_num, self._max_num = (6,12)
        elif number_range == '6 AND BELOW':
            self._min_num, self._max_num = (0,6)
        elif number_range == 'DOUBLE DIGITS':
            self._min_num, self._max_num = (10,12)
        else:
            self._min_num, self._max_num = (int(number_range.split()[1].strip('\'s')),)*2
        self._canvas.destroy()
        self.create_flashcards()

    def game_over_screen(self):
        """Opens game over screen featuring a "Main Menu" button and "Quit" button."""
        self._canvas = tkinter.Canvas(self.master)
        self._canvas.grid()
        self._top_level()
        
        _game_over = tkinter.Label(self._canvas, text='Game over!', font='Arial 50 bold')
        _game_over.grid(row=0, column=0, columnspan=2, pady=10)
        _you_got = tkinter.Label(self._canvas, text='{} got:'.format(self._name), font='Arial 50 bold')
        _you_got.grid(row=1, column=0, padx=20)
        
        _correct = tkinter.Label(self._canvas, text='{} correct'.format(self._right), font='Arial 50 bold', foreground='green')
        _correct.grid(row=1, column=1)
        
        _wrong = tkinter.Label(self._canvas, text='{} wrong'.format(self._wrong_counter), font='Arial 50 bold', foreground='red')
        _wrong.grid(row=2, column=1)
        
        main_menu = tkinter.Button(self._canvas, text='Main menu', command=self._on_mainmenu)
        main_menu.grid(row=3, column=0, columnspan=2, pady=30)
        
        _quit = tkinter.Button(self._canvas, text='Quit', command=self.master.destroy)
        _quit.grid(row=3, column=1, pady=30)
        
    
    def _top_level(self):
        """Configures top level for canvas window."""
        top=self._canvas.winfo_toplevel()                
        top.rowconfigure(0, weight=1)            
        top.columnconfigure(0, weight=1)
        
    def _canvas_config(self):
        """Configures canvas rows and column positions and weights."""
        self._canvas.rowconfigure(0, weight=1)           
        self._canvas.columnconfigure(0, weight=1)
        
    def update_counter_correct(self):
        """Updates correct counter along with the wrong/correct displays."""
        self.inc_right()
        self.count_var.set('Correct: {}\nWrong: {}'.format(self._right, self._wrong_counter))
        
    def update_counter_wrong(self):
        """Updates wrong counter along with the wrong/correct displays."""
        self.inc_wrong()
        self.count_var.set('Correct: {}\nWrong: {}'.format(self._right, self._wrong_counter))
        
    def create_flashcards(self):
        """Creates problem screen featuring flash card interface and counter displays."""
        self._canvas = tkinter.Canvas(self.master)
        self._canvas.grid()
        self._top_level()
        
        self.count_var = tkinter.StringVar()
        self.count_var.set('Correct: 0\nWrong: 0')
        
        self.counter = tkinter.Label(self._canvas, textvariable=self.count_var, font=('Arial',25,'bold'))
        self.counter.grid(row=0,column=0)
        
        self._main_menu = tkinter.Button(self._canvas, text='Main menu', command=self._on_mainmenu)
        self._main_menu.grid(row=20, column=2,          
            sticky=tkinter.S+tkinter.E, pady=30)
        
        self._quit = tkinter.Button(self._canvas, text='Quit', command=self.master.destroy)
        self._quit.grid(row=20, column=3,          
            sticky=tkinter.S+tkinter.E, pady=30)
        
        self.new_numbers()
        
        self.display_numbers(self.first, self.sec)
        
        self._times = tkinter.Label(self._canvas, text='x', font=('Arial',100,'bold'))
        self._times.grid(row=2,column=0,
                         sticky=tkinter.N)

        self._line = tkinter.Label(self._canvas, text='------------------------------------------')
        self._line.grid(row=3, column=0, columnspan=2, sticky=tkinter.N)
        
        self._choose_question()
        
    def _choose_question(self):
        """
        Chooses a random interface for the user to answer a problem.
        This includes multiple choice, fill-in, and entry.
        """
        if len(str(self.correct_answer(self.first, self.sec))) > 1:
            random.choice([self.entry, self.multiple_choice, self.fill_in])()
        else:
            random.choice([self.entry, self.multiple_choice])()
        
    def _num_format(self, num):
        """Formats numbers to properly align flash card interface."""
        return '{}'.format(num) if len(str(num)) == 3 else\
            ' {}'.format(num) if len(str(num)) == 2 else '  {}'.format(num)
        
    def entry_answer(self):
        """Returns user's answer to problem."""
        return self._answer.get()
    
    def display_numbers(self, first, sec):
        """Displays the two numbers in flash card interface."""
        self._first_num = tkinter.Label(self._canvas, text='{}'.format(first) if len(str(first)) == 2 else '  {}'.format(first), font=('Arial',100,'bold'))
        self._first_num.grid(row=1,column=1,
                         sticky=tkinter.N)
        
        self._sec_num = tkinter.Label(self._canvas, text='{}'.format(sec) if len(str(sec)) == 2 else '  {}'.format(sec), font=('Arial',100,'bold'))
        self._sec_num.grid(row=2,column=1,
                         sticky=tkinter.N)
        
    def _display_correct(self):
        """Displays specific "Correct" messages if user answered correctly."""
        correct_messages = ['Good job {}!'.format(self._name), 'That\'s correct {}!'.format(self._name), 'Nice work {}!'.format(self._name)]
        self._correct_display = tkinter.Label(self._canvas, 
                                              text=random.choice(correct_messages) + ("\nThat's {} straight correct!".format(self._streak) if self._streak >= 5 else ''),
                                              font=('Arial',20,'bold'), anchor='e', foreground='green')
        self._correct_display.grid(row=0, column=1)      
        
    def _display_wrong(self):
        """Displays specific "Wrong" messages if user answered incorrectly."""
        self._correct_display = tkinter.Label(self._canvas, text='That\'s incorrect! \n{} x {} = {}.'.format(self.first, self.sec, self.correct_answer(self.first, self.sec)),
                                              font=('Arial',20,'bold'), anchor='e', foreground='red')
        self._correct_display.grid(row=0, column=1)
        
    def _display_error(self):
        """Displays specific "Error" messages if user entered an invalid input."""
        self._correct_display = tkinter.Label(self._canvas, text='Invalid entry!',
                                              font=('Arial',20,'bold'), anchor='e', foreground='red')
        self._correct_display.grid(row=0, column=1)   
        
    def new_numbers(self):
        """Creates new numbers for specific problem."""
        self.first, self.sec = self.choose_numbers()
        
    def entry(self):
        """Creates entry box for user to answer in a "Entry Question"."""
        default_text = tkinter.StringVar(); default_text.set('What is the answer?')
        self._answer = tkinter.Entry(self._canvas, justify='center', textvariable=default_text)
        self._answer.grid(row=4,column=1)
        self._answer.bind('<Button-1>', lambda event: default_text.set('') if self._answer.get() == 'What is the answer?'\
                                 else None)
        self._answer.bind('<Return>', lambda event: self._on_submit_down_entry())
        
        self._submit = tkinter.Button(self._canvas, text='Submit', command=self._on_submit_down_entry)
        self._submit.grid(row=4,column=2,sticky=tkinter.N)
        
    def multiple_choice(self):
        """Creates four specific multiple-choice buttons for user."""
        def choices_list():
            correct_answer = self.correct_answer(self.first, self.sec)
            if self.first == 0:
                return [0,1,2,3]
            elif self.sec == 0:
                return [0, self.first, random.choice([self.first-1,self.first+1]) if self.first-1 > 0 else self.first+1, random.choice([self.first-2,self.first+2]) if self.first-2 > 0 else self.first+2]
            elif 1 <= correct_answer <= 10:
                return list({correct_answer} | {correct_answer-n if correct_answer-n >= 0 else correct_answer+n for n in range(1,4)})
            return [correct_answer, random.randrange(correct_answer-10,correct_answer-3),
                       random.randrange(correct_answer+4,correct_answer+12), 
                       random.choice([i for i in range(correct_answer-3,correct_answer)]+\
                                     [i for i in range(correct_answer+1,correct_answer+4)])]

        choices = choices_list(); random.shuffle(choices)
        self._answer = tkinter.IntVar()
        self._answer.set(choices[0])
        
        self.choice1 = tkinter.Radiobutton(self._canvas, text=self._num_format(choices[0]), font=('Arial',17,'bold'), variable=self._answer, value=choices[0])
        self.choice1.grid(row=4, column=1); self.choice1.select()
        self.choice2 = tkinter.Radiobutton(self._canvas, text=self._num_format(choices[1]), font=('Arial',17,'bold'), variable=self._answer, value=choices[1])
        self.choice2.grid(row=5, column=1)
        self.choice3 = tkinter.Radiobutton(self._canvas, text=self._num_format(choices[2]), font=('Arial',17,'bold'), variable=self._answer, value=choices[2])
        self.choice3.grid(row=6, column=1)
        self.choice4 = tkinter.Radiobutton(self._canvas, text=self._num_format(choices[3]), font=('Arial',17,'bold'), variable=self._answer, value=choices[3])
        self.choice4.grid(row=7, column=1)
        
        self._canvas.bind('<Key>', lambda event: self._on_submit_down_mc())
        
        self._submit = tkinter.Button(self._canvas, text='Submit', command=self._on_submit_down_mc)
        self._submit.grid(row=7,column=2,sticky=tkinter.N)
        
    def fill_in(self):
        """Creates a fill-in-the-blank question for the user."""
        correct_answer = self.correct_answer(self.first, self.sec)
        
        # Displaying Incomplete answer Label
        to_replace = random.choice(str(correct_answer))
        self._answer_part = str(correct_answer).replace(to_replace, '_', 1)
        self.answer_part = tkinter.Label(self._canvas, text=self._answer_part, font=('Arial',100,'bold'))
        self.answer_part.grid(row=4, column=1)
        
        default_text = tkinter.StringVar(); default_text.set('Fill in the blank!')
        
        self.fill_in_entry = tkinter.Entry(self._canvas, justify='center', textvariable=default_text)
        self.fill_in_entry.grid(row=5, column=1)
        self.fill_in_entry.bind('<Button-1>', lambda event: default_text.set('') if self.fill_in_entry.get() == 'Fill in the blank!'\
                                 else None)
        self.fill_in_entry.bind('<Return>', lambda event: self._on_submit_down_fillin())
        
        self._submit = tkinter.Button(self._canvas, text='Submit', command=self._on_submit_down_fillin)
        self._submit.grid(row=5, column=2)
 
    def _mc_destroy(self):
        """Destroys widgets for multiple choice questions."""
        self.choice1.destroy()
        self.choice2.destroy()
        self.choice3.destroy()
        self.choice4.destroy()
        self._submit.destroy()
        
    def _entry_destroy(self):
        """Destroys widgets for entry questions."""
        self._answer.destroy()
        self._submit.destroy()
        
    def _fillin_destroy(self):
        """Destroys widgets for fill-in-the-blank questions."""
        self.answer_part.destroy()
        self.fill_in_entry.destroy()
        self._submit.destroy()
        
    def _correct_wrong_destroy(self):
        """Destroys widgets for wrong/correct counters."""
        self._correct_display.destroy()    
        
    def _on_mainmenu(self):
        """Destroys widgets for main menu and creates start screen."""
        self._canvas.destroy()
        self.start_screen()
        
    def _on_enter_entry(self, event):
        """Submits user's answer if user pressed "Enter"."""
        self._on_submit_down_entry()
        
    def _on_submit_down_entry(self):
        """Submits user's answer and updates counters, problems, and game over status for entry questions."""
        try:
            if (self._right, self._wrong_counter) != (0,0):
                self._correct_wrong_destroy()
            if self.correct(int(self.entry_answer()), self.first, self.sec):
                self.inc_streak()
                self._display_correct()
                self.update_counter_correct()
            else:
                self.reset_streak()
                self._display_wrong()
                self.update_counter_wrong()
            self._entry_destroy()
            self.new_numbers()
            self.display_numbers(self.first, self.sec)
            self._choose_question()
            if self.game_is_over():
                self._canvas.destroy()
                self.game_over_screen()
        except ValueError:
            self._display_error()
            
    def _on_submit_down_mc(self):
        """Submits user's answer and updates counters, problems, and game over status for multiple choice questions."""
        if (self._right, self._wrong_counter) != (0,0):
            self._correct_wrong_destroy()
        if self.correct(self._answer.get(), self.first, self.sec):
            self.inc_streak()
            self._display_correct()
            self.update_counter_correct()
        else:
            self.reset_streak()
            self._display_wrong()
            self.update_counter_wrong()
        self._mc_destroy()
        self.new_numbers()
        self.display_numbers(self.first, self.sec)
        self._choose_question()
        if self.game_is_over():
            self._canvas.destroy()
            self.game_over_screen()
        
    def _on_submit_down_fillin(self):
        """Submits user's answer and updates counters, problems, and game over status for fill-in questions."""
        try:
            if (self._right, self._wrong_counter) != (0,0):
                self._correct_wrong_destroy()
            if self.correct(int(self._answer_part.replace('_', self.fill_in_entry.get())), 
                        self.first, self.sec):
                self.inc_streak()
                self._display_correct()
                self.update_counter_correct()
            else:
                self.reset_streak()
                self._display_wrong()
                self.update_counter_wrong()
            self._fillin_destroy()
            self.new_numbers()
            self.display_numbers(self.first, self.sec)
            self._choose_question()
            if self.game_is_over():
                self._canvas.destroy()
                self.game_over_screen()
        except ValueError:
            self._display_error()
            
        
if __name__ == '__main__':
    app = MultiplicationApp()
    app.start()         
